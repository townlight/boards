from fastapi.testclient import TestClient

import townlight_boards
from townlight_boards.main import app


client = TestClient(app)


def test_package_version() -> None:
    assert townlight_boards.__version__ == "0.2.0"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Townlight Boards"
    assert data["status"] == "board administration foundation plus roster persistence"
    assert "database-backed board roster and attendance review records" in data["message"]
    assert "appointment decisions" in data["message"]
    assert data["version"] == "0.2.0"
    assert "Post-v0.2.0 roadmap" in data["next_step"]


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "townlight_boards"
    assert data["version"] == "0.2.0"
    assert data["townlight_core_version"] == "1.3.0.dev2"
