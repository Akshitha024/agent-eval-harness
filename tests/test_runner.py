"""End-to-end runner smoke test."""

from __future__ import annotations

from pathlib import Path

from aeh.runner import run


def test_runner_smoke(tmp_path: Path) -> None:
    s = run(tmp_path / "out", n=20, seed=1)
    assert s["n_traj"] == 20
    assert (tmp_path / "out" / "summary.json").exists()
