"""Configure explicit credentials for existing authorized workflow tests."""
import pytest

@pytest.fixture(autouse=True)
def configured_boards_staff_key(monkeypatch):
    monkeypatch.setenv("TOWNLIGHT_BOARDS_STAFF_API_KEY", "test-only-key")
