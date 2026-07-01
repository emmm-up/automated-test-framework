from __future__ import annotations

from datetime import timedelta
from typing import Any

import pytest

from framework.base import APIClient


class FakeResponse:
    def __init__(
        self,
        status_code: int = 200,
        json_body: Any = None,
        text: str = "",
        headers: dict[str, str] | None = None,
        raise_error: Exception | None = None,
    ) -> None:
        self.status_code = status_code
        self._json_body = json_body
        self.text = text
        self.headers = headers or {"content-type": "application/json"}
        self.elapsed = timedelta(milliseconds=15)
        self._raise_error = raise_error

    def json(self) -> Any:
        if isinstance(self._json_body, ValueError):
            raise self._json_body
        return self._json_body

    def raise_for_status(self) -> None:
        if self._raise_error:
            raise self._raise_error


class FakeSession:
    def __init__(self, response: FakeResponse | None = None) -> None:
        self.response = response or FakeResponse(json_body={"ok": True})
        self.calls: list[dict[str, Any]] = []
        self.closed = False

    def request(self, method: str, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append({"method": method, "url": url, "kwargs": kwargs})
        return self.response

    def close(self) -> None:
        self.closed = True


@pytest.fixture
def fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture
def client(fake_session: FakeSession) -> APIClient:
    api_client = APIClient(base_url="https://api.example.test", timeout=10)
    api_client.session = fake_session
    return api_client
