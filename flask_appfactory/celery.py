# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Celery application factory."""

from __future__ import absolute_import, print_function, unicode_literals

from flask_celeryext import create_celery_app
from flask_registry import ModuleAutoDiscoveryRegistry


def load_tasks(app):
    """Load Celery tasks from installed packages.

    .. versionadded:: v0.2.0
    """
    app.extensions['registry']['tasks'] = ModuleAutoDiscoveryRegistry(
            module_name='tasks', app=app)


def celeryfactory(app):
    """Create a Celery application based on Flask application.

    .. versionadded:: v0.2.0

    :param app: Flask application instance.
    """
    try:
        # Check if celery application has already been created.
        celery = app.extensions['flask-celeryext'].celery
    except KeyError:
        celery = create_celery_app(app)
    load_tasks(app)

    return celery
