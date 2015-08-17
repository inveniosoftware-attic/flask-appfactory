# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test celery factory."""

from __future__ import absolute_import, print_function, unicode_literals

from flask_appfactory import appfactory
from flask_appfactory.celery import celeryfactory


def test_dummy_app():
    """"Test celery app creation."""
    class conf:
        EXTENSIONS = ['flask_celeryext:FlaskCeleryExt']

    app = appfactory("app2", conf)
    celery = celeryfactory(app)
    assert celery
    assert celery.flask_app == app
    assert app.extensions['flask-celeryext'].celery == celery


def test_dummy_app_noext():
    """"Test celery app creation without extension."""
    app = appfactory("app3", None)
    celery = celeryfactory(app)
    assert celery
    assert celery.flask_app == app
    assert 'flask-celeryext' not in app.extensions
