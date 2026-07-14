from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

app = typer.Typer(
    help="Inspect EKS workload identity wiring without mutating cluster or AWS state.",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)
console = Console()


@app.callback()
def callback() -> None:
    """PodSleuth command group."""


@app.command("version")
def version() -> None:
    console.print("podsleuth 0.1.0")


def main(argv: Annotated[list[str] | None, typer.Argument(hidden=True)] = None) -> None:
    app(args=argv)
