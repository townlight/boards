from datetime import date

from fastapi.testclient import TestClient

from civicboards.attendance_tracker import summarize_attendance
from civicboards.board_registry import register_board_stub
from civicboards.main import app
from civicboards.notice_export import build_board_records_export
from civicboards.term_tracker import build_term_review_plan
from civicboards.vacancy_tracker import build_vacancy_checklist


client = TestClient(app)


def test_board_registry_flags_authority_and_boundary() -> None:
    result = register_board_stub(
        board_id="pc-001",
        board_name="Planning Commission",
        liaison="clerk@example.gov",
    )
    assert result.board_name == "Planning Commission"
    assert any("enabling authority" in note for note in result.roster_notes)
    assert "staff remain responsible" in result.disclaimer


def test_term_review_plan_builds_reminders() -> None:
    result = build_term_review_plan(member_name="Jordan Lee", term_end=date(2026, 12, 31))
    assert result.member_name == "Jordan Lee"
    assert len(result.reminders) == 4
    assert result.staff_review_required is True


def test_vacancy_checklist_requires_public_notice_review() -> None:
    result = build_vacancy_checklist(
        board_name="Library Board",
        vacancy_reason="resignation",
    )
    assert result.public_notice_required is True
    assert "application window" in result.checklist[2]


def test_attendance_summary_flags_low_attendance() -> None:
    result = summarize_attendance(
        member_name="Avery Patel",
        meetings_attended=2,
        meetings_held=5,
    )
    assert result.attendance_status == "review-required"
    assert result.staff_review_required is True
    assert any("remove or replace" in item for item in result.review_notes)


def test_records_export_preserves_board_context() -> None:
    result = build_board_records_export(board_id="pc-001", title="Planning Commission archive")
    assert result.board_id == "pc-001"
    assert "Preserve agenda" in result.checklist[0]
    assert "retention schedule" in result.retention_note


def test_board_support_apis_success_shape() -> None:
    registry = client.post(
        "/api/v1/civicboards/registry",
        json={
            "board_id": "pc-001",
            "board_name": "Planning Commission",
            "liaison": "clerk@example.gov",
        },
    )
    terms = client.post(
        "/api/v1/civicboards/terms",
        json={"member_name": "Jordan Lee", "term_end": "2026-12-31"},
    )
    vacancies = client.post(
        "/api/v1/civicboards/vacancies",
        json={"board_name": "Library Board", "vacancy_reason": "resignation"},
    )
    attendance = client.post(
        "/api/v1/civicboards/attendance",
        json={"member_name": "Avery Patel", "meetings_attended": 2, "meetings_held": 5},
    )
    export = client.post(
        "/api/v1/civicboards/export",
        json={"title": "Planning Commission archive", "board_id": "pc-001"},
    )
    assert registry.status_code == 200
    assert registry.json()["board_name"] == "Planning Commission"
    assert terms.status_code == 200
    assert len(terms.json()["reminders"]) == 4
    assert vacancies.status_code == 200
    assert vacancies.json()["public_notice_required"] is True
    assert attendance.status_code == 200
    assert attendance.json()["attendance_status"] == "review-required"
    assert export.status_code == 200
    assert export.json()["board_id"] == "pc-001"


def test_public_ui_route_is_accessible_and_honest() -> None:
    response = client.get("/civicboards")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert '<a class="skip-link" href="#main">Skip to main content</a>' in text
    assert '<main id="main" tabindex="-1">' in text
    assert "v0.1.0 board administration foundation" in text
    assert "does not appoint members" in text
    assert "system of record" in text
