# CivicBoards

CivicBoards is the CivicSuite module for board and commission roster support, term tracking, vacancy tracking, attendance review, and notice/records export checklists.

Current state: **v0.1.1 local-first board administration and staff review runtime**. This repo ships a FastAPI package, health/readiness endpoints, documentation gates, deterministic sample board registry, term review plans, vacancy checklists, attendance summaries, default local SQLite-backed board roster and attendance review records, staff-only review queues, CivicClerk/CivicNotice handoff contracts, notice/records export checklist, an accessible public sample UI at `/civicboards`, and a staff workspace at `/civicboards/staff`, aligned to the published CivicCore v1.2.0 release wheel. It does **not** ship live agenda systems, appointment decisions, legal advice, live LLM calls, official notice publication, meeting system write-back, or board system-of-record integrations.

## What CivicBoards Does

- Create sample board and commission registry stubs.
- Build term-end reminder plans.
- Assemble vacancy checklists for staff review.
- Summarize attendance without removing or replacing members.
- Persist board roster, attendance review, and staff review queue records in a default local SQLite database.
- Expose staff-only board review queues protected by `CIVICBOARDS_STAFF_API_KEY`.
- Publish suite integration contracts for CivicClerk appointment workflows, CivicNotice vacancy notices, CivicRecords retention, and CivicLegal eligibility review.
- Produce notice and records export checklists.
- Demonstrate a public board-support UI at `/civicboards`.
- Demonstrate a staff board-review workspace at `/civicboards/staff`.

## What CivicBoards Does Not Do

- It does not appoint, remove, or replace members.
- It does not publish official notices.
- It does not provide legal advice.
- It does not call live LLMs in v0.1.1.
- It does not replace a board system of record.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and CivicCore versions.
- `GET /ready` and `GET /api/v1/civicboards/readiness` return local database/schema readiness.
- `GET /civicboards` returns the accessible public sample UI.
- `GET /civicboards/staff` returns the staff review workspace.
- `GET /api/v1/civicboards/integration-contracts` returns suite integration contracts.
- `POST /api/v1/civicboards/registry` returns a sample board registry stub.
- `GET /api/v1/civicboards/registry/{board_id}` retrieves a persisted board roster record.
- `POST /api/v1/civicboards/terms` returns term-end reminders.
- `POST /api/v1/civicboards/vacancies` returns a vacancy checklist.
- `POST /api/v1/civicboards/attendance` returns attendance review flags and a persisted `attendance_id`.
- `GET /api/v1/civicboards/attendance/{attendance_id}` retrieves a persisted attendance review.
- `POST /api/v1/civicboards/export` returns a notice and records export checklist.
- `GET /api/v1/civicboards/staff/reviews` lists staff-only review items.

## Local Persistence

CivicBoards uses `CIVICBOARDS_DATA_DIR` for its default local SQLite-backed roster database, or `CIVICBOARDS_ROSTER_DB_URL` when IT needs an explicit SQLAlchemy database URL. Staff routes require `CIVICBOARDS_STAFF_API_KEY`, `X-CivicBoards-Role: staff`, and `X-CivicBoards-Staff-Key` matching the configured key.

## Local Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code is Apache License 2.0. Documentation is CC BY 4.0.
