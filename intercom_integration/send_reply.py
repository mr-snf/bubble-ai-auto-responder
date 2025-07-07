import os

from intercom.client import Client
from dotenv import load_dotenv

load_dotenv()

intercom = Client(personal_access_token=os.getenv("INTERCOM_ACCESS_TOKEN"))
admin_id = os.getenv("INTERCOM_ADMIN_ID")


def send_reply(conversation_id: str, message: str) -> None:
    try:
        intercom.messages.create(
            message_type="inapp",
            body=message,
            from_={"type": "admin", "id": admin_id},
            to={"type": "user", "id": conversation_id},
        )
        print(f"Message sent to {conversation_id}")
    except Exception as e:
        print(f"Error sending message: {e}")
