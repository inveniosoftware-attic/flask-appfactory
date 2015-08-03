# mymodule/cli.py

import click
from flask import current_app
from flask_cli import with_appcontext

@click.command()
def testsimple():
    """Command without application context."""
    click.echo("Test")

@click.command()
@with_appcontext
def testapp():
    """Command with application context."""
    click.echo(current_app.name)

commands = [testsimple, testapp]
