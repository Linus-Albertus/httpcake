import click
import json
import subprocess


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
        with open(f"{request_dir}/requests.json", "r") as file:
            existing_data = json.load(file)

    except FileNotFoundError:
        existing_data = []

    request_data = {
        "name": name,
        "httpie_request": request,
        "method": method,
        "tags": tags.split(",") if tags else [],
    }

    # TODO: check httpie request
    # TODO: save response if is a aceptable one

    # Append new data
    existing_names = [n["name"] for n in existing_data]
    if name not in existing_names:
        existing_data.append(request_data)

        with open(f"{request_dir}/requests.json", "w") as file:
            json.dump(existing_data, file, indent=4)
        click.echo("Request saved.")

    else:
        click.echo("Choose another name! That one is already taken.")


@click.command()
@click.pass_context
def ls(ctx: click.Context) -> None:
    """List all requests saved"""
    request_dir = ctx.obj["request_dir"]

    try:
        with open(f"{request_dir}/requests.json", "r") as file:
            existing_data = json.load(file)

        counter = 1
        for d in existing_data:
            click.echo(
                f"({counter}) Name: {d["name"]}, Method: {d["method"]}, Request: {d["httpie_request"]}, Tags: {d["tags"]}"
            )
            counter += 1

    except FileNotFoundError:
        click.echo(f"No saved requests for this project!")


@click.command()
@click.option("--request", "-r", type=click.INT, prompt="ID of request")
@click.pass_context
def run(ctx: click.Context, request: int) -> None:
    """Run a request from name"""
    request_dir = ctx.obj["request_dir"]

    try:
        with open(f"{request_dir}/requests.json", "r") as file:
            existing_data = json.load(file)

        request_body = existing_data[request - 1]

        click.echo(
            f"Running: {request_body["method"]}, {request_body["httpie_request"]}",
            nl=True,
        )
        click.echo()
        subprocess.run(
            ["http", str(request_body["method"]), str(request_body["httpie_request"])]
        )

    except FileNotFoundError:
        click.echo(f"No save requests for this project!")


@click.command()
@click.option("--request", "-r", type=click.INT, prompt="ID of request")
@click.pass_context
def delete(ctx: click.Context, request: int) -> None:
    """Delete a request from name"""
    request_dir = ctx.obj["request_dir"]

    try:
        with open(f"{request_dir}/requests.json", "r") as file:
            existing_data = json.load(file)

        deleted_request = existing_data.pop(request - 1)

        with open(f"{request_dir}/requests.json", "w") as file:
            json.dump(existing_data, file, indent=4)

        click.echo(f"Deleted request #{request}: {deleted_request["name"]}.")

    except FileNotFoundError:
        click.echo(f"No save request for this project!")

