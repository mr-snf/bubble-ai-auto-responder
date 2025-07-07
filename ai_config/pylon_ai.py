import json
from configs.config import MAX_TOKENS, TEMPERATURE, TOP_P, ENDPOINT, MODEL
from intercom_integration.send_reply import send_reply
from pydantic import BaseModel, Field
from typing import Literal
import os
from openai import OpenAI
import numpy as np

token = os.environ["GITHUB_TOKEN"]

client = OpenAI(
    base_url=ENDPOINT,
    api_key=token,
)


class ClassificationResponse(BaseModel):
    """
    Classifies customer support queries into one of the supported intents.
    """

    intent: Literal[
        "invoice_request",
        "refund_request",
        "email_change",
        "password_reset",
        "account_closure",
        "feature_request",
        "bug_report",
        "subscription_upgrade",
        "subscription_cancellation",
        "delivery_status",
        "payment_issue",
        "general_inquiry",
    ] = Field(..., description="Predicted intent label.")
    chain_of_thought: str = Field(..., description="Reasoning for the prediction.")


def get_embedding(text: str) -> list:
    response = client.embeddings.create(input=text, model=MODEL)
    return response.data[0].embedding


def precompute_sample_embeddings(sample_path: str, out_path: str):
    with open(sample_path) as f:
        samples = json.load(f)
    sample_embeddings = []
    for item in samples:
        emb = get_embedding(item["query"])
        sample_embeddings.append(
            {"embedding": emb, "intent": item["intent"], "query": item["query"]}
        )
    with open(out_path, "w") as f:
        json.dump(sample_embeddings, f)


class PylonAI:
    def __init__(
        self,
        model_config_path: str,
        embedding_path: str = "data/sample_embeddings.json",
    ):
        with open(model_config_path) as f:
            self.config = json.load(f)
        self.intents = self.config["intents"]
        self.embedding_path = embedding_path
        self.sample_embeddings = None
        if os.path.exists(self.embedding_path):
            with open(self.embedding_path) as f:
                self.sample_embeddings = json.load(f)

    def classify_intent(self, query: str) -> str:
        if self.sample_embeddings:
            user_emb = np.array(get_embedding(query))
            best_score = -1
            best_intent = None
            for item in self.sample_embeddings:
                sample_emb = np.array(item["embedding"])
                score = np.dot(user_emb, sample_emb) / (
                    np.linalg.norm(user_emb) * np.linalg.norm(sample_emb)
                )
                if score > best_score:
                    best_score = score
                    best_intent = item["intent"]
            return best_intent if best_intent is not None else "general_inquiry"

        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=MAX_TOKENS,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Classify the following customer support query into one of the intents: "
                            + ", ".join(self.intents)
                            + ". Respond ONLY with the intent label."
                        ),
                    },
                    {
                        "role": "user",
                        "content": query,
                    },
                ],
            )
            content = (
                response.choices[0].message.content
                if response.choices and response.choices[0].message
                else None
            )
            intent = content.strip() if content else "general_inquiry"
            return intent
        except Exception as e:
            print(f"Error with OpenAI intent classification: {e}")
            for intent in self.intents:
                if intent.replace("_", " ") in query.lower():
                    return intent
            return "general_inquiry"

    def generate_response(self, intent: str, user_query: str = "") -> str:
        try:
            with open("fallback_macros/intercom_macros.json") as f:
                macros = json.load(f)["macros"]
            macro_response = next(
                (macro["response"] for macro in macros if macro["intent"] == intent),
                None,
            )
            if not macro_response:
                macro_response = (
                    "Thank you for contacting support. How can we help you?"
                )
            prompt = (
                f"You are a helpful customer support agent. "
                f"A user asked: '{user_query}'. "
                f"The intent is '{intent}'. "
                f"Here is a suggested response: '{macro_response}'. "
                f"Please write a detailed, helpful, and friendly reply in more than 150 words, "
                f"but less than 200 words, "
                f"expanding on the macro if possible. "
                f"Please do not include any other text in your response."
            )
            response = client.chat.completions.create(
                model=MODEL,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=MAX_TOKENS,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful customer support agent.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            content = (
                response.choices[0].message.content
                if response.choices
                and response.choices[0].message
                and response.choices[0].message.content
                else None
            )
            if content:
                return content.strip()
            else:
                return macro_response
        except Exception as e:
            print(f"Error with OpenAI response generation: {e}")
            with open("fallback_macros/intercom_macros.json") as f:
                macros = json.load(f)["macros"]
            for macro in macros:
                if macro["intent"] == intent:
                    return macro["response"]
            return "Thank you for contacting support. How can we help you?"

    def handle_query(self, query: str, conversation_id: str) -> tuple[str, str]:
        intent = self.classify_intent(query)
        response = self.generate_response(intent, user_query=query)
        send_reply(conversation_id, response)
        return intent, response
