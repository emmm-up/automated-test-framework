def test_get_request_builds_relative_url(client, fake_session):
    response = client.get("/users", params={"active": "true"})

    assert response.status_code == 200
    assert fake_session.calls[0]["method"] == "GET"
    assert fake_session.calls[0]["url"] == "https://api.example.test/users"
    assert fake_session.calls[0]["kwargs"]["params"] == {"active": "true"}


def test_get_request_applies_default_timeout(client, fake_session):
    client.get("/health")

    assert fake_session.calls[0]["kwargs"]["timeout"] == 10
