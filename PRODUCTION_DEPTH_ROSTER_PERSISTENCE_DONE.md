# Production Depth: Board Roster Persistence

## Summary

CivicBoards now supports optional SQLAlchemy-backed board roster and attendance review records through `CIVICBOARDS_ROSTER_DB_URL`.

## Shipped

- `BoardRosterRepository` with schema-aware SQLAlchemy tables.
- Seeded sample board records.
- Persisted board registry records.
- Persisted attendance review records with `attendance_id`.
- Retrieval endpoints:
  - `GET /api/v1/civicboards/registry/{board_id}`
  - `GET /api/v1/civicboards/attendance/{attendance_id}`
- Actionable `503` guidance when persistence is not configured.
- Regression tests for repository reload, API round trip, missing-record `404`, no-config `503`, and stateless fallback behavior.

## Still Not Shipped

- Live agenda systems.
- Appointment decisions.
- Legal advice.
- Live LLM calls.
- Official notice publication.
- Meeting system write-back.
- Board system-of-record integrations.

## Verification

Run before merge:

```bash
python -m pytest --collect-only -q
python -m pytest -q
bash scripts/verify-docs.sh
python scripts/check-civiccore-placeholder-imports.py
python -m ruff check .
bash scripts/verify-release.sh
git diff --check
```
