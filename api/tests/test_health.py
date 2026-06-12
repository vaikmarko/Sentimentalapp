def test_healthz(client):
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"ok": True}


def test_version(client):
    res = client.get("/version")
    assert res.status_code == 200
    assert "version" in res.json()
