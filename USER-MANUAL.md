<a id="townlight_boards-user-manual"></a>

# Townlight Boards User Manual

## For Non-Technical Users

Townlight Boards helps city staff keep board and commission rosters, member terms, vacancy workflows, attendance review notes, meeting records, public notice context, and export manifests organized. It can create a sample board registry stub, build term reminders, assemble vacancy checklists, summarize attendance review, and assemble a notice/records export checklist.

Current state: `0.2.0` board administration foundation plus roster persistence release. Townlight Boards can optionally save board roster and attendance review records when IT configures `TOWNLIGHT_BOARDS_ROSTER_DB_URL`. Townlight Boards does not appoint members, remove members, publish official notices, provide legal advice, call live LLMs, write back to meeting systems, or update a board system of record. Staff own every decision.

## For IT and Technical Staff

Townlight Boards is a FastAPI Python package pinned to `townlight-core==1.3.0.dev2`. The current runtime exposes:

- `GET /`
- `GET /health`
- `GET /townlight_boards`
- `POST /api/v1/townlight_boards/registry`
- `GET /api/v1/townlight_boards/registry/{board_id}`
- `POST /api/v1/townlight_boards/terms`
- `POST /api/v1/townlight_boards/vacancies`
- `POST /api/v1/townlight_boards/attendance`
- `GET /api/v1/townlight_boards/attendance/{attendance_id}`
- `POST /api/v1/townlight_boards/export`

Run:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

Set `TOWNLIGHT_BOARDS_ROSTER_DB_URL` to enable local SQLAlchemy-backed board roster and attendance review records. If the variable is not set, Townlight Boards keeps deterministic stateless behavior and retrieval endpoints return actionable configuration guidance.

## Architecture

```mermaid
flowchart LR
  Staff["Clerk / board liaison / commission staff"] --> Townlight Boards["Townlight Boards"]
  Townlight Boards --> CivicCore["Townlight Core 1.3.0.dev2"]
  Townlight Boards -. future handoff .-> CivicClerk["CivicClerk v0.1.0"]
  Townlight Boards --> Export["Notice and records export checklist"]
```

Townlight Boards depends on Townlight Core. Townlight Core does not depend on Townlight Boards. Townlight Boards v0.2.0 uses deterministic sample board and commission data plus optional local roster persistence; live agenda systems, appointment decisions, legal advice, official notice publication, meeting system write-back, and production board-system integrations are future work.

## Upgrading standalone PostgreSQL data

Stop the old service and back up its PostgreSQL database. In the same database,
verify that the old schema exists and the new schema does not. As the schema
owner, run the following in a transaction, then start the upgraded service
and check that existing records are present. The operation keeps the tables
and data in the same database. SQLite files require no schema rename.

```sql
BEGIN;
ALTER SCHEMA civicboards RENAME TO townlight_boards;
COMMIT;
```
