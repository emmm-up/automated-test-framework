from tests.conftest import FakeResponse


def test_create_then_fetch_user_workflow(client, fake_session):
    fake_session.response = FakeResponse(status_code=201, json_body={"id": 42, "name": "Ada"})
    created = client.post("/users", json={"name": "Ada"})

    fake_session.response = FakeResponse(status_code=200, json_body={"id": created.json()["id"], "name": "Ada"})
    fetched = client.get(f"/users/{created.json()['id']}")

    assert created.status_code == 201
    assert fetched.json() == {"id": 42, "name": "Ada"}
    assert [call["method"] for call in fake_session.calls] == ["POST", "GET"]
