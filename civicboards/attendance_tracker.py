"""Attendance tracking helpers for Townlight Boards v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass

from civicboards.board_registry import DISCLAIMER


@dataclass(frozen=True)
class AttendanceSummary:
    member_name: str
    attendance_status: str
    review_notes: tuple[str, ...]
    staff_review_required: bool
    disclaimer: str = DISCLAIMER


def summarize_attendance(
    *, member_name: str, meetings_attended: int, meetings_held: int
) -> AttendanceSummary:
    """Summarize attendance without making removal or eligibility determinations."""

    if meetings_held <= 0:
        rate = 0.0
    else:
        rate = meetings_attended / meetings_held
    status = "review-required" if rate < 0.75 else "on-track"
    notes = (
        f"Attendance rate: {meetings_attended}/{meetings_held}.",
        "Staff must verify excused absences, resignation rules, and removal thresholds.",
        "Do not remove or replace a member without clerk/legal review.",
    )
    return AttendanceSummary(
        member_name=member_name.strip() or "Unnamed member",
        attendance_status=status,
        review_notes=notes,
        staff_review_required=status == "review-required",
    )
