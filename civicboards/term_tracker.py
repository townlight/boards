"""Term tracking helpers for Townlight Boards v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from civicboards.board_registry import DISCLAIMER


@dataclass(frozen=True)
class TermReviewPlan:
    member_name: str
    term_end: date
    reminders: tuple[str, ...]
    staff_review_required: bool
    disclaimer: str = DISCLAIMER


def build_term_review_plan(*, member_name: str, term_end: date) -> TermReviewPlan:
    """Build deterministic term-end reminders without deciding reappointment."""

    reminders = (
        f"{term_end - timedelta(days=120)}: confirm eligibility and appointing authority.",
        f"{term_end - timedelta(days=90)}: notify liaison and clerk of upcoming term end.",
        f"{term_end - timedelta(days=60)}: prepare vacancy/reappointment agenda item if needed.",
        f"{term_end - timedelta(days=30)}: confirm public notice and roster update timing.",
    )
    return TermReviewPlan(
        member_name=member_name.strip() or "Unnamed member",
        term_end=term_end,
        reminders=reminders,
        staff_review_required=True,
    )
