# myapp/config.py

EXTENSIONS = [
    "flask_appfactory.ext.jinja2",
    "flask_celeryext:FlaskCeleryExt",
    "myexts.sqlalchemy",
]

PACKAGES = [
    "mymodule",
]

BROKER_URL = "redis://localhost:6379/0"
