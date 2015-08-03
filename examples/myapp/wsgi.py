# myapp/wsgi.py

from __future__ import absolute_import
from .app import create_app

application = create_app()
