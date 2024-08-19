"""CRUD operations related tests."""

import json

from click.testing import CliRunner

from crud import create, ls
from httpcake import cli

runner = CliRunner()


def test_create():
    result = runner.invoke(
        cli, ["create", "--name", "Test Request", "--request", "httpie.io/hello"]
    )
    assert result.exit_code == 0
    assert result.output == "Request saved.\n"


def test_ls():
    result = runner.invoke(cli, ["ls"])
    assert result.exit_code == 0


def test_run():
    pass


def test_delete_ok():
    result = runner.invoke(cli, ["delete", "--request", 0])
    assert result.exit_code == 0


def test_delete_negatives():
    result = runner.invoke(cli, ["delete", "--request", -1])
    assert result.exit_code == 0
    assert result.output == "You must enter a positive integer or zero.\n"


def test_delete_out_of_range():
    result = runner.invoke(cli, ["delete", "--request", 1000])
    assert result.exit_code == 0
    assert result.output == "Request out of range!\n"
