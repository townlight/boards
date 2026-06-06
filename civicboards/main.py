"""FastAPI runtime foundation for CivicBoards."""

import os
from datetime import date
from pathlib import Path

from civiccore import __version__ as CIVICCORE_VERSION
from civiccore.auth import staff_key_gate
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from civicboards import __version__
from civicboards.attendance_tracker import summarize_attendance
from civicboards.board_registry import register_board_stub
from civicboards.notice_export import build_board_records_export
from civicboards.persistence import BoardRosterRepository, StaffReviewQueueItem, StoredAttendanceReview
from civicboards.public_ui import render_public_lookup_page, render_staff_page
from civicboards.term_tracker import build_term_review_plan
from civicboards.vacancy_tracker import build_vacancy_checklist


app = FastAPI(
    title="CivicBoards",
    version=__version__,
    description="Board and commission roster, terms, vacancies, attendance, notices, and records-export support for CivicSuite.",
)

_roster_repository: BoardRosterRepository | None = None
_roster_db_url: str | None = None
_require_staff_key = staff_key_gate("CIVICBOARDS_STAFF_API_KEY", "X-CivicBoards-Staff-Key")


class BoardRegistryRequest(BaseModel):
    board_id: str = Field(..., min_length=1, max_length=160)
    board_name: str = Field(..., min_length=1, max_length=500)
    liaison: str = Field(..., min_length=1, max_length=255)


class TermRequest(BaseModel):
    member_name: str
    term_end: date


class VacancyRequest(BaseModel):
    board_name: str
    vacancy_reason: str


class AttendanceRequest(BaseModel):
    member_name: str
    meetings_attended: int
    meetings_held: int


class RecordsExportRequest(BaseModel):
    board_id: str
    title: str
    format: str = "markdown"


class StaffReviewCreateRequest(BaseModel):
    board_id: str = Field(..., min_length=1, max_length=160)
    title: str = Field(..., min_length=1, max_length=500)
    reason: str = Field(..., min_length=1, max_length=1000)


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicBoards",
        "version": __version__,
        "status": "board administration foundation plus roster persistence",
        "message": (
            "CivicBoards package, API foundation, sample board registry, term tracking, "
            "vacancy checklist, attendance summary, local-first database-backed board roster and attendance "
            "review records, staff review queues, CivicClerk/CivicNotice handoff contracts, records export checklist, "
            "and public/staff UI foundations are online; live agenda systems, appointment decisions, legal advice, "
            "live LLM calls, official notice publication, meeting system write-back, and board system-of-record integrations are not implemented."
        ),
        "next_step": "Open /civicboards/staff for board roster intake, attendance review, and staff queue triage.",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civicboards",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/ready")
def ready() -> dict[str, object]:
    return _readiness_payload()


@app.get("/api/v1/civicboards/readiness")
def readiness() -> dict[str, object]:
    return _readiness_payload()


@app.get("/civicboards", response_class=HTMLResponse)
def public_civicboards_page() -> str:
    """Return the public sample board administration support UI."""

    return render_public_lookup_page()


@app.get("/civicboards/staff", response_class=HTMLResponse)
def staff_civicboards_page() -> str:
    """Return the staff board roster and review queue UI."""

    return render_staff_page()


@app.get("/api/v1/civicboards/integration-contracts")
def integration_contracts() -> dict[str, object]:
    """Return suite-visible integration contracts for installer and downstream checks."""

    return {
        "module": "civicboards",
        "version": __version__,
        "contracts": [
            {
                "name": "civicboards.board_roster.v1",
                "endpoint": "/api/v1/civicboards/registry",
                "method": "POST",
                "boundary": "Creates board roster records; it does not appoint or remove members.",
            },
            {
                "name": "civicboards.staff_review_queue.v1",
                "endpoint": "/api/v1/civicboards/staff/reviews",
                "method": "GET",
                "requires_staff_key": True,
                "boundary": "Staff-only queue for board, term, vacancy, and attendance review.",
            },
            {
                "name": "civicboards.notice_packet.v1",
                "endpoint": "/api/v1/civicboards/vacancies",
                "method": "POST",
                "boundary": "Builds vacancy notice checklists; it does not publish official notices.",
            },
            {
                "name": "civicboards.records_export.v1",
                "endpoint": "/api/v1/civicboards/export",
                "method": "POST",
                "boundary": "Builds records export checklists; it does not publish or redact records.",
            },
        ],
        "downstream_ready_for": [
            "civicclerk agenda board appointments",
            "civicnotice public vacancy notices",
            "civicrecords-ai board file retention",
            "civiclegal eligibility review",
        ],
    }


@app.post("/api/v1/civicboards/registry")
def board_registry(request: BoardRegistryRequest) -> dict[str, object]:
    result = _register_board(
        board_id=request.board_id,
        board_name=request.board_name,
        liaison=request.liaison,
    )
    return result.__dict__


@app.get("/api/v1/civicboards/registry/{board_id}")
def get_board_registry(board_id: str) -> dict[str, object]:
    stored = _get_roster_repository().get_board(board_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Board roster record not found.",
                "fix": "Use a board_id returned by POST /api/v1/civicboards/registry.",
            },
        )
    return stored.__dict__


@app.post("/api/v1/civicboards/terms")
def term_plan(request: TermRequest) -> dict[str, object]:
    return build_term_review_plan(
        member_name=request.member_name,
        term_end=request.term_end,
    ).__dict__


