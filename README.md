# Bubbles AI Reply System

## Overview

This system uses OpenAI (Pylon-like) NLP to classify and respond to 12 common customer support inquiries, integrates with Intercom for automated replies, and falls back to macros for reliability.

## Features

- Real AI-powered intent classification using OpenAI (gpt-4o) and instructor.
- Handles 12+ common support intents (see `ai_config/pylon_model_config.json`).
- Macro-based fallback for reliability.
- Intercom integration for automated response delivery.
- Easily extensible and testable.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Environment variables:**

   - `OPENAI_API_KEY`: Your OpenAI API key (for intent classification)
   - `INTERCOM_ACCESS_TOKEN`: Your Intercom personal access token
   - (Optional) Update `<YOUR_ADMIN_ID>` in `intercom_integration/send_reply.py` with your Intercom admin ID

   **How to obtain tokens:**

   - See the end of this file for step-by-step instructions.

3. **Configuration files:**
   - `ai_config/pylon_model_config.json`: List of supported intents and model settings
   - `fallback_macros/intercom_macros.json`: Macro responses for each intent
   - `ai_config/sample_queries.json`: Example queries for training/evaluation

## Usage

- Use the `PylonAI` class in `ai_config/pylon_ai.py`:
  ```python
  from ai_config.pylon_ai import PylonAI
  ai = PylonAI("ai_config/pylon_model_config.json")
  ai.handle_query("I want a refund for my last purchase.", conversation_id)
  ```
- The system will classify the query, generate a response, and send it via Intercom.

## Testing & QA

- See `tests/` for test cases, including performance, privacy, and security.
- Requirements and QA deliverables: `docs/QA_Assignment_Deliverables.md`

## Notes

- If OpenAI API is unavailable, the system falls back to keyword matching and macro responses.
- Ensure all environment variables are set before running.
- The file `intercom_integration/error_handler.py` is not needed and can be deleted.

## Extending

- Add new intents to `pylon_model_config.json` and `intercom_macros.json`.
- Update training data in `sample_queries.json` for better accuracy.

---

## How to Obtain API Tokens

### Intercom Access Token

1. Log in to Intercom and go to the Developer Hub.
2. Create a new app (Internal integration).
3. In your app, go to Authentication and generate a Personal Access Token.
4. Use this as `INTERCOM_ACCESS_TOKEN` in your `.env` file.

### OpenAI API Key

1. Log in to https://platform.openai.com/
2. Go to API Keys and create a new secret key.
3. Use this as `OPENAI_API_KEY` in your `.env` file.

---

For more, see the QA deliverables and code comments.
