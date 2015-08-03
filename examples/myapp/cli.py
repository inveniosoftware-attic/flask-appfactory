# myapp/cli.py

from __future__ import absolute_import
from flask_appfactory.cli import clifactory
from .app import create_app

cli = clifactory(create_app)
