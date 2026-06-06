"""End-to-end runner: synthesize trajectories -> council -> diff against baseline -> alerts."""

from __future__ import annotations

import json
import random
from pathlib import Path

from aeh.alerts.regression import make_alerts
from aeh.diff.trajectory_diff import diff
from aeh.judges.council import DEFAULT_COUNCIL, run_council
from aeh.types import CouncilResult, DiffReport, Step, Trajectory
from aeh.viz.charts import (
    alerts_pie,
    diff_summary_bar,
    judge_agreement_heatmap,
    n_steps_box,
    score_hist,
)


def _synth(n: int = 30, seed: int = 17) -> list[Trajectory]:
    rng = random.Random(seed)
    tools = ["search", "retrieve", "summarize", "verify", "answer"]
    out: list[Trajectory] = []
    for i in range(n):
        n_steps = rng.randint(3, 10)
        steps = [
            Step(idx=j, tool=rng.choice(tools), args_summary=f"arg-{j}", result_summary=f"r-{j}")
            for j in range(n_steps)
        ]
        out.append(Trajectory(tid=f"t-{i:03d}", steps=steps, final_answer=f"answer-{i}"))
    return out


def _mutate(trajs: list[Trajectory], frac: float = 0.3, seed: int = 19) -> list[Trajectory]:
    rng = random.Random(seed)
    out: list[Trajectory] = []
    for t in trajs:
        if rng.random() > frac:
            out.append(t)
            continue
        new_steps = list(t.steps)
        if new_steps:
            j = rng.randrange(len(new_steps))
            new_steps[j] = new_steps[j].model_copy(update={"tool": "new_tool"})
        out.append(t.model_copy(update={"steps": new_steps}))
    return out


def run(out_dir: Path, n: int = 30, seed: int = 17) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    figs = Path("results/figures")
    prev = _synth(n=n, seed=seed)
    curr = _mutate(prev, frac=0.3, seed=seed + 1)

    prev_scores = {c.tid: c.mean_score for c in [run_council(t, DEFAULT_COUNCIL) for t in prev]}
    curr_scores: list[CouncilResult] = [run_council(t, DEFAULT_COUNCIL) for t in curr]
    diffs: list[DiffReport] = [diff(a, b) for a, b in zip(prev, curr, strict=True)]
    alerts = make_alerts(prev_scores, curr_scores, diffs)

    step_counts = {t.tid: len(t.steps) for t in curr}

    score_hist(curr_scores, figs / "score_hist.png")
    judge_agreement_heatmap(curr_scores, figs / "judge_heatmap.png")
    diff_summary_bar(diffs, figs / "diff_summary.png")
    alerts_pie(alerts, figs / "alerts_pie.png")
    n_steps_box(curr_scores, step_counts, figs / "steps_box.png")

    summary: dict[str, object] = {
        "n_traj": len(curr),
        "n_alerts": len(alerts),
        "mean_curr_score": sum(c.mean_score for c in curr_scores) / max(1, len(curr_scores)),
        "diffs": [d.model_dump() for d in diffs],
        "alerts": [a.model_dump() for a in alerts],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    return summary
