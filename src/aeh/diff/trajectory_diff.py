"""Trajectory diff: same length, tool-by-tool comparison, set-diff of tools."""

from __future__ import annotations

from aeh.types import DiffReport, Trajectory


def diff(a: Trajectory, b: Trajectory) -> DiffReport:
    tools_a = [s.tool for s in a.steps]
    tools_b = [s.tool for s in b.steps]
    set_a = set(tools_a)
    set_b = set(tools_b)
    same_len = len(tools_a) == len(tools_b)
    n_step_changes = sum(1 for x, y in zip(tools_a, tools_b, strict=False) if x != y)
    return DiffReport(
        tid=a.tid,
        same_n_steps=same_len,
        n_step_changes=n_step_changes,
        n_tool_changes=len(set_a ^ set_b),
        tools_added=sorted(set_b - set_a),
        tools_removed=sorted(set_a - set_b),
    )
