# Changelog

All notable changes to CivicBoards will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.1] - 2026-04-28

### Changed

- Aligned CivicBoards to `civiccore==0.3.0`.
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
