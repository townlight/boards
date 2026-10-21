<a id="civicboards-agent-board"></a>

# Townlight Boards Agent Board

## Source of Truth

- Upstream suite spec: `townlight/townlight/docs/CivicSuiteUnifiedSpec.md`, especially the Townlight Boards catalog entry and suite-wide non-negotiables.
- Townlight Boards supports central board registry stubs, term tracking, vacancy tracking, attendance review, and public-records-aware export checklists.
- Staff own every decision.

## Hard Boundaries

- Townlight Boards never appoints members, removes members, publishes official notices, provides legal advice, writes back to meeting systems, or updates a board system of record.
- Townlight Boards v0.1.1 must not call live LLMs or live agenda systems.
- Term tracking, vacancy tracking, attendance review, and records exports must be marked staff-review-required where applicable.
- Townlight Boards depends on Townlight Core; Townlight Core must never depend on Townlight Boards.
- Townlight Boards may reference Townlight Meetings meeting concepts only through released APIs or deterministic sample data in v0.1.1.

## Verification

Run `bash scripts/verify-release.sh` before every push or release.
