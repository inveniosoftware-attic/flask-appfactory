# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Command line interface factory."""

from __future__ import absolute_import, print_function, unicode_literals

import click
from flask_cli import FlaskGroup
from flask_registry import ModuleAutoDiscoveryRegistry

from .app import load_application


class CLIDiscoveryRegistry(ModuleAutoDiscoveryRegistry):

    """Discover CLI modules and register them on a command collection.

    Searches for a variable ``commands`` in a module ``cli`` in each package.
    The variable must be a list of commands/groups to register, e.g:

    .. code-block:: python

       import click

       @click.command()
       def testcmd():
           click.echo("Test")

       commands = [testcmd, ]

    :param cli: A ``click.Command`` or ``click.Group`` object.
    :param app: Flask application.
    """

    def __init__(self, cli, app, **kwargs):
        """Initialize the registry."""
        self.cli = cli
        super(CLIDiscoveryRegistry, self).__init__('cli', app=app, **kwargs)

    def register(self, module):
        """Register modules with CLI variable."""
        module_commands = getattr(module, 'commands', None)
        if module_commands is not None:
            for c in module_commands:
                if isinstance(c, click.BaseCommand):
                    self.cli.add_command(c)

        super(CLIDiscoveryRegistry, self).register(module)


def load_cli(app, cli=None):
    """Load CLI commands and register them on CLI application.

    :param app: Flask application instance.
    :param cli: Click command group. If no group is provided, the commands are
        registered on the Flask applications cli.
    """
    CLIDiscoveryRegistry(app.cli if cli is None else cli, app)


def clifactory(create_app, **config):
    """Create a click CLI application based on configuration.

    The CLI will install the default ``run`` and ``shell`` commands from Flask,
    and load commands from the list of modules defined in ``PACKAGES``. It will
    search in ``cli.py`` in each module for a variable ``cli``.

    The Flask application is not fully loaded unless the Flask app context is
    required.

    :param create_app: Flask application factory function.
    """
    # Create application object without loading the full application.
    app = create_app(load=False, **config)

    def create_cli_app(info):
        if not app.extensions['loaded']:
            load_application(app)
        return app

    @click.group(cls=FlaskGroup, create_app=create_cli_app)
    def cli(**params):
        pass

    # # Create command collection
    # cli = AppFactoryCollection(create_cli_app)
    # cli.add_source(flask_cli)

    # Register CLI modules from packages.
    load_cli(app, cli)

    return cli
