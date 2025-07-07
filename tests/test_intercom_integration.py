from typing import Generator
import pytest
from intercom_integration.send_reply import send_reply


class DummyMessages:
    def __init__(self, parent):
        self.parent = parent

    def create(self, **kwargs):
        self.parent.last = kwargs
        return kwargs


class DummyIntercom:
    def __init__(self):
        self.last = None
        self.messages = DummyMessages(self)


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
    assert patch_intercom.last["to"]["id"] == "user_1"
    assert patch_intercom.last["body"] == "Hello!"


def test_send_reply_error(monkeypatch: pytest.MonkeyPatch) -> None:
    import intercom_integration.send_reply as sr

    def fail_create(**kwargs):
        raise Exception("API error simulated")

    monkeypatch.setattr(sr.intercom.messages, "create", fail_create)
    send_reply("user_2", "Test error handling")
