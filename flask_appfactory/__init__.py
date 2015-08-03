# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask-AppFactory is an dynamic application loader.

It allows you to build reusable modules that can be easily be assembled into
full Flask applications using this loader. Each reusable module can provide
default configuration, blueprints and command line interface.
"""

from __future__ import absolute_import, unicode_literals, print_function

from .app import appfactory
from .cli import clifactory, load_cli

from .version import __version__

__all__ = ('appfactory', 'clifactory', 'load_cli', '__version__')
