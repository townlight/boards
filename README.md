## Windows 1.8.2.1 maintenance release

Windows 1.8.2.1 packages the staff authorization, explicit database configuration and component metadata corrections. Its exact signed installed checks cover setup, the 1.8.1.1 upgrade, saved staff records, procurement/Contracts handoffs, backup/restore and uninstall retention. Unchanged module and 31-source/34-format import evidence remains attributed to the earlier build that produced it; this is not a new exhaustive test of every module or live provider.

Windows 1.8.2.1 has signed installed acceptance for fresh setup and an in-place upgrade from Windows 1.8.1.1. Before upgrading, back up city data and settings, close Townlight, run the signed MSI, and reopen it under the same Windows account with the existing `%LOCALAPPDATA%\CivicSuite` profile. Keep the prior installer and a restore path. Other upgrade paths are unverified. Station uses its separately configured service. The acceptance summary distinguishes new maintenance checks from reused workflow evidence.

[Release and downloads](https://github.com/townlight/townlight/releases/tag/townlight-windows-v1.8.2.1) · [Acceptance and limits](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.2.1/ACCEPTANCE-Windows-1.8.2.1.md).

<a id="townlight_boards"></a>

# Townlight Boards

## Shared meeting imports · Windows 1.8.1.1

Windows 1.8.1.1 adds shared meeting imports for 31 source families, with 34 supported source/format pairs. Installed Windows Sandbox checks exercised preview, save and durable readback using public captures and fixtures, plus the documented Townlight handoffs. These checks do not establish automatic discovery on every live portal or a complete retest of every module.

[All 31 sources, formats and handoffs](https://townlight.github.io/manuals/meeting-imports.html) · [Installed acceptance](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.1.1/ACCEPTANCE-Windows-1.8.1.1.md).

Windows 1.8.2.1 has signed installed acceptance for fresh setup and an in-place upgrade from Windows 1.8.1.1. Before upgrading, back up city data and settings, close Townlight, run the signed MSI, and reopen it under the same Windows account with the existing `%LOCALAPPDATA%\CivicSuite` profile. Keep the prior installer and a restore path. Other upgrade paths are unverified. Station uses its separately configured service. The acceptance summary distinguishes new maintenance checks from reused workflow evidence.

Windows 1.8.2.1 contains Townlight Runtime 0.3.2 and Meetings 1.0.6. Its current component sources and installed evidence are identified in the maintenance acceptance summary.


Townlight Boards is the Townlight module for board and commission roster support, term tracking, vacancy tracking, attendance review, and notice/records export checklists.

## In the Windows suite

Maintain board rosters, vacancies, terms, and attendance linked to existing Meetings records. Install the [signed Townlight Windows beta 1.8.1.1](https://github.com/townlight/townlight/releases/tag/townlight-windows-v1.8.1.1) and select the full profile. See the [staff operating guide](https://townlight.github.io/manuals/windows-staff-workflows.html#boards). The package examples below describe the standalone development interface.

Current state: **v0.2.1 board administration foundation plus roster persistence release**. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic sample board registry, term review plans, vacancy checklists, attendance summaries, optional database-backed board roster and attendance review records, notice/records export checklist, and accessible public sample UI at `/townlight_boards`, aligned to `townlight-core==1.3.0.dev2`. It does **not** ship live agenda systems, appointment decisions, legal advice, live LLM calls, official notice publication, meeting system write-back, or board system-of-record integrations.

<a id="what-townlight_boards-does"></a>

## What Townlight Boards Does

- Create sample board and commission registry stubs.
- Build term-end reminder plans.
- Assemble vacancy checklists for staff review.
- Summarize attendance without removing or replacing members.
- Persist board roster and attendance review records when `TOWNLIGHT_BOARDS_ROSTER_DB_URL` is configured.
- Produce notice and records export checklists.
- Demonstrate a public board-support UI at `/townlight_boards`.

<a id="what-townlight_boards-does-not-do"></a>

## What Townlight Boards Does Not Do

- It does not appoint, remove, or replace members.
- It does not publish official notices.
- It does not provide legal advice.
- It does not call live LLMs in v0.2.1.
- It does not replace a board system of record.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and Townlight Core versions.
- `GET /townlight_boards` returns the accessible public sample UI.
- `POST /api/v1/townlight_boards/registry` returns a sample board registry stub.
- `GET /api/v1/townlight_boards/registry/{board_id}` retrieves a persisted board roster record when `TOWNLIGHT_BOARDS_ROSTER_DB_URL` is configured.
- `POST /api/v1/townlight_boards/terms` returns term-end reminders.
- `POST /api/v1/townlight_boards/vacancies` returns a vacancy checklist.
- `POST /api/v1/townlight_boards/attendance` returns attendance review flags and an `attendance_id` when persistence is configured.
- `GET /api/v1/townlight_boards/attendance/{attendance_id}` retrieves a persisted attendance review when `TOWNLIGHT_BOARDS_ROSTER_DB_URL` is configured.
- `POST /api/v1/townlight_boards/export` returns a notice and records export checklist.

## Optional Persistence

Set `TOWNLIGHT_BOARDS_ROSTER_DB_URL` to enable local SQLAlchemy-backed board roster and attendance review records:

```bash
export TOWNLIGHT_BOARDS_ROSTER_DB_URL="sqlite+pysqlite:///./townlight_boards.db"
```

Without that variable, Townlight Boards remains deterministic and stateless. Retrieval endpoints return actionable `503` responses that name the required configuration.

## Local Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code: AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying deployments. See [LICENSE](LICENSE) and [LICENSE-EXCEPTION.md](LICENSE-EXCEPTION.md).
Documentation is CC BY 4.0.

## Standalone staff API authentication — unreleased source correction

The standalone `/api/v1/townlight_boards/` endpoints require `X-Townlight-Boards-Role: staff` and `X-Townlight-Boards-Staff-Key: <configured secret>`. Set `TOWNLIGHT_BOARDS_STAFF_API_KEY` in the service environment; never place the secret in URLs or public examples. Missing configuration returns 503; missing, invalid or non-staff credentials return 403. Health and the deterministic sample page remain public. This reuses Core's staff-key contract and is not individual staff-account administration.

The installed Windows suite uses its existing named staff sessions and role checks through `municipal_staff.py`, rather than this standalone API. This source correction is not present in the unchanged Windows 1.8.1.1 MSI.
