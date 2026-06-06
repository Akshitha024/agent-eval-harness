"""Replay a trajectory by re-executing each step against a deterministic tool table."""

from __future__ import annotations

from collections.abc import Callable

from aeh.types import Trajectory

ToolFn = Callable[[str], str]


def replay(traj: Trajectory, tools: dict[str, ToolFn]) -> Trajectory:
    """Re-run each step against `tools`; new trajectory with updated results."""
    out_steps = []
    for step in traj.steps:
        fn = tools.get(step.tool)
        result = fn(step.args_summary) if fn else "(tool not found)"
        new = step.model_copy(update={"result_summary": result})
        out_steps.append(new)
    return traj.model_copy(update={"steps": out_steps})
