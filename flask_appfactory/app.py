# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask application factory."""

from __future__ import absolute_import, print_function, unicode_literals

import logging
import os
import re
import sys
import warnings

import ast
from flask import Flask
from flask_cli import FlaskCLI
from flask_registry import BlueprintAutoDiscoveryRegistry, \
    ConfigurationRegistry, ExtensionRegistry, PackageRegistry, Registry


def configure_warnings():
    """Configure warnings by routing warnings to the logging system.

    It also unhides ``DeprecationWarning``.
    """
    if not sys.warnoptions:
        # Route warnings through python logging
        logging.captureWarnings(True)

        # DeprecationWarning is by default hidden, hence we force the
        # "default" behavior on deprecation warnings which is not to hide
        # errors.
        warnings.simplefilter("default", DeprecationWarning)


def load_config(app, module_name, **kwargs_config):
    """Load configuration.

    Configuration is loaded in the following order:

    1. Configuration module (i.e. ``module_name``).
    2. Instance configuration in ``<instance folder>/<app name>.cfg``
    3. Keyword configuration arguments.
    4. Environment variables specified in ``<app name>_APP_CONFIG_ENVS``
       configuration variable or comma separated list in environment variable
       with the same name.

    Additionally checks if ``SECRET_KEY`` is set in the configuration and warns
    if it is not.

    :param app: Flask application.
    :param module_name: Configuration module.
    :param kwargs_config: Configuration keyword arguments
    """
    # 1. Load site specific default configuration
    if module_name:
        app.config.from_object(module_name)

    # 2. Load <app name>.cfg from instance folder
    app.config.from_pyfile('{0}.cfg'.format(app.name), silent=True)

    # 3. Update application config from parameters.
    app.config.update(kwargs_config)

    # 4. Update config with specified environment variables.
    envvars = '{0}_APP_CONFIG_ENVS'.format(app.name.upper())

    for cfg_name in app.config.get(envvars, os.getenv(envvars, '')).split(','):
        cfg_name = cfg_name.strip().upper()
        if cfg_name:
            cfg_value = app.config.get(cfg_name)
            cfg_value = os.getenv(cfg_name, cfg_value)
            try:
                cfg_value = ast.literal_eval(cfg_value)
            except (SyntaxError, ValueError):
                pass
            app.config[cfg_name] = cfg_value
            app.logger.debug("{0} = {1}".format(cfg_name, cfg_value))

    # Ensure SECRET_KEY is set.
    SECRET_KEY = app.config.get('SECRET_KEY')

    if SECRET_KEY is None:
        app.config["SECRET_KEY"] = 'change_me'
        warnings.warn(
            "Set variable SECRET_KEY with random string in {}".format(
                os.path.join(app.instance_path, "{}.cfg".format(app.name)),
            ), UserWarning)

    # Initialize application registry, used for discovery and loading of
    # configuration, extensions and blueprints
    Registry(app=app)

    app.extensions['registry'].update(
        # Register packages listed in PACKAGES conf variable.
        packages=PackageRegistry(app))

    app.extensions['loaded'] = False


def load_application(app):
    """Load the application.

    Assembles the application by use of ``PACKAGES`` and ``EXTENSIONS``
    configuration variables.

    1. Load extensions by calling ``setup_app()`` in module defined in
       ``EXTENSIONS``.
    2. Register blueprints from each module defined in ``PACAKGES`` by looking
       searching in ``views.py`` for a ``blueprint`` or ``blueprints``
       variable.

    :param app: Flask application.
    """
    # Extend application config with default configuration values from packages
    # (app config takes precedence)
    app.extensions['registry'].update(
        # Register extensions listed in EXTENSIONS conf variable.
        extensions=ExtensionRegistry(app),
        # Register blueprints from packages in PACKAGES configuration variable.
        blueprints=BlueprintAutoDiscoveryRegistry(app=app),
    )

    ConfigurationRegistry(app)

    app.extensions['loaded'] = True


def base_app(app_name, instance_path=None, static_folder=None,
             static_url_path='/static/', instance_relative_config=True,
             template_folder='templates', flask_cls=Flask):
    """Create a base Flask Application.

    Ensures instance path and is set and created. Instance path defaults to
    ``<sys.prefix>/var/<app name>-instance``.

    Additionally configure warnings to be routed to the Python logging system,
    and by default makes ``DeprecationWarning`` loud.

    .. versionchanged:: v0.2.0
       Added ``flask_cls`` parameter.

    :param app_name: Flask application name.
    :param instance_path: Instance path
    :param static_folder: Static folder.
    :param static_url_path: URL path of static folder. Default: ``/static/``.
    :param instance_relative_config: Use instance relative config
        Default: ``True``.
    :param template_folder: Template folder. Default: ``templates``.
    :param flask_cls: Flask Application class. Default: ``Flask``.
    """
    configure_warnings()

    # Prefix for env variables
    env_prefix = re.sub('[^A-Z]', '', app_name.upper())

    # Detect instance path
    instance_path = instance_path or \
        os.getenv(env_prefix + '_INSTANCE_PATH') or \
        os.path.join(sys.prefix, 'var', app_name + '-instance')

    # Detect static files path
    static_folder = static_folder or \
        os.getenv(env_prefix + '_STATIC_FOLDER') or \
        os.path.join(instance_path, 'static')

    # Create instance path
    try:
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
    except Exception:  # pragma: no cover
        pass

    # Create the Flask application instance
    app = flask_cls(
        app_name,
        static_url_path=static_url_path,
        static_folder=static_folder,
        instance_relative_config=instance_relative_config,
        instance_path=instance_path,
        template_folder=template_folder,
    )

    # Compatibility layer to support Flask 1.0 click integration on v0.10
    FlaskCLI(app=app)

    return app


def appfactory(app_name, module_name, load=True, **kwargs_config):
    """Create a Flask application according to a defined configuration.

    :param app_name: Flask application name.
    :param module_name: Python configuration module.
    :param load: Load application (instead of only the configuration).
        Default: ``True``.
    :param kwargs_config: Extra configuration variables for the Flask
        application.
    """
    app = base_app(app_name)

    load_config(app, module_name, **kwargs_config)

    if load:
        load_application(app)

    return app
