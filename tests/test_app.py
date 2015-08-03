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

import os
from flask_appfactory import appfactory


def test_dummy_app():
    """."""
    class conf:
        SOMEVAR = True
    app = appfactory("dummyapp", conf)
    assert app.name == "dummyapp"
    assert app.config['SOMEVAR']
    assert app.config['SECRET_KEY'] == "change_me"
    assert len(app.extensions['registry']['packages']) == 0
    assert len(app.extensions['registry']['blueprints']) == 0

    with app.test_client() as c:
        rv = c.get('/')
        assert rv.status_code == 404


def test_conf_overwrite():
    """."""
    class conf:
        SOMEVAR = True
    app = appfactory("dummyapp", conf, SOMEVAR=False)
    assert app.config['SOMEVAR'] == False


def test_envvars_overwrite():
    """."""
    class conf:
        SOMEVAR = True

    try:
        os.environ['MYAPP_APP_CONFIG_ENVS'] = 'SOMEVAR, SOMEVAR1'
        os.environ['SOMEVAR'] = 'False'
        os.environ['SOMEVAR1'] = '"V1"'
        os.environ['SOMEVAR2'] = '"V2"'

        app = appfactory("myapp", conf, SOMEVAR=True)
        # Env overrides kwargs
        assert app.config['SOMEVAR'] == False
        # Only vars specified in MYAPP_APP_CONFIG_ENVS is set.
        assert app.config['SOMEVAR1'] == "V1"
        assert 'SOMEVAR2' not in app.config
    finally:
        del os.environ['MYAPP_APP_CONFIG_ENVS']
        del os.environ['SOMEVAR']
        del os.environ['SOMEVAR1']
        del os.environ['SOMEVAR2']


def test_envvars_string():
    """."""
    class conf:
        pass

    try:
        os.environ['MYAPP_APP_CONFIG_ENVS'] = 'SOMEVAR'
        os.environ['SOMEVAR'] = 'syntaxerror'
        app = appfactory("myapp", conf)
        assert app.config['SOMEVAR'] == "syntaxerror"
    finally:
        del os.environ['MYAPP_APP_CONFIG_ENVS']
        del os.environ['SOMEVAR']


def test_simple_app():
    """."""
    class conf:
        PACKAGES = ['simplemodule']
    app = appfactory("simpleapp", conf)

    assert app.extensions['loaded']
    assert len(app.extensions['registry']['packages']) == 1
    assert len(app.extensions['registry']['blueprints']) == 1
    assert app.config['SIMPLEMODULE_VAR']

    with app.test_client() as c:
        rv = c.get('/')
        assert rv.status_code == 200
        assert rv.data == 'TEST'.encode('utf-8')


def test_simple_app_noload():
    """."""
    class conf:
        PACKAGES = ['simplemodule']
    app = appfactory("simpleapp", conf, load=False)

    assert not app.extensions['loaded']
    assert len(app.extensions['registry']['packages']) == 1
    assert 'blueprints' not in app.extensions['registry']
    assert 'SIMPLEMODULE_VAR' not in app.config
    assert 'PACKAGES' in app.config

    with app.test_client() as c:
        assert c.get('/').status_code == 404
