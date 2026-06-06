"""Five chart families for the agent-eval-harness."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from aeh.types import CouncilResult, DiffReport, RegressionAlert


def _save(fig: Figure, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def score_hist(scores: list[CouncilResult], out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist([s.mean_score for s in scores], bins=20, color="#3b6fa1", edgecolor="white")
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("mean judge score")
    ax.set_ylabel("trajectories")
    ax.set_title("Score distribution across trajectories")
    return _save(fig, out)


def judge_agreement_heatmap(scores: list[CouncilResult], out: Path) -> Path:
    if not scores:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.text(0.5, 0.5, "no scores", ha="center", va="center")
        ax.set_axis_off()
        return _save(fig, out)
    judges = [v.judge_name for v in scores[0].verdicts]
    mat = np.zeros((len(scores), len(judges)))
    for i, c in enumerate(scores):
        for j, v in enumerate(c.verdicts):
            mat[i, j] = v.score
    fig, ax = plt.subplots(figsize=(7, 4.5))
    im = ax.imshow(mat, aspect="auto", cmap="viridis", vmin=0, vmax=1)
    ax.set_xticks(range(len(judges)))
    ax.set_xticklabels(judges, rotation=30, ha="right")
    ax.set_ylabel("trajectory")
    ax.set_title("Per-trajectory judge scores")
    fig.colorbar(im, ax=ax, label="score")
    return _save(fig, out)


def diff_summary_bar(diffs: list[DiffReport], out: Path) -> Path:
    same = sum(1 for d in diffs if d.same_n_steps)
    diff_len = len(diffs) - same
    n_changed = sum(1 for d in diffs if d.n_step_changes > 0)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(
        ["same length", "different length", "any step change"],
        [same, diff_len, n_changed],
        color="#5b8d4a",
    )
    ax.set_ylabel("trajectories")
    ax.set_title("Diff summary")
    return _save(fig, out)


def alerts_pie(alerts: list[RegressionAlert], out: Path) -> Path:
    from collections import Counter

    cnt = Counter(a.severity for a in alerts)
    fig, ax = plt.subplots(figsize=(5, 5))
    if not cnt:
        ax.text(0.5, 0.5, "no alerts", ha="center", va="center")
        ax.set_axis_off()
        return _save(fig, out)
    labels = list(cnt.keys())
    vals = list(cnt.values())
    ax.pie(vals, labels=labels, autopct="%1.0f%%", colors=["#c25a4f", "#e6a23c", "#5b8d4a"])
    ax.set_title("Alerts by severity")
    return _save(fig, out)


def n_steps_box(scores: list[CouncilResult], step_counts: dict[str, int], out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.boxplot([list(step_counts.values())], tick_labels=["all trajectories"])
    ax.set_ylabel("# steps per trajectory")
    ax.set_title("Trajectory step-count distribution")
    return _save(fig, out)
