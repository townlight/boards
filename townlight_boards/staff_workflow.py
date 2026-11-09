"""Staff-maintained board roster and attendance storage for the desktop suite."""
from datetime import date
from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from pydantic import BaseModel, ConfigDict, Field, model_validator

from townlight_boards.persistence import board_roster_records, metadata

ShortText = Annotated[str, Field(min_length=1, max_length=255)]

seats = sa.Table(
    "staff_seats", metadata,
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("board_id", sa.String(160), sa.ForeignKey(board_roster_records.c.board_id), nullable=False),
    sa.Column("seat_name", sa.String(255), nullable=False),
    sa.Column("member_name", sa.String(255)),
    sa.Column("term_start", sa.Date),
    sa.Column("term_end", sa.Date),
    sa.UniqueConstraint("board_id", "seat_name"),
    schema=board_roster_records.schema,
)

attendance = sa.Table(
    "staff_meeting_attendance", metadata,
    sa.Column("seat_id", sa.Uuid, sa.ForeignKey(seats.c.id), primary_key=True),
    sa.Column("meeting_id", sa.Uuid, primary_key=True),
    sa.Column("member_name", sa.String(255), nullable=False),
    sa.Column("present", sa.Boolean, nullable=False),
    schema=board_roster_records.schema,
)


class BoardInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    board_name: ShortText
    liaison: ShortText


class SeatInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    board_id: UUID
    seat_name: ShortText
    member_name: ShortText | None = None
    term_start: date | None = None
    term_end: date | None = None

    @model_validator(mode="after")
    def validate_appointment(self):
        if self.member_name is None:
            if self.term_start or self.term_end:
                raise ValueError("A vacant seat cannot have appointment dates.")
        elif not self.term_start or not self.term_end or self.term_end < self.term_start:
            raise ValueError("An appointment needs term dates in chronological order.")
        return self


class AttendanceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seat_id: UUID
    meeting_id: UUID
    present: bool


def seat_status(member_name: str | None, term_end: date | None, today: date) -> str:
    if member_name is None:
        return "Vacant"
    if term_end is None:
        return "Appointed"
    remaining = (term_end - today).days
    if remaining < 0:
        return "Term expired"
    if remaining <= 90:
        return "Term expires within 90 days"
    return "Appointed"
