def test_app_starts(client):
    response = client.get("/docs")
    assert response.status_code == 200

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
