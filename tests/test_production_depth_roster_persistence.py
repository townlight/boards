from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civicboards.main import app, _dispose_roster_repository
from civicboards.persistence import BoardRosterRepository


client = TestClient(app)


def test_repository_persists_board_roster_and_attendance_review(tmp_path: Path) -> None:
    db_path = tmp_path / "civicboards.db"
    db_url = f"sqlite+pysqlite:///{db_path.as_posix()}"

    repository = BoardRosterRepository(db_url=db_url)
    roster = repository.register_board(
        board_id="pc-001",
        board_name="Planning Commission",
        liaison="clerk@example.gov",
    )
    attendance = repository.create_attendance_review(
        member_name="Avery Patel",
        meetings_attended=2,
        meetings_held=5,
    )
    repository.engine.dispose()

    reloaded = BoardRosterRepository(db_url=db_url)
    stored_roster = reloaded.get_board(roster.board_id)
    stored_attendance = reloaded.get_attendance_review(attendance.attendance_id)
    reloaded.engine.dispose()

    assert stored_roster is not None
    assert stored_roster.board_name == "Planning Commission"
    assert stored_roster.liaison == "clerk@example.gov"
    assert stored_attendance is not None
    assert stored_attendance.attendance_status == "review-required"
    assert stored_attendance.staff_review_required is True
    db_path.unlink()


def test_roster_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicboards-api.db"
    monkeypatch.setenv("CIVICBOARDS_ROSTER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_roster_repository()

    created_board = client.post(
        "/api/v1/civicboards/registry",
        json={
            "board_id": "pc-001",
            "board_name": "Planning Commission",
            "liaison": "clerk@example.gov",
        },
    )
    fetched_board = client.get("/api/v1/civicboards/registry/pc-001")
    created_attendance = client.post(
        "/api/v1/civicboards/attendance",
        json={"member_name": "Avery Patel", "meetings_attended": 2, "meetings_held": 5},
    )
    attendance_id = created_attendance.json()["attendance_id"]
    fetched_attendance = client.get(f"/api/v1/civicboards/attendance/{attendance_id}")

    _dispose_roster_repository()
    monkeypatch.delenv("CIVICBOARDS_ROSTER_DB_URL")

    assert created_board.status_code == 200
    assert fetched_board.status_code == 200
    assert fetched_board.json()["board_name"] == "Planning Commission"
    assert created_attendance.status_code == 200
    assert attendance_id
    assert fetched_attendance.status_code == 200
    assert fetched_attendance.json()["attendance_status"] == "review-required"
    db_path.unlink()


def test_get_board_uses_default_local_persistence(monkeypatch) -> None:
    monkeypatch.delenv("CIVICBOARDS_ROSTER_DB_URL", raising=False)
    _dispose_roster_repository()

    created = client.post(
        "/api/v1/civicboards/registry",
        json={
            "board_id": "pc-001",
            "board_name": "Planning Commission",
            "liaison": "clerk@example.gov",
        },
    )
    response = client.get("/api/v1/civicboards/registry/pc-001")

    assert created.status_code == 200
    assert response.status_code == 200
    assert response.json()["board_name"] == "Planning Commission"


def test_get_attendance_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicboards-missing.db"
    monkeypatch.setenv("CIVICBOARDS_ROSTER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_roster_repository()

    response = client.get("/api/v1/civicboards/attendance/missing")

    _dispose_roster_repository()
    monkeypatch.delenv("CIVICBOARDS_ROSTER_DB_URL")

    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["message"] == "Attendance review record not found."
    assert "POST /api/v1/civicboards/attendance" in detail["fix"]
    db_path.unlink()


def test_staff_review_queue_requires_key_and_returns_items(monkeypatch) -> None:
    monkeypatch.setenv("CIVICBOARDS_STAFF_API_KEY", "local-boards-key")
    created = client.post(
        "/api/v1/civicboards/staff/reviews",
        headers={
            "X-CivicBoards-Role": "staff",
            "X-CivicBoards-Staff-Key": "local-boards-key",
        },
        json={
            "board_id": "pc-001",
            "title": "Planning Commission vacancy review",
            "reason": "Vacancy notice and appointment workflow need staff review.",
        },
    )

    denied = client.get("/api/v1/civicboards/staff/reviews")
    allowed = client.get(
        "/api/v1/civicboards/staff/reviews",
        headers={
            "X-CivicBoards-Role": "staff",
            "X-CivicBoards-Staff-Key": "local-boards-key",
        },
    )

    assert created.status_code == 200
    assert denied.status_code in {401, 403}
    assert allowed.status_code == 200
    assert allowed.json()["visibility"] == "staff_only"
    assert allowed.json()["items"][0]["board_id"] == "pc-001"


def test_attendance_review_creates_staff_review_queue_item(monkeypatch) -> None:
    monkeypatch.setenv("CIVICBOARDS_STAFF_API_KEY", "local-boards-key")
    attendance = client.post(
        "/api/v1/civicboards/attendance",
        json={"member_name": "Avery Patel", "meetings_attended": 2, "meetings_held": 5},
    )
    queue = client.get(
        "/api/v1/civicboards/staff/reviews",
        headers={
            "X-CivicBoards-Role": "staff",
            "X-CivicBoards-Staff-Key": "local-boards-key",
        },
    )

    assert attendance.status_code == 200
    assert attendance.json()["staff_review_required"] is True
    assert queue.status_code == 200
    assert any("Attendance review" in item["title"] for item in queue.json()["items"])
