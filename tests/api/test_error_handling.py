import pytest
import requests

from tests.conftest import FakeResponse


def test_http_error_is_raised(client, fake_session):
    fake_session.response = FakeResponse(
        status_code=500,
        json_body={"error": "server"},
        raise_error=requests.HTTPError("500 server error"),
    )

    with pytest.raises(requests.HTTPError, match="500 server error"):
        client.get("/fail")


def test_non_json_response_can_be_logged(client, fake_session):
    fake_session.response = FakeResponse(json_body=ValueError("not json"), text="plain text")

    response = client.get("/plain")

    assert response.text == "plain text"
