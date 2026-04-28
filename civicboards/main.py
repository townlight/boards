"""FastAPI runtime foundation for CivicBoards."""

from datetime import date

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicboards import __version__
from civicboards.attendance_tracker import summarize_attendance
from civicboards.board_registry import register_board_stub
from civicboards.notice_export import build_board_records_export
from civicboards.public_ui import render_public_lookup_page
from civicboards.term_tracker import build_term_review_plan
from civicboards.vacancy_tracker import build_vacancy_checklist


app = FastAPI(
    title="CivicBoards",
    version=__version__,
    description="Board and commission roster, terms, vacancies, attendance, notices, and records-export support for CivicSuite.",
)


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
        "status": "board administration foundation",
        "message": (
            "CivicBoards package, API foundation, sample board registry, term tracking, "
            "vacancy checklist, attendance summary, records export checklist, and public UI "
            "foundation are online; live agenda systems, appointment decisions, legal advice, "
            "live LLM calls, meeting system write-back, and board system-of-record integrations "
            "are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: CivicClerk agenda handoff, public vacancy pages, and staff review queues",
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
    return register_board_stub(
        board_id=request.board_id,
        board_name=request.board_name,
        liaison=request.liaison,
    ).__dict__


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
    return summarize_attendance(
        member_name=request.member_name,
        meetings_attended=request.meetings_attended,
        meetings_held=request.meetings_held,
    ).__dict__


@app.post("/api/v1/civicboards/export")
def records_export(request: RecordsExportRequest) -> dict[str, object]:
    return build_board_records_export(
        board_id=request.board_id,
        title=request.title,
        format=request.format,
    ).__dict__
