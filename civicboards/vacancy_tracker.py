"""Vacancy tracking helpers for Townlight Boards v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass

from civicboards.board_registry import DISCLAIMER


@dataclass(frozen=True)
class VacancyChecklist:
    board_name: str
    vacancy_reason: str
    checklist: tuple[str, ...]
    public_notice_required: bool
    disclaimer: str = DISCLAIMER


def build_vacancy_checklist(*, board_name: str, vacancy_reason: str) -> VacancyChecklist:
    """Return a staff-owned vacancy checklist."""

    reason = vacancy_reason.strip() or "unspecified"
    items = (
        "Confirm vacancy date, seat number, term end, and appointing authority.",
        "Check bylaws and state/local notice requirements before publication.",
        "Prepare application window, public page update, and agenda item for appointment.",
        "Preserve resignation, eligibility review, applications, and appointment record.",
    )
    return VacancyChecklist(
        board_name=board_name.strip() or "Unnamed board",
        vacancy_reason=reason,
        checklist=items,
        public_notice_required=True,
    )
