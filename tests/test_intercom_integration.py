from typing import Generator
import pytest
from intercom_integration.send_reply import send_reply


class DummyMessages:
    def __init__(self, parent):
        self.parent = parent

    def create(self, **kwargs):
        self.parent.last = kwargs
        return kwargs


class DummyConversations:
    def __init__(self, parent):
        self.parent = parent

    def create(self, *args, **kwargs):
        self.parent.last = {"args": args, "kwargs": kwargs}
        return self.parent.last

    def reply(self, *args, **kwargs):
        self.parent.last = {"args": args, "kwargs": kwargs}
        return self.parent.last


class DummyIntercom:
    def __init__(self):
        self.last = None
        self.messages = DummyConversations(self)
        self.conversations = DummyConversations(self)


@pytest.fixture(autouse=True)
def patch_intercom(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[DummyIntercom, None, None]:
    import intercom_integration.send_reply as sr

    dummy = DummyIntercom()
    monkeypatch.setattr(sr, "intercom", dummy)
    yield dummy


def test_send_reply_success(patch_intercom: DummyIntercom) -> None:
    send_reply("user_1", "Hello!")
    assert patch_intercom.last is not None
    assert patch_intercom.last["kwargs"]["id"] == "user_1"
    assert patch_intercom.last["kwargs"]["body"] == "Hello!"
    assert patch_intercom.last["kwargs"]["type"] == "admin"
    assert patch_intercom.last["kwargs"]["message_type"] == "comment"


def test_send_reply_error(monkeypatch: pytest.MonkeyPatch) -> None:
    import intercom_integration.send_reply as sr

    def fail_create(**kwargs) -> None:
        raise Exception("API error simulated")

    monkeypatch.setattr(sr.intercom.messages, "create", fail_create)
    send_reply("user_2", "Test error handling")


def test_reply_with_note(patch_intercom: DummyIntercom) -> None:
    send_reply("user_3", "Internal note here", message_type="note")
    assert patch_intercom.last is not None
    assert patch_intercom.last["kwargs"]["message_type"] == "note"
    assert patch_intercom.last["kwargs"]["body"] == "Internal note here"


def test_reply_and_close_conversation(patch_intercom: DummyIntercom) -> None:
    send_reply("user_4", "Closing this conversation", message_type="close")
    assert patch_intercom.last is not None
    assert patch_intercom.last["kwargs"]["message_type"] == "close"
    assert patch_intercom.last["kwargs"]["body"] == "Closing this conversation"


def test_reply_as_user(patch_intercom: DummyIntercom) -> None:
    send_reply(
        "conv_123",
        "Replying as user",
        message_type="comment",
        reply_type="user",
        user_id="user_123",
    )
    assert patch_intercom.last is not None
    assert patch_intercom.last["kwargs"]["type"] == "user"
    assert patch_intercom.last["kwargs"]["id"] == "conv_123"
    assert patch_intercom.last["kwargs"]["body"] == "Replying as user"
