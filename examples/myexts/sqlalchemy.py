# myexts/sqlalchemy.py

import click
from flask_cli import with_appcontext
from flask.ext.sqlalchemy import SQLAlchemy
from flask_registry import ModuleAutoDiscoveryRegistry, RegistryProxy

db = SQLAlchemy()

models = RegistryProxy(
    'models',  # Registry namespace
    ModuleAutoDiscoveryRegistry,
    'models'   # Module name (i.e. models.py)
)

def setup_app(app):
    # Set default configuration
    app.config.setdefault(
        'SQLALCHEMY_DATABASE_URI',
        'sqlite:////tmp/test.db'
    )
    # Add extension CLI to application.
    app.cli.add_command(initdb)
    db.init_app(app)

@click.command()
@with_appcontext
def initdb():
    """Initialize database."""
    db.create_all()
