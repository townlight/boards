# CivicBoards

CivicBoards is the CivicSuite module for board and commission roster support, term tracking, vacancy tracking, attendance review, and notice/records export checklists.

Current state: v0.1.1 board administration foundation release. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic sample board registry, term review plans, vacancy checklists, attendance summaries, notice/records export checklist, and accessible public sample UI at /civicboards, aligned to civiccore==0.3.0. It does not ship live agenda systems, appointment decisions, legal advice, live LLM calls, official notice publication, meeting system write-back, or board system-of-record integrations.

## What CivicBoards Does

- Create sample board and commission registry stubs.
- Build term-end reminder plans.
- Assemble vacancy checklists for staff review.
- Summarize attendance without removing or replacing members.
- Produce notice and records export checklists.
- Demonstrate a public board-support UI at /civicboards.

## What CivicBoards Does Not Do

- It does not appoint, remove, or replace members.
- It does not publish official notices.
- It does not provide legal advice.
- It does not call live LLMs in v0.1.1.
- It does not replace a board system of record.

## API Surface

- GET / returns the shipped/planned boundary.
- GET /health returns package and CivicCore versions.
- GET /civicboards returns the accessible public sample UI.
- POST /api/v1/civicboards/registry returns a sample board registry stub.
- POST /api/v1/civicboards/terms returns term-end reminders.
- POST /api/v1/civicboards/vacancies returns a vacancy checklist.
- POST /api/v1/civicboards/attendance returns attendance review flags.
- POST /api/v1/civicboards/export returns a notice and records export checklist.

## Local Development

bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh


## License

Code is Apache License 2.0. Documentation is CC BY 4.0.
