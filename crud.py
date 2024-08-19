import click
import subprocess

import toml


@click.command()
@click.option("--name", "-n", type=click.STRING, prompt="Name to save the request")
@click.option("--request", "-r", type=click.STRING, prompt="Httpie request")
@click.option("--method", "-m", type=str, default="GET")
@click.option("--tags", help="Comma-separated list of tags")
@click.pass_context
def create(ctx: click.Context, name: str, request: str, method: str, tags: str) -> None:
    """Create a request"""
    request_dir = ctx.obj["request_dir"]

    # TODO: create dir if not exists

    try:
        with open(f"{request_dir}/requests.toml", "r") as file:
            existing_data = toml.load(file)
    except FileNotFoundError:
        existing_data = {}

    request_data = {
        name: {
            "httpie_request": request,
            "method": method,
            "tags": tags.split(",") if tags else [],
        }
    }

    # TODO: check httpie request
    # TODO: save response if is a aceptable one

    # Append new data
    if name not in existing_data:
        existing_data.update(request_data)

        with open(f"{request_dir}/requests.toml", "w") as file:
            toml.dump(existing_data, file)
        click.echo("Request saved.")
    else:
        click.echo("Choose another name! That one is already taken.")


@click.command()
@click.pass_context
def ls(ctx: click.Context) -> None:
    """List all requests saved"""
    request_dir = ctx.obj["request_dir"]

    try:
        with open(f"{request_dir}/requests.toml", "r") as file:
            existing_data = toml.load(file)

        counter = 1
        for name, data in existing_data.items():
            click.echo(
                f"({counter}) Name: {name}, Method: {data['method']}, Request: {data['httpie_request']}, Tags: {data['tags']}"
            )
            counter += 1

    except FileNotFoundError:
        click.echo("No saved requests for this project!")


@click.command()
@click.option("--request", "-r", type=click.INT, prompt="ID of request")
@click.pass_context
def run(ctx: click.Context, request: int) -> None:
    """Run a request from name"""
    request_dir = ctx.obj["request_dir"]

    try:
        with open(f"{request_dir}/requests.toml", "r") as file:
            existing_data = toml.load(file)

        request -= 1
        if 0 <= request < len(existing_data):
            # Access request by index
            request_data = list(existing_data.values())[request]

            click.echo(
                f"Running: {request_data['method']}, {request_data['httpie_request']}",
                nl=True,
            )
            click.echo()
            subprocess.run(
                [
                    "https",
                    str(request_data["method"]),
                    str(request_data["httpie_request"]),
                ]
            )
        else:
            click.echo("Request out of range!")

    except FileNotFoundError:
        click.echo("No saved requests for this project!")


@click.command()
@click.option("--request", "-r", type=click.INT, prompt="ID of request")
@click.pass_context
def delete(ctx: click.Context, request: int) -> None:
    """Delete a request from name"""
    request_dir = ctx.obj["request_dir"]
    deleted_request = None

    try:
        with open(f"{request_dir}/requests.toml", "r") as file:
            existing_data = toml.load(file)

        if request == 0:
            # Get the last key (request name)
            last_key = list(existing_data.keys())[-1]
            deleted_request = existing_data.pop(last_key)
            click.echo("Deleted last request.")
        elif request < 0:
            click.echo("You must enter a positive integer or zero.")
        elif len(existing_data) != 0:
            if 1 <= request <= len(existing_data):
                # Get the key at the specified index
                keys = list(existing_data.keys())
                deleted_key = keys[request - 1]
                deleted_request = existing_data.pop(deleted_key)
            else:
                click.echo("Request out of range!")

            with open(f"{request_dir}/requests.toml", "w") as file:
                toml.dump(existing_data, file)

            if deleted_request is not None:
                click.echo(f"Deleted request #{request}: {deleted_key}.")
        else:
            click.echo("No requests saved!")

    except FileNotFoundError:
        click.echo("No save request for this project!")
