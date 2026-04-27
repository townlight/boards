# CivicBoards Agent Board

## Source of Truth

- Upstream suite spec: `CivicSuite/civicsuite/docs/CivicSuiteUnifiedSpec.md`, especially the CivicBoards catalog entry and suite-wide non-negotiables.
- CivicBoards supports central board registry stubs, term tracking, vacancy tracking, attendance review, and public-records-aware export checklists.
- Staff own every decision.

## Hard Boundaries

- CivicBoards never appoints members, removes members, publishes official notices, provides legal advice, writes back to meeting systems, or updates a board system of record.
- CivicBoards v0.1.0 must not call live LLMs or live agenda systems.
- Term tracking, vacancy tracking, attendance review, and records exports must be marked staff-review-required where applicable.
- CivicBoards depends on CivicCore; CivicCore must never depend on CivicBoards.
- CivicBoards may reference CivicClerk meeting concepts only through released APIs or deterministic sample data in v0.1.0.

## Verification

Run `bash scripts/verify-release.sh` before every push or release.
