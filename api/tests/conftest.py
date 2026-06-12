import pytest
from fastapi.testclient import TestClient

from app.core.auth import AuthedUser, get_current_user
from app.main import app
from app.routes import deps

TEST_USER = AuthedUser(uid="test-uid", email="test@example.com", name="Test User")


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    from app.core.config import get_settings

    get_settings.cache_clear()
    deps.get_runner.cache_clear()  # fresh in-memory store per test
    app.dependency_overrides[get_current_user] = lambda: TEST_USER
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    get_settings.cache_clear()
