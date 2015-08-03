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

from flask_appfactory import appfactory


def test_jinja2_ext():
    """Test Jinja2 extension."""
    class conf:
        PACKAGES = ['simplemodule', 'simplemodule2']
        EXTENSIONS = ['flask_appfactory.ext.jinja2']
        JINJA2_EXTENSIONS = ['jinja2.ext.do']

    app = appfactory("dummyapp", conf)

    with app.test_client() as c:
        c.get('/simplemodule').data == "SIMPLEMODULE"
        c.get('/simplemodule2') == "SIMPLEMODULE"

    # Test reverse package order
    class conf:
        PACKAGES = ['simplemodule2', 'simplemodule']
        EXTENSIONS = ['flask_appfactory.ext.jinja2']

    app = appfactory("dummyapp", conf)

    with app.test_client() as c:
        c.get('/simplemodule').data == "SIMPLEMODULE2"
        c.get('/simplemodule2') == "SIMPLEMODULE2"
