"""Board and commission registry helpers for Townlight Boards v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass


DISCLAIMER = (
    "Townlight Boards supports board and commission administration, but staff remain "
    "responsible for appointments, attendance determinations, notices, minutes, "
    "and statutory compliance."
)


@dataclass(frozen=True)
class BoardRoster:
    board_id: str
    board_name: str
    liaison: str
    roster_notes: tuple[str, ...]
    disclaimer: str = DISCLAIMER


def register_board_stub(*, board_id: str, board_name: str, liaison: str) -> BoardRoster:
    """Return a deterministic board registry stub for staff review."""

    notes = (
        "Confirm enabling authority, appointment body, term length, quorum rule, and vacancy rule.",
        "Attach member roster, terms, liaison contact, public page link, and adopted bylaws if available.",
        "Route agendas, packets, minutes, attendance, and notices through staff-owned review.",
    )
    return BoardRoster(
        board_id=board_id.strip() or "unassigned-board",
        board_name=board_name.strip() or "Unnamed board",
        liaison=liaison.strip() or "Unassigned liaison",
        roster_notes=notes,
    )
