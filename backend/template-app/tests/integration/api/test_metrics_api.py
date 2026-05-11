import pytest


@pytest.mark.asyncio
async def test_metrics(client):
    response = await client.get("/observability/metrics")
    assert response.status_code == 200
    assert "cpu_percent" in response.json()
