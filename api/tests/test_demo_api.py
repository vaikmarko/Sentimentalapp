def test_echo_roundtrip(client):
    start = client.post("/api/demo/echo", json={"text": "tere stuudio"})
    assert start.status_code == 200
    run_id = start.json()["run_id"]

    result = client.get(f"/api/demo/echo/{run_id}")
    assert result.status_code == 200
    body = result.json()
    assert body["status"] == "done"
    assert body["result"] == {"text": "TERE STUUDIO"}


def test_echo_requires_auth():
    # No dependency override here — the real auth dependency must reject.
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as raw:
        res = raw.post("/api/demo/echo", json={"text": "x"})
    assert res.status_code == 401


def test_cannot_read_another_users_run(client):
    start = client.post("/api/demo/echo", json={"text": "private"})
    run_id = start.json()["run_id"]

    from app.core.auth import AuthedUser, get_current_user
    from app.main import app

    app.dependency_overrides[get_current_user] = lambda: AuthedUser(uid="someone-else")
    res = client.get(f"/api/demo/echo/{run_id}")
    assert res.status_code == 404
