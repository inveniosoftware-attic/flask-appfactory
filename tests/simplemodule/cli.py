# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

import click
from flask import current_app
from flask_cli import with_appcontext


@click.command()
def testsimple():
    """."""
    click.echo("Test Simple")


@click.command()
@with_appcontext
def testapp():
    """."""
    click.echo("Test %s" % current_app.name)


commands = [testsimple, testapp]
