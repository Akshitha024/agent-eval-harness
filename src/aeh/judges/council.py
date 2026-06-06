"""Judge council. Each judge returns a per-trajectory score in [0, 1]."""

from __future__ import annotations

from collections.abc import Callable

from aeh.types import CouncilResult, JudgeVerdict, Trajectory

Judge = Callable[[Trajectory], JudgeVerdict]


def length_judge(t: Trajectory) -> JudgeVerdict:
    """Shorter is better, in the [3, 12] range."""
    n = len(t.steps)
    if n == 0:
        score = 0.0
    elif n <= 3:
        score = 1.0
    elif n >= 12:
        score = 0.0
    else:
        score = max(0.0, 1.0 - (n - 3) / 9)
    return JudgeVerdict(judge_name="length", score=score)


def tool_diversity_judge(t: Trajectory) -> JudgeVerdict:
    n = max(1, len(t.steps))
    diversity = len({s.tool for s in t.steps}) / n
    return JudgeVerdict(judge_name="diversity", score=diversity)


def final_answer_judge(t: Trajectory) -> JudgeVerdict:
    """Heuristic: any final answer is better than none."""
    return JudgeVerdict(judge_name="answer_present", score=1.0 if t.final_answer else 0.0)


def run_council(t: Trajectory, judges: list[Judge]) -> CouncilResult:
    verdicts = [j(t) for j in judges]
    mean = sum(v.score for v in verdicts) / max(1, len(verdicts))
    return CouncilResult(tid=t.tid, mean_score=mean, verdicts=verdicts)


DEFAULT_COUNCIL: list[Judge] = [length_judge, tool_diversity_judge, final_answer_judge]
