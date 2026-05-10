from __future__ import annotations


def test_list_users(client):
    resp = client.get("/api/v1/users")
    assert resp.status_code == 200
