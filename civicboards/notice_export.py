"""Notice and records export helpers for CivicBoards v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass

from civicboards.board_registry import DISCLAIMER


@dataclass(frozen=True)
class BoardRecordsExport:
    board_id: str
    title: str
    checklist: tuple[str, ...]
    retention_note: str
    disclaimer: str = DISCLAIMER


def build_board_records_export(
    *, board_id: str, title: str, format: str = "markdown"
) -> BoardRecordsExport:
    """Return a public-records-aware board export checklist."""

    checklist = (
        "Preserve agenda, packet, notice, minutes, attendance, roster, and appointment records.",
        "Confirm closed/session-sensitive material is excluded before public release.",
        "Include file hashes, export timestamp, board identifier, and reviewer initials.",
        "Record whether the export is for public portal, records request, or staff archive.",
    )
    return BoardRecordsExport(
        board_id=board_id.strip() or "unassigned-board",
        title=title.strip() or "Board records export",
        checklist=checklist,
        retention_note=f"Export format '{format}' must follow the city's retention schedule.",
    )
