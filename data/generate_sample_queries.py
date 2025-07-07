import json
import random
import os
import copy
from collections import defaultdict

intents = [
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
]

# Example templates for each intent
intent_templates = {
    "invoice_request": [
        "Can I get a copy of my invoice?",
        "Please send me my latest invoice.",
        "Where can I download my billing statement?",
        "I need an invoice for my last payment.",
        "Could you email me my invoice?",
        "How do I get a receipt for my purchase?",
        "Send me the invoice for last month.",
        "I want to see my previous invoices.",
        "Can you provide my billing history?",
        "Where is my invoice for the last order?",
    ],
    "refund_request": [
        "I want a refund for my last purchase.",
        "Can I get my money back?",
        "I was charged incorrectly, please refund.",
        "How do I request a refund?",
        "Refund the payment for my last order.",
        "I need a refund for a duplicate charge.",
        "Please process my refund.",
        "I want to return my order and get a refund.",
        "How long does a refund take?",
        "Refund my recent transaction.",
    ],
    "email_change": [
        "How do I change my email address?",
        "I want to update my email.",
        "My email is wrong, how do I fix it?",
        "Can you change my account email?",
        "I need to use a new email address.",
        "Update my contact email, please.",
        "Change my email to john@example.com.",
        "I want to register a different email.",
        "How do I update my login email?",
        "Switch my account to a new email.",
    ],
    "password_reset": [
        "I forgot my password.",
        "How do I reset my password?",
        "Send me a password reset link.",
        "I can't log in, need to reset password.",
        "Help me recover my password.",
        "I want to change my password.",
        "Forgot my login password.",
        "Reset my account password.",
        "How do I get a new password?",
        "I need to update my password.",
    ],
    "account_closure": [
        "Please close my account.",
        "How do I delete my account?",
        "I want to deactivate my profile.",
        "Remove my account from your system.",
        "Delete my user account.",
        "I no longer need my account, please close it.",
        "Terminate my account.",
        "How do I permanently delete my account?",
        "Please remove all my data and close my account.",
        "I want to opt out and close my account.",
    ],
    "feature_request": [
        "Can you add this feature?",
        "I have a suggestion for a new feature.",
        "It would be great if you could add...",
        "Is it possible to implement this feature?",
        "I'd like to request a new functionality.",
        "Can you improve the app with this feature?",
        "Please consider adding this option.",
        "Feature request: dark mode.",
        "Can you add multi-language support?",
        "I want a new feature for notifications.",
    ],
    "bug_report": [
        "I found a bug in your app.",
        "The app crashes when I try to login.",
        "There's an error on the payment page.",
        "I encountered a glitch in the system.",
        "Something isn't working as expected.",
        "I think I discovered a bug.",
        "The app freezes on startup.",
        "Unexpected error message appears.",
        "The download button doesn't work.",
        "I can't submit my form due to a bug.",
    ],
    "subscription_upgrade": [
        "I want to upgrade my subscription.",
        "How do I get more features?",
        "Can I switch to a higher plan?",
        "Upgrade my account, please.",
        "I want to access premium features.",
        "How do I upgrade my subscription?",
        "Upgrade to the pro plan.",
        "I want to unlock advanced features.",
        "Can I get a business subscription?",
        "How do I move to a better plan?",
    ],
    "subscription_cancellation": [
        "Cancel my subscription.",
        "I want to stop my subscription.",
        "How do I cancel my plan?",
        "Please cancel my account renewal.",
        "I don't want to be billed again.",
        "End my subscription, please.",
        "How do I turn off auto-renewal?",
        "Cancel my premium plan.",
        "I want to unsubscribe from your service.",
        "Stop my monthly subscription.",
    ],
    "delivery_status": [
        "Where is my order?",
        "What's the status of my delivery?",
        "Has my package shipped yet?",
        "When will my order arrive?",
        "Track my shipment.",
        "I haven't received my order.",
        "Where is my package?",
        "Order tracking shows no update.",
        "My delivery is late.",
        "Can you check my order status?",
    ],
    "payment_issue": [
        "My payment failed.",
        "Why was my payment declined?",
        "I can't complete my payment.",
        "There was an error processing my payment.",
        "My card was charged but order not placed.",
        "Payment didn't go through.",
        "Payment page is not loading.",
        "I was double charged.",
        "How do I fix a payment error?",
        "My payment is pending.",
    ],
    "general_inquiry": [
        "I have a question.",
        "Can you help me with something?",
        "I need assistance.",
        "How do I use your service?",
        "What are your business hours?",
        "Can I speak to a representative?",
        "How do I contact support?",
        "Where can I find your FAQ?",
        "Do you offer live chat?",
        "What services do you provide?",
    ],
}

