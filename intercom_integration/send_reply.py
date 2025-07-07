import os


from dotenv import load_dotenv
from intercom.client import Client

load_dotenv()

intercom = Client(personal_access_token=os.getenv("INTERCOM_ACCESS_TOKEN", ""))
admin_id = os.getenv("INTERCOM_ADMIN_ID", "1234567890")


def send_reply(
    conversation_id: str,
    message: str,
    message_type: str = "comment",
    reply_type: str = "admin",
    user_id: str = "user_1",
) -> None:
    try:
        intercom.conversations.reply(
            id=conversation_id,
            type=reply_type,
            admin_id=admin_id if reply_type == "admin" else user_id,
            message_type=message_type,
            body=message,
        )
        print(f"Message sent to conversation {conversation_id}")
    except Exception as e:
        print(f"Error sending message: {e}")
