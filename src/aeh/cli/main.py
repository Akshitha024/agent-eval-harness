"""Typer CLI for agent-eval-harness."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

from aeh.runner import run

app = typer.Typer(no_args_is_help=True, help="Generic agent evaluation harness.")
console = Console()


@app.command()
def info() -> None:
    """Print harness info."""
    console.print("agent-eval-harness: see `aeh bench --help`.")


@app.command()
def bench(
    out_dir: Path = typer.Option(Path("runs/latest")),
    n: int = typer.Option(30),
    seed: int = typer.Option(17),
) -> None:
    res = run(out_dir, n=n, seed=seed)
    console.print_json(
        json.dumps(
            {
                "n_traj": res["n_traj"],
                "n_alerts": res["n_alerts"],
                "mean_curr_score": res["mean_curr_score"],
            },
            default=str,
        )
    )


if __name__ == "__main__":
    app()