# Substitution options for placeholders
substitutions = {
    "invoice": ["invoice", "bill", "statement", "receipt"],
    "order": ["order", "purchase", "item", "package"],
    "account": ["account", "profile", "user account"],
    "email": ["email", "e-mail", "mail address"],
    "password": ["password", "passcode", "login password"],
    "subscription": ["subscription", "plan", "membership"],
    "feature": ["feature", "option", "functionality"],
    "payment": ["payment", "transaction", "charge", "billing"],
    "delivery": ["delivery", "shipment", "package", "order"],
    "bug": ["bug", "issue", "problem", "error"],
    "support": ["support", "helpdesk", "customer service"],
}

# Polite prefixes and suffixes
prefixes = ["", "Hi, ", "Hello, ", "Hey team, ", "Greetings, "]
suffixes = ["", " Thanks!", " Please help.", " ASAP.", " Thank you."]

# Minor mutation functions for diversity
mutation_funcs = [
    lambda s: s,  # original
    lambda s: s.lower(),
    lambda s: s.upper(),
    lambda s: s.capitalize(),
    lambda s: s.replace("?", "!"),
    lambda s: s.replace(".", "!"),
]


def generate_combinations(template, substitutions):
    # Find all words in the template that are keys in substitutions
    keys = [k for k in substitutions if k in template]
    if not keys:
        return [template]
    # For each key, get all possible substitutions
    from itertools import product

    options = [substitutions[k] for k in keys]
    all_combos = list(product(*options))
    results = []
    for combo in all_combos:
        temp = template
        for k, v in zip(keys, combo):
            temp = temp.replace(k, v)
        results.append(temp)
    return results


def main():
    # Backup old queries if file exists
    if os.path.exists("data/sample_queries.json"):
        with open("data/sample_queries.json") as f:
            old_queries = json.load(f)
        with open("data/sample_queries_backup.json", "w") as f:
            json.dump(old_queries, f, indent=2)
        print(f"Backed up {len(old_queries)} old queries to sample_queries_backup.json")
    else:
        old_queries = []

    queries = []
    queries_per_intent = defaultdict(list)

    # 1. Old random logic (preserved)
    samples_per_intent = 2000 // len(intents)
    for intent in intents:
        templates = intent_templates[intent]
        for i in range(samples_per_intent):
            template = random.choice(templates)
            temp = template
            for k, opts in substitutions.items():
                if k in temp:
                    temp = temp.replace(k, random.choice(opts))
            q = {"query": temp, "intent": intent}
            queries.append(q)
            queries_per_intent[intent].append(q)

    # 2. Systematic combinatorial generation
    for intent in intents:
        for template in intent_templates[intent]:
            combos = generate_combinations(template, substitutions)
            for combo in combos:
                for prefix in prefixes:
                    for suffix in suffixes:
                        base = f"{prefix}{combo}{suffix}".strip()
                        for mutate in mutation_funcs:
                            mutated = mutate(base)
                            q = {"query": mutated, "intent": intent}
                            queries.append(q)
                            queries_per_intent[intent].append(q)

    # 3. Add old queries (if any)
    for q in old_queries:
        queries.append(q)
        queries_per_intent[q["intent"]].append(q)

    # 4. Deduplicate
    seen = set()
    unique_queries = []
    unique_per_intent = defaultdict(list)
    for q in queries:
        key = (q["query"].strip().lower(), q["intent"])
        if key not in seen:
            seen.add(key)
            unique_queries.append(q)
            unique_per_intent[q["intent"]].append(q)

    # 5. If more than 2000, randomly sample 2000
    if len(unique_queries) > 2000:
        unique_queries = random.sample(unique_queries, 2000)
        # Rebuild per-intent counts
        unique_per_intent = defaultdict(list)
        for q in unique_queries:
            unique_per_intent[q["intent"]].append(q)
    # 6. If fewer, augment with minor mutations
    elif len(unique_queries) < 2000:
        needed = 2000 - len(unique_queries)
        extra = []
        for q in unique_queries:
            for mutate in mutation_funcs:
                mutated = mutate(q["query"])
                key = (mutated.strip().lower(), q["intent"])
                if key not in seen:
                    seen.add(key)
                    extra.append({"query": mutated, "intent": q["intent"]})
                if len(extra) >= needed:
                    break
            if len(extra) >= needed:
                break
        unique_queries.extend(extra[:needed])
        # Update per-intent
        for q in extra[:needed]:
            unique_per_intent[q["intent"]].append(q)

    # 7. Output
    with open("data/sample_queries.json", "w") as f:
        json.dump(unique_queries, f, indent=2)
    print(
        f"Generated {len(unique_queries)} unique sample queries in sample_queries.json"
    )
    print("Breakdown by intent:")
    for intent in intents:
        print(f"  {intent}: {len(unique_per_intent[intent])}")


if __name__ == "__main__":
    main()
