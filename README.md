# agent-eval-harness

> Generic agent evaluation harness: trajectory replays, judge council, action-graph diffing, regression alerts.
> Last updated: 2024-11-12.

`agent-eval-harness` is a framework-agnostic evaluation harness for agent trajectories. It scores each trajectory with a small judge council, diffs it against a baseline trajectory of the same id, and raises a regression alert when either the score drops or the diff is large. Five chart families surface the score distribution, judge agreement, diff summary, alerts breakdown, and step-count distribution.

Designed to slot in next to any agent loop: produce `Trajectory` objects, point the harness at them, get alerts.

## Headline (fixture: 30 trajectories, 30% mutation rate)

| metric | value |
|---|---|
| trajectories | 30 |
| mean score | reported at runtime |
| alerts | reported at runtime |

Reproduce: `make install && make bench`.

## Pipeline

```mermaid
flowchart LR
  A[Baseline Trajectories] --> B["Judge council\n(length, diversity, answer_present)"]
  C[Current Trajectories]  --> D[Judge council]
  A & C --> E[Trajectory diff]
  D & E --> F[Regression alerts]
  D, E, F --> G[5 chart families + summary.json]
```

## Five chart families

- `results/figures/score_hist.png` - distribution of mean council scores
- `results/figures/judge_heatmap.png` - per-trajectory judge scores
- `results/figures/diff_summary.png` - per-diff status counts
- `results/figures/alerts_pie.png` - alerts by severity
- `results/figures/steps_box.png` - step-count distribution

## Repo layout

```
src/aeh/
  types.py                # Trajectory, Step, JudgeVerdict, CouncilResult, DiffReport, RegressionAlert
  trajectory/replay.py    # re-run a trajectory against a tool table
  judges/council.py       # 3-judge council with reducer
  diff/trajectory_diff.py # diff(a, b) -> DiffReport
  alerts/regression.py    # score-drop + diff-size alerts
  viz/charts.py           # 5 chart families
  cli/main.py             # `aeh bench`
  runner.py
tests/                    # tests, all green
docs/research_report.pdf
docs/_report/, docs/test_results/, results/figures/
CITATION.cff, LICENSE, Makefile, .github/workflows/ci.yml
```

## Quick start

```bash
make install
make test
make bench
make pdf
```

## Documentation

Long-form research report: [`docs/research_report.pdf`](./docs/research_report.pdf) and [`docs/_report/research_report.md`](./docs/_report/research_report.md).

Test artifacts: [`docs/test_results/`](./docs/test_results/).

## References

- Yao et al., "ReAct: Synergizing Reasoning and Acting" (2022)
- Zheng et al., "Judging LLM-as-a-Judge" (2023)

## License

MIT.
