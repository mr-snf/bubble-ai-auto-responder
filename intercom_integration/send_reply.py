import os


from dotenv import load_dotenv
from intercom.client import Client

load_dotenv()

intercom = Client(personal_access_token=os.getenv("INTERCOM_ACCESS_TOKEN", ""))
admin_id = os.getenv("INTERCOM_ADMIN_ID", "1234567890")


def send_reply(conversation_id: str, message: str) -> None:
    try:
        intercom.conversations.reply(
            id=conversation_id,
            type="admin",
            admin_id=admin_id,
            message_type="comment",
            body=message,
        )
        print(f"Message sent to conversation {conversation_id}")
    except Exception as e:
        print(f"Error sending message: {e}")
