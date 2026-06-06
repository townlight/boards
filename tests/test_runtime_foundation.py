from fastapi.testclient import TestClient

import civicboards
from civicboards.main import app


client = TestClient(app)


def test_package_version_is_011() -> None:
    assert civicboards.__version__ == "0.1.1"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "CivicBoards"
    assert data["status"] == "board administration foundation plus roster persistence"
    assert "local-first database-backed board roster" in data["message"]
    assert "appointment decisions" in data["message"]
    assert data["version"] == "0.1.1"
    assert data["next_step"].startswith("Open /civicboards/staff")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "civicboards"
    assert data["version"] == "0.1.1"
    assert data["civiccore_version"] == "1.2.0"


def test_readiness_is_green_with_default_local_database() -> None:
    response = client.get("/api/v1/civicboards/readiness")
    assert response.status_code == 200
    data = response.json()

    assert data["ready"] is True
    assert data["schema_ready"] is True
    assert data["using_default_local_database"] is True
    assert data["roster_database_configured"] is True


def test_integration_contracts_advertise_suite_handoffs() -> None:
    response = client.get("/api/v1/civicboards/integration-contracts")
    assert response.status_code == 200
    data = response.json()
    contracts = {contract["name"] for contract in data["contracts"]}

    assert "civicboards.board_roster.v1" in contracts
    assert "civicboards.staff_review_queue.v1" in contracts
    assert "civicboards.notice_packet.v1" in contracts
    assert "civicboards.records_export.v1" in contracts
    assert "civicnotice public vacancy notices" in data["downstream_ready_for"]
