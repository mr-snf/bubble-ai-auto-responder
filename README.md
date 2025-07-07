# Bubbles AI Reply System

## Overview

This system uses OpenAI (Pylon-like) NLP to classify and respond to 12+ common customer support inquiries, integrates with Intercom for automated replies, and falls back to macros for reliability.

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
   - `INTERCOM_ADMIN_ID`: Your Intercom admin ID

   You can set these in your shell or in a `.env` file. The project uses `python-dotenv` to load environment variables automatically.

   Example `.env` file:

   ```env
   OPENAI_API_KEY=sk-...your-openai-key...
   INTERCOM_ACCESS_TOKEN=your_intercom_token
   INTERCOM_ADMIN_ID=your_admin_id
   ```

3. **Configuration files:**
   - `ai_config/pylon_model_config.json`: List of supported intents and model settings
   - `fallback_macros/intercom_macros.json`: Macro responses for each intent
   - `data/sample_queries.json`: Example queries for training/evaluation

## Usage

- **Run the system interactively:**

  ```bash
  python main.py
  ```

  This will prompt you for a customer query and a conversation ID, classify the intent, generate a response, and (if configured) send it to Intercom.

- **Use the PylonAI class in your code:**
  ```python
  from ai_config.pylon_ai import PylonAI
  ai = PylonAI("ai_config/pylon_model_config.json")
  ai.handle_query("I want a refund for my last purchase.", conversation_id)
  ```
  The system will classify the query, generate a response, and send it via Intercom.

## Intercom Integration Notes

- The code uses `from intercom.client import Client` and the `conversations.reply` method to send replies to Intercom conversations.
- If you are running locally and do not want to send real messages, use dummy values for the environment variables.
- If the environment variables are not set, the system will use empty strings, which will not connect to Intercom.

## Testing & QA

- Run all tests with:
  ```bash
  pytest tests
  ```
- The `pytest.ini` file ensures the project root is in the Python path for imports.
- See `tests/` for test cases, including performance, privacy, and security.
- Requirements and QA deliverables: `docs/QA_Assignment_Deliverables.md`

## Troubleshooting

- **ModuleNotFoundError:**
  - Ensure you are running from the project root and that dependencies are installed.
  - The `pytest.ini` file should resolve most import issues for tests.
- **Intercom import errors:**
  - The correct import is `from intercom.client import Client` for this project version.
  - Ensure you have `intercom==0.2.3` installed (as specified in `requirements.txt`).
- **Environment variable issues:**
  - Make sure your `.env` file is present and correct, or export variables in your shell.
  - The system will use empty strings if variables are missing, which disables real Intercom integration.

## Notes

- If OpenAI API is unavailable, the system falls back to keyword matching and macro responses.
- Ensure all environment variables are set before running for full functionality.
- For local testing, you can use dummy values for all environment variables.

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
