"""FastAPI runtime foundation for Townlight Boards."""

import os
from datetime import date

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicboards import __version__
from civicboards.attendance_tracker import summarize_attendance
from civicboards.board_registry import register_board_stub
from civicboards.notice_export import build_board_records_export
from civicboards.persistence import BoardRosterRepository, StoredAttendanceReview
from civicboards.public_ui import render_public_lookup_page
from civicboards.term_tracker import build_term_review_plan
from civicboards.vacancy_tracker import build_vacancy_checklist


app = FastAPI(
    title='Townlight Boards',
    version=__version__,
    description='Board and commission roster, terms, vacancies, attendance, notices, and records-export support for Townlight.',
)

_roster_repository: BoardRosterRepository | None = None
_roster_db_url: str | None = None


class BoardRegistryRequest(BaseModel):
    board_id: str
    board_name: str
    liaison: str


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


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicBoards",
        "version": __version__,
        "status": "board administration foundation plus roster persistence",
        "message": (
            "Townlight Boards package, API foundation, sample board registry, term tracking, "
            "vacancy checklist, attendance summary, optional database-backed board roster and attendance "
            "review records, records export checklist, and public UI foundation are online; live agenda "
            "systems, appointment decisions, legal advice, live LLM calls, meeting system write-back, "
            "and board system-of-record integrations are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: Townlight Meetings agenda handoff, public vacancy pages, and staff review queues",
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


@app.get("/civicboards", response_class=HTMLResponse)
def public_civicboards_page() -> str:
    """Return the public sample board administration support UI."""

    return render_public_lookup_page()


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
    if _roster_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Boards roster persistence is not configured.",
                "fix": "Set CIVICBOARDS_ROSTER_DB_URL to retrieve persisted board roster records.",
            },
        )
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
    if _roster_database_url() is not None:
        stored = _get_roster_repository().create_attendance_review(
            member_name=request.member_name,
            meetings_attended=request.meetings_attended,
            meetings_held=request.meetings_held,
        )
        return _stored_attendance_response(stored)

    result = summarize_attendance(
        member_name=request.member_name,
        meetings_attended=request.meetings_attended,
        meetings_held=request.meetings_held,
    )
    payload = result.__dict__
    payload["attendance_id"] = None
    return payload


@app.get("/api/v1/civicboards/attendance/{attendance_id}")
def get_attendance_review(attendance_id: str) -> dict[str, object]:
    if _roster_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Boards roster persistence is not configured.",
                "fix": "Set CIVICBOARDS_ROSTER_DB_URL to retrieve persisted attendance review records.",
            },
        )
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


def _roster_database_url() -> str | None:
    return os.environ.get("CIVICBOARDS_ROSTER_DB_URL")


def _get_roster_repository() -> BoardRosterRepository:
    global _roster_db_url, _roster_repository
    db_url = _roster_database_url()
    if db_url is None:
        raise RuntimeError("CIVICBOARDS_ROSTER_DB_URL is not configured.")
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
