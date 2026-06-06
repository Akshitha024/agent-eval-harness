"""Tests for the judge council."""

from __future__ import annotations

from aeh.judges.council import (
    DEFAULT_COUNCIL,
    final_answer_judge,
    length_judge,
    run_council,
    tool_diversity_judge,
)
from aeh.types import Step, Trajectory


def _traj(n_steps: int, tools: list[str] | None = None) -> Trajectory:
    return Trajectory(
        tid="t",
        steps=[Step(idx=i, tool=(tools[i] if tools else f"t{i}")) for i in range(n_steps)],
        final_answer="a",
    )


def test_length_judge_short_is_one() -> None:
    assert length_judge(_traj(3)).score == 1.0


def test_length_judge_long_is_zero() -> None:
    assert length_judge(_traj(12)).score == 0.0


def test_diversity_judge_unique_is_one() -> None:
    assert tool_diversity_judge(_traj(4)).score == 1.0


def test_diversity_judge_all_same_is_low() -> None:
    assert tool_diversity_judge(_traj(4, ["x", "x", "x", "x"])).score < 0.5


def test_final_answer_judge() -> None:
    t = _traj(3)
    t.final_answer = ""
    assert final_answer_judge(t).score == 0.0
    t.final_answer = "yes"
    assert final_answer_judge(t).score == 1.0


def test_council_returns_mean() -> None:
    t = _traj(3)
    c = run_council(t, DEFAULT_COUNCIL)
    assert 0 <= c.mean_score <= 1
    assert len(c.verdicts) == 3
