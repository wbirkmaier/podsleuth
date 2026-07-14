from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from podsleuth.analysis import build_snapshot
from podsleuth.exceptions import PodSleuthError
from podsleuth.fixtures import load_fixture_snapshot
from podsleuth.reporting import build_workload_explanation, render_workload_explanation

app = typer.Typer(
    help="Inspect EKS workload identity wiring without mutating cluster or AWS state.",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)
error_console = Console(stderr=True)


@app.callback()
def callback() -> None:
    """PodSleuth command group."""


@app.command("version")
def version() -> None:
    typer.echo("podsleuth 0.1.0")


@app.command("scan")
def scan(
    fixtures: Annotated[
        Path,
        typer.Option(
            "--fixtures",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Directory containing cluster.json and iam.json fixture files.",
        ),
    ],
) -> None:
    try:
        snapshot = build_snapshot(load_fixture_snapshot(fixtures))
    except PodSleuthError as error:
        error_console.print(str(error), style="red")
        raise typer.Exit(code=error.exit_code) from error

    typer.echo(snapshot.model_dump_json(indent=2))


@app.command("explain")
def explain(
    workload: Annotated[str, typer.Argument(help="Workload reference in <namespace>/<name> form.")],
    fixtures: Annotated[
        Path,
        typer.Option(
            "--fixtures",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Directory containing cluster.json and iam.json fixture files.",
        ),
    ],
) -> None:
    try:
        bundle = load_fixture_snapshot(fixtures)
        explanation = build_workload_explanation(bundle, build_snapshot(bundle), workload)
    except PodSleuthError as error:
        error_console.print(str(error), style="red")
        raise typer.Exit(code=error.exit_code) from error

    typer.echo(render_workload_explanation(explanation))


def main(argv: Annotated[list[str] | None, typer.Argument(hidden=True)] = None) -> None:
    app(args=argv)
