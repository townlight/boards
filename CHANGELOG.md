# Changelog

All notable changes to CivicBoards will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Default local SQLite-backed board roster, attendance review, and staff review queue persistence via `CIVICBOARDS_DATA_DIR`.
- Staff workspace at `/civicboards/staff` plus staff-key protected review queue endpoints.
- Suite integration-contract metadata for CivicClerk board actions, CivicNotice public vacancy notices, CivicRecords retention, and CivicLegal eligibility review.
- CivicCore v1.2.0 release-wheel dependency alignment for staff key gating.

## [0.1.1] - 2026-04-28

### Added

- Optional SQLAlchemy-backed board roster and attendance review records via `CIVICBOARDS_ROSTER_DB_URL`.
- Board roster and attendance review retrieval endpoints for persisted records.

### Changed

- Aligned CivicBoards to `civiccore==0.3.0` for the v0.1.1 compatibility release. Current unreleased work aligns to the published CivicCore v1.2.0 release wheel.
- Updated current-facing docs, release gate, CI wheel install, health/version tests, and browser QA evidence for the v0.1.1 compatibility release.

## [0.1.0] - 2026-04-27

### Added

- FastAPI package/runtime foundation pinned to `civiccore==0.2.0`.
- board registry helper using deterministic sample data.
- term tracking helper with staff-verification boundary.
- vacancy tracking helper with review-required boundary.
- attendance review helper.
- Public-records export checklist for board records.
- Accessible public sample UI at `/civicboards` with browser QA coverage.
- Release gate: tests, docs, placeholder import guard, Ruff, and build artifact checks.

### Not Shipped

- live agenda systems, official appointment decision decisions, legal advice, live LLM calls, meeting system write-back, and board system-of-record integrations.
