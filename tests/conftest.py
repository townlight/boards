from __future__ import annotations

import pytest

import civicboards.main as main_module


@pytest.fixture(autouse=True)
def isolated_civicboards_runtime_data(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Keep default local-first runtime data isolated per test."""

    monkeypatch.setenv("CIVICBOARDS_DATA_DIR", str(tmp_path / "runtime-data"))
    yield
    main_module._dispose_roster_repository()
    main_module._roster_db_url = None
