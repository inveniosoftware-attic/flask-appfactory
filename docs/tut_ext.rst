Step 2: Enabling an extension
-----------------------------

In step 1 you have created your first reusable package. Usually however, your
packages will need access to e.g. a database backend, a cache etc. These
features are enabled via extensions.

Flask-SQLAlchemy extension
~~~~~~~~~~~~~~~~~~~~~~~~~~
Next up in our tutorial, we will enable the
`Flask-SQLAlchemy <https://pythonhosted.org/Flask-SQLAlchemy/>`_
extension to provide database models for our application and reusable packages.

Here's how the directory structure looks like::

    myext/__init__.py  (empty)
    myext/sqlalchemy.py

Flask-AppFactory enables extensions simply by calling a method
``setup_app(app)`` with the Flask application object (line 16). This
pattern allows each extension to customize the Flask application as they see
fit.

.. literalinclude:: ../examples/myexts/sqlalchemy.py
   :language: python
   :linenos:
   :emphasize-lines: 16, 18, 10

Each extension can set default configuration (line 18). The extension should
however not overwrite an existing value, hence ``app.config.setdefault``
is used. This is because any instance specific configuration has already been
loaded at this point.

By default Flask-AppFactory only loads configuration, blueprints and CLI from
each reusable package. Each enabled extension can however load further modules
from each package. E.g. in the Flask-SQLAlchemy case, we may want to load
database models from a ``models.py`` in all  enabled reusable packages. This is
achieved by creating a registry (line 10).

Each extension can natually also provide CLI commands (see line 26-30).


Using Flask-SQLAlchemy in packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that the extension has been enabled, you'll want to use it in your
packages. E.g. you could add a ``models.py`` file to the reusable package
you created in step 1:

.. literalinclude:: ../examples/mymodule/models.py
   :language: python
   :linenos:

