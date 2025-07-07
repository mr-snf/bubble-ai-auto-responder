from ai_config.pylon_ai import PylonAI


def main():
    print("Bubbles AI Reply System - Local Test Mode\n")
    ai = PylonAI("ai_config/pylon_model_config.json")
    while True:
        query = input("Enter a customer query (or 'quit' to exit): ")
        if query.strip().lower() == "quit":
            break
        conversation_id = (
            input("Enter a conversation ID (or leave blank for dummy): ")
            or "dummy_convo_id"
        )
        intent, response = ai.handle_query(query, conversation_id)
        print(f"\nIntent classified: {intent}")
        print(f"Generated response:\n{response}\n")
        print("-" * 40)


if __name__ == "__main__":
    main()
