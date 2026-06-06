"""Tests for the trajectory diff."""

from __future__ import annotations

from aeh.diff.trajectory_diff import diff
from aeh.types import Step, Trajectory


def test_identical_trajectories_show_no_changes() -> None:
    a = Trajectory(tid="t", steps=[Step(idx=0, tool="x"), Step(idx=1, tool="y")])
    b = a.model_copy()
    d = diff(a, b)
    assert d.same_n_steps
    assert d.n_step_changes == 0
    assert d.n_tool_changes == 0


def test_changed_tool_shows_step_change() -> None:
    a = Trajectory(tid="t", steps=[Step(idx=0, tool="x"), Step(idx=1, tool="y")])
    b = Trajectory(tid="t", steps=[Step(idx=0, tool="x"), Step(idx=1, tool="z")])
    d = diff(a, b)
    assert d.n_step_changes == 1
    assert "z" in d.tools_added
    assert "y" in d.tools_removed
