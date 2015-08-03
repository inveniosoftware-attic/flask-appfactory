# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test app factory."""

from __future__ import absolute_import, print_function, unicode_literals

from click.testing import CliRunner
from flask import Flask
from flask_appfactory import appfactory, clifactory
from flask_cli import ScriptInfo


def create_app(load=True):
    """Application factory used for testing."""
    class conf:
        PACKAGES = ['simplemodule']

    return appfactory('myapp', conf, load=load)


def test_factory():
    """Test CLI factory method with/without app context."""
    cli = clifactory(create_app)

    # Without app context
    runner = CliRunner()
    result = runner.invoke(cli, ['testsimple'])
    assert result.exit_code == 0
    assert result.output == 'Test Simple\n'

    # With app context
    runner = CliRunner()
    result = runner.invoke(cli, ['testapp'])
    assert result.exit_code == 0
    assert result.output == 'Test myapp\n'


def test_cli_module_only_testing():
    """Test that CLI module can be tested standalone."""
    from simplemodule.cli import testsimple, testapp

    runner = CliRunner()
    result = runner.invoke(testsimple, [])
    assert result.exit_code == 0
    assert result.output == 'Test Simple\n'

    # Testing click applications which needs the Flask app context requires you
    # to manually create a ScriptInfo object.
    obj = ScriptInfo(create_app=lambda info: Flask('anotherapp'))

    runner = CliRunner()
    result = runner.invoke(testapp, [], obj=obj)
    assert result.exit_code == 0
    assert result.output == 'Test anotherapp\n'
