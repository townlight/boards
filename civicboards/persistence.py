from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicboards.attendance_tracker import summarize_attendance
from civicboards.board_registry import BoardRoster, register_board_stub


metadata = sa.MetaData()

board_roster_records = sa.Table(
    "board_roster_records",
    metadata,
    sa.Column("board_id", sa.String(160), primary_key=True),
    sa.Column("board_name", sa.String(500), nullable=False),
    sa.Column("liaison", sa.String(255), nullable=False),
    sa.Column("roster_notes", sa.JSON(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicboards",
)

attendance_review_records = sa.Table(
    "attendance_review_records",
    metadata,
    sa.Column("attendance_id", sa.String(36), primary_key=True),
    sa.Column("member_name", sa.String(255), nullable=False),
    sa.Column("meetings_attended", sa.Integer(), nullable=False),
    sa.Column("meetings_held", sa.Integer(), nullable=False),
    sa.Column("attendance_status", sa.String(120), nullable=False),
    sa.Column("review_notes", sa.JSON(), nullable=False),
    sa.Column("staff_review_required", sa.Boolean(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicboards",
)

staff_review_queue_records = sa.Table(
    "staff_review_queue_records",
    metadata,
    sa.Column("review_id", sa.String(36), primary_key=True),
    sa.Column("board_id", sa.String(160), nullable=False),
    sa.Column("title", sa.String(500), nullable=False),
    sa.Column("reason", sa.Text(), nullable=False),
    sa.Column("status", sa.String(120), nullable=False),
    sa.Column("assigned_to", sa.String(255), nullable=True),
    sa.Column("resolution", sa.Text(), nullable=True),
    sa.Column("created_by", sa.String(160), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicboards",
)


@dataclass(frozen=True)
class SchemaStatus:
    ready: bool
    schema_version: str
    expected_schema_version: str


@dataclass(frozen=True)
class StoredAttendanceReview:
    attendance_id: str
    member_name: str
    meetings_attended: int
    meetings_held: int
    attendance_status: str
    review_notes: tuple[str, ...]
    staff_review_required: bool
    disclaimer: str
    created_at: datetime


@dataclass(frozen=True)
class StaffReviewQueueItem:
    review_id: str
    board_id: str
    title: str
    reason: str
    status: str
    assigned_to: str | None
    resolution: str | None
    created_by: str
    created_at: datetime
    updated_at: datetime


class BoardRosterRepository:
    """SQLAlchemy-backed board roster and attendance-review records."""

    expected_schema_version = "civicboards-local-first-v1"

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None, seed_defaults: bool = True) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civicboards": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicboards"))
        metadata.create_all(self.engine)
        if seed_defaults:
            self.seed_sample_boards()

    def schema_status(self) -> SchemaStatus:
        try:
            with self.engine.begin() as connection:
                for table in (
                    board_roster_records,
                    attendance_review_records,
                    staff_review_queue_records,
                ):
                    connection.execute(sa.select(sa.func.count()).select_from(table)).scalar_one()
        except Exception:
            return SchemaStatus(
                ready=False,
                schema_version="unavailable",
                expected_schema_version=self.expected_schema_version,
            )
        return SchemaStatus(
            ready=True,
            schema_version=self.expected_schema_version,
            expected_schema_version=self.expected_schema_version,
        )

    def seed_sample_boards(self) -> None:
        samples = (
            {
                "board_id": "pc-001",
                "board_name": "Planning Commission",
                "liaison": "clerk@example.gov",
            },
            {
                "board_id": "lib-001",
                "board_name": "Library Board",
                "liaison": "library@example.gov",
            },
        )
        for sample in samples:
            self.register_board(
                board_id=sample["board_id"],
                board_name=sample["board_name"],
                liaison=sample["liaison"],
            )

    def register_board(self, *, board_id: str, board_name: str, liaison: str) -> BoardRoster:
        roster = register_board_stub(board_id=board_id, board_name=board_name, liaison=liaison)
        now = datetime.now(UTC)
        with self.engine.begin() as connection:
            exists = connection.execute(
                sa.select(board_roster_records.c.board_id).where(
                    board_roster_records.c.board_id == roster.board_id
                )
            ).first()
            values = {
                "board_id": roster.board_id,
                "board_name": roster.board_name,
                "liaison": roster.liaison,
                "roster_notes": list(roster.roster_notes),
                "disclaimer": roster.disclaimer,
                "updated_at": now,
            }
            if exists is None:
                connection.execute(
                    board_roster_records.insert().values(
                        **values,
                        created_at=now,
                    )
                )
            else:
                connection.execute(
                    board_roster_records.update()
                    .where(board_roster_records.c.board_id == roster.board_id)
                    .values(**values)
                )
        return roster

    def get_board(self, board_id: str) -> BoardRoster | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(board_roster_records).where(board_roster_records.c.board_id == board_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_board(row)

    def create_attendance_review(
        self,
        *,
        member_name: str,
        meetings_attended: int,
        meetings_held: int,
    ) -> StoredAttendanceReview:
        summary = summarize_attendance(
            member_name=member_name,
            meetings_attended=meetings_attended,
            meetings_held=meetings_held,
        )
        stored = StoredAttendanceReview(
            attendance_id=str(uuid4()),
            member_name=summary.member_name,
            meetings_attended=meetings_attended,
            meetings_held=meetings_held,
            attendance_status=summary.attendance_status,
            review_notes=summary.review_notes,
            staff_review_required=summary.staff_review_required,
            disclaimer=summary.disclaimer,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                attendance_review_records.insert().values(
                    attendance_id=stored.attendance_id,
                    member_name=stored.member_name,
                    meetings_attended=stored.meetings_attended,
                    meetings_held=stored.meetings_held,
                    attendance_status=stored.attendance_status,
                    review_notes=list(stored.review_notes),
                    staff_review_required=stored.staff_review_required,
                    disclaimer=stored.disclaimer,
                    created_at=stored.created_at,
                )
            )
        if stored.staff_review_required:
            self.create_staff_review_queue_item(
                board_id="attendance-review",
                title=f"Attendance review: {stored.member_name}",
                reason="Attendance summary requires staff review before vacancy, removal, or appointment action.",
                created_by="system",
            )
        return stored

    def get_attendance_review(self, attendance_id: str) -> StoredAttendanceReview | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(attendance_review_records).where(
                    attendance_review_records.c.attendance_id == attendance_id
                )
            ).mappings().first()
        if row is None:
            return None
        return _row_to_attendance(row)

    def create_staff_review_queue_item(
        self,
        *,
        board_id: str,
        title: str,
        reason: str,
        created_by: str = "staff",
    ) -> StaffReviewQueueItem:
        now = datetime.now(UTC)
        item = StaffReviewQueueItem(
            review_id=str(uuid4()),
            board_id=board_id.strip() or "unassigned-board",
            title=title.strip() or "Untitled board review",
            reason=reason.strip() or "Board staff review required.",
            status="open",
            assigned_to=None,
            resolution=None,
            created_by=created_by.strip() or "staff",
            created_at=now,
            updated_at=now,
        )
        with self.engine.begin() as connection:
            connection.execute(
                staff_review_queue_records.insert().values(
                    review_id=item.review_id,
                    board_id=item.board_id,
                    title=item.title,
                    reason=item.reason,
                    status=item.status,
                    assigned_to=item.assigned_to,
                    resolution=item.resolution,
                    created_by=item.created_by,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                )
            )
        return item

    def list_staff_review_queue_items(self, status: str | None = None) -> list[StaffReviewQueueItem]:
        query = sa.select(staff_review_queue_records).order_by(
            staff_review_queue_records.c.updated_at.desc()
        )
        if status:
            query = query.where(staff_review_queue_records.c.status == status)
        with self.engine.begin() as connection:
            rows = connection.execute(query).mappings().all()
        return [_row_to_staff_review(row) for row in rows]


def _row_to_board(row: object) -> BoardRoster:
    data = dict(row)
    return BoardRoster(
        board_id=data["board_id"],
        board_name=data["board_name"],
        liaison=data["liaison"],
        roster_notes=tuple(data["roster_notes"]),
        disclaimer=data["disclaimer"],
    )


def _row_to_attendance(row: object) -> StoredAttendanceReview:
    data = dict(row)
    return StoredAttendanceReview(
        attendance_id=data["attendance_id"],
        member_name=data["member_name"],
        meetings_attended=data["meetings_attended"],
        meetings_held=data["meetings_held"],
        attendance_status=data["attendance_status"],
        review_notes=tuple(data["review_notes"]),
        staff_review_required=data["staff_review_required"],
        disclaimer=data["disclaimer"],
        created_at=data["created_at"],
    )


def _row_to_staff_review(row: object) -> StaffReviewQueueItem:
    data = dict(row)
    return StaffReviewQueueItem(
        review_id=data["review_id"],
        board_id=data["board_id"],
        title=data["title"],
        reason=data["reason"],
        status=data["status"],
        assigned_to=data["assigned_to"],
        resolution=data["resolution"],
        created_by=data["created_by"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )
