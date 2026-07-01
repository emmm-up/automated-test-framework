def test_post_request_sends_json_body(client, fake_session):
    response = client.post("/users", json={"name": "Ada"})

    assert response.json() == {"ok": True}
    assert fake_session.calls[0]["method"] == "POST"
    assert fake_session.calls[0]["kwargs"]["json"] == {"name": "Ada"}


def test_put_and_patch_requests_share_payload_handling(client, fake_session):
    client.put("/users/1", json={"name": "Grace"})
    client.patch("/users/1", json={"role": "admin"})

    assert [call["method"] for call in fake_session.calls] == ["PUT", "PATCH"]
    assert fake_session.calls[1]["kwargs"]["json"] == {"role": "admin"}
