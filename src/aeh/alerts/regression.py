"""Regression alerting based on council-score drop and diff size."""

from __future__ import annotations

from aeh.types import CouncilResult, DiffReport, RegressionAlert


def make_alerts(
    prev_scores: dict[str, float],
    curr: list[CouncilResult],
    diffs: list[DiffReport],
    score_threshold: float = 0.10,
    diff_threshold: int = 3,
) -> list[RegressionAlert]:
    by_tid = {d.tid: d for d in diffs}
    out: list[RegressionAlert] = []
    for c in curr:
        prev = prev_scores.get(c.tid)
        diff_report = by_tid.get(c.tid)
        if prev is not None and prev - c.mean_score > score_threshold:
            out.append(
                RegressionAlert(
                    tid=c.tid,
                    severity="high",
                    message=f"score dropped {prev:.2f} to {c.mean_score:.2f}",
                )
            )
        if diff_report and diff_report.n_step_changes > diff_threshold:
            out.append(
                RegressionAlert(
                    tid=c.tid,
                    severity="medium",
                    message=f"{diff_report.n_step_changes} step changes",
                )
            )
    return out
