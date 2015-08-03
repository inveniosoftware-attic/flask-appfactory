# manage.py
from myapp.app import create_app
from flask_appfactory import load_cli
app = create_app()
load_cli(app)