@app.post("/api/v1/civicboards/vacancies")
def vacancy_checklist(request: VacancyRequest) -> dict[str, object]:
    return build_vacancy_checklist(
        board_name=request.board_name,
        vacancy_reason=request.vacancy_reason,
    ).__dict__


@app.post("/api/v1/civicboards/attendance")
def attendance_summary(request: AttendanceRequest) -> dict[str, object]:
    result = summarize_attendance(
        member_name=request.member_name,
        meetings_attended=request.meetings_attended,
        meetings_held=request.meetings_held,
    )
    stored = _get_roster_repository().create_attendance_review(
        member_name=request.member_name,
        meetings_attended=request.meetings_attended,
        meetings_held=request.meetings_held,
    )
    response = _stored_attendance_response(stored)
    response["staff_review_required"] = result.staff_review_required
    return response


@app.get("/api/v1/civicboards/attendance/{attendance_id}")
def get_attendance_review(attendance_id: str) -> dict[str, object]:
    stored = _get_roster_repository().get_attendance_review(attendance_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Attendance review record not found.",
                "fix": "Use an attendance_id returned by POST /api/v1/civicboards/attendance.",
            },
        )
    return _stored_attendance_response(stored)


@app.post("/api/v1/civicboards/export")
def records_export(request: RecordsExportRequest) -> dict[str, object]:
    return build_board_records_export(
        board_id=request.board_id,
        title=request.title,
        format=request.format,
    ).__dict__


@app.post("/api/v1/civicboards/staff/reviews")
def create_staff_review(
    request: StaffReviewCreateRequest,
    _staff_principal: object = Depends(_require_staff_key),
) -> dict[str, object]:
    item = _get_roster_repository().create_staff_review_queue_item(
        board_id=request.board_id,
        title=request.title,
        reason=request.reason,
        created_by="staff",
    )
    return _staff_review_payload(item)


@app.get("/api/v1/civicboards/staff/reviews")
def list_staff_reviews(
    status: str | None = None,
    _staff_principal: object = Depends(_require_staff_key),
) -> dict[str, object]:
    return {
        "visibility": "staff_only",
        "items": [
            _staff_review_payload(item)
            for item in _get_roster_repository().list_staff_review_queue_items(status=status)
        ],
    }


def _roster_database_url() -> str:
    configured = os.environ.get("CIVICBOARDS_ROSTER_DB_URL")
    if configured:
        return configured
    data_dir = Path(os.environ.get("CIVICBOARDS_DATA_DIR", Path.cwd() / "data")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite+pysqlite:///{(data_dir / 'civicboards-roster.db').as_posix()}"


def _uses_default_roster_database() -> bool:
    return not os.environ.get("CIVICBOARDS_ROSTER_DB_URL")


def _get_roster_repository() -> BoardRosterRepository:
    global _roster_db_url, _roster_repository
    db_url = _roster_database_url()
    if _roster_repository is None or db_url != _roster_db_url:
        _dispose_roster_repository()
        _roster_db_url = db_url
        _roster_repository = BoardRosterRepository(db_url=db_url)
    return _roster_repository


def _dispose_roster_repository() -> None:
    global _roster_repository
    if _roster_repository is not None:
        _roster_repository.engine.dispose()
        _roster_repository = None


def _register_board(*, board_id: str, board_name: str, liaison: str):
    if _roster_database_url() is None:
        return register_board_stub(
            board_id=board_id,
            board_name=board_name,
            liaison=liaison,
        )
    return _get_roster_repository().register_board(
        board_id=board_id,
        board_name=board_name,
        liaison=liaison,
    )


def _stored_attendance_response(stored: StoredAttendanceReview) -> dict[str, object]:
    return {
        "attendance_id": stored.attendance_id,
        "member_name": stored.member_name,
        "meetings_attended": stored.meetings_attended,
        "meetings_held": stored.meetings_held,
        "attendance_status": stored.attendance_status,
        "review_notes": list(stored.review_notes),
        "staff_review_required": stored.staff_review_required,
        "disclaimer": stored.disclaimer,
        "created_at": stored.created_at.isoformat(),
    }


def _staff_review_payload(item: StaffReviewQueueItem) -> dict[str, object]:
    return {
        "review_id": item.review_id,
        "board_id": item.board_id,
        "title": item.title,
        "reason": item.reason,
        "status": item.status,
        "assigned_to": item.assigned_to,
        "resolution": item.resolution,
        "created_by": item.created_by,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat(),
        "visibility": "staff_only",
        "boundary": (
            "Staff review queues support board administration only; they do not appoint, remove, "
            "replace, or determine eligibility for board members."
        ),
    }


def _readiness_payload() -> dict[str, object]:
    db_url = _roster_database_url()
    repository = _get_roster_repository()
    schema_status = repository.schema_status()
    blockers: list[str] = []
    if not schema_status.ready:
        blockers.append("Initialize the CivicBoards local roster database schema.")
    ready_for_public_use = not blockers
    return {
        "status": "ready" if ready_for_public_use else "not-ready",
        "ready": ready_for_public_use,
        "roster_database_configured": True,
        "roster_database_url": db_url,
        "using_default_local_database": _uses_default_roster_database(),
        "schema_ready": schema_status.ready,
        "schema_version": schema_status.schema_version,
        "expected_schema_version": schema_status.expected_schema_version,
        "blockers": blockers,
    }
