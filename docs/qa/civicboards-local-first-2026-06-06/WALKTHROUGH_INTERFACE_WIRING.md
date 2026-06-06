# CivicBoards local-first walkthrough and interface wiring audit

Date: 2026-06-06
Scope: CivicBoards local-first runtime, public UI, staff UI, API wiring, persistence, and suite integration contracts.

## Result

PASS. No blocker, critical, major, minor, or nit findings were found in this walkthrough.

## Runtime exercised

- Local app: `http://127.0.0.1:18865`
- Runtime data: local SQLite through `CIVICBOARDS_DATA_DIR`
- Screenshots:
  - `desktop-public.png`
  - `desktop-staff.png`
  - `mobile-public.png`
  - `mobile-staff.png`
- API evidence: `api-evidence.json`

## Product model

CivicBoards is a board and commission administration module. It supports roster intake, term and vacancy review helpers, attendance review, staff review queues, public records export context, and suite-visible integration contracts. It explicitly does not appoint or remove board members, publish legal notices, make legal eligibility decisions, or replace the clerk system of record.

## Routes and workflows checked

- `GET /health` returned HTTP 200 with CivicBoards `0.1.1` and CivicCore `1.2.0`.
- `GET /api/v1/civicboards/readiness` returned HTTP 200 with `ready=true`, `schema_ready=true`, and `using_default_local_database=true`.
- `GET /api/v1/civicboards/integration-contracts` returned all required local-first contracts: board roster, staff review queue, notice packet, and records export.
- `GET /civicboards` rendered the public board administration page on desktop and mobile without layout overlap.
- `GET /civicboards/staff` rendered the staff review page on desktop and mobile without layout overlap.
- `POST /api/v1/civicboards/registry` created a board roster record.
- `GET /api/v1/civicboards/registry/{board_id}` retrieved the created roster record.
- `POST /api/v1/civicboards/attendance` created a persisted attendance review and flagged staff review.
- `GET /api/v1/civicboards/attendance/{attendance_id}` retrieved the created attendance record.
- `GET /api/v1/civicboards/staff/reviews` without staff auth returned the expected staff-key configuration error.
- `POST /api/v1/civicboards/export` returned a records export checklist and retention note.

## Wiring verdict

The public UI is conservative and honest about module boundaries. The staff UI exposes the workflows implemented by the backend: board roster creation, attendance review creation, and review queue loading. The API supports local persistence by default, and the readiness endpoint proves the schema is present before the suite can treat the module as ready.

The staff queue is protected by CivicCore `staff_key_gate`; keyed behavior is covered by tests because the walkthrough server intentionally did not expose a staff secret in process startup.

## Evidence-backed source cross-check

- Readiness and integration contracts are implemented in `civicboards/main.py`.
- Staff queue endpoints are implemented in `civicboards/main.py`.
- Default local SQLite pathing is implemented in `civicboards/main.py`.
- Staff review persistence and schema checks are implemented in `civicboards/persistence.py`.
- Attendance reviews auto-queue staff review when review is required in `civicboards/persistence.py`.
- Behavioral tests cover readiness/contracts, staff-key queue access, auto-queued attendance review, and placeholder import guard behavior.

## Test commands

- `python -m pytest -q`: passed, 21 tests.
- `bash scripts/verify-release.sh`: passed, including tests, docs, placeholder import guard, Ruff, and build artifact checks.
- `python -m py_compile civicboards/main.py civicboards/persistence.py civicboards/public_ui.py`: passed.

## Findings

None.
