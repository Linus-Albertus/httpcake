import os
import click
import crud
from pathlib import Path


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """A simple app for manage httpie requests"""

    request_dir = "./.httpcake/"

    if not os.path.exists(request_dir):
        os.makedirs(request_dir)

    ctx.obj = {"request_dir": Path(request_dir)}

cli.add_command(crud.create)
cli.add_command(crud.ls)
cli.add_command(crud.run)
cli.add_command(crud.delete)

