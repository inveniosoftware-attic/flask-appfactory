Step 1: Creating a reusable package
-----------------------------------
First, let's start by creating a small reusable package that we would possibly
like to use in many different applications. The package consists of:

- a Flask blueprint +  templates.
- a Click command line interface.
- default configuration for the package.

Here's how the directory structure looks like::

    mymodule/__init__.py  (empty)
    mymodule/cli.py
    mymodule/config.py
    mymodule/views.py
    mymodule/templates/mymodule.html
    mymodule/templates/mymodule_base.html


Default configuration
~~~~~~~~~~~~~~~~~~~~~
The package can provide default configuration values in a ``config.py`` that it
expects to be set. The values are merged into the Flask applications
configuration and can be overwritten by each instance of an application.

.. literalinclude:: ../examples/mymodule/config.py
   :language: python
   :linenos:

Blueprint
~~~~~~~~~
The package can also provide a blueprint. The blueprint will automatically be
registered on the Flask application by Flask-AppFactory.


.. literalinclude:: ../examples/mymodule/views.py
   :language: python
   :linenos:
   :emphasize-lines: 8, 15

This example blueprint simply renders the template ``mymodule.html`` and
pass it the value of ``MYMODULE_GREETING`` (line 15) that we ensured was set in
``config.py``. Notice, also that the Blueprint's template folder is set in line
8 (without it, the templates in the next section are not found).


Templates
~~~~~~~~~
The package provides two templates ``mymodule.html`` and ``mymodule_base.html``
, where ``mymodule.html`` simply extends ``mymodule_base.html``. The reason for
this slightly odd method, is that it allows other packages to easily modify the
templates without copy/pasting the entire template code. Another package simply
creates a ``mymodule.html`` also extending from ``mymodule_base.html``, and
only overwrites the few template blocks that it needs to customize.

.. literalinclude:: ../examples/mymodule/templates/mymodule.html
   :language: html
   :linenos:

.. literalinclude:: ../examples/mymodule/templates/mymodule_base.html
   :language: html
   :linenos:

.. note::
   It is usually a good idea to put your templates into a subfolder to avoid
   name conflicts between multiple packages.


Command Line interface
~~~~~~~~~~~~~~~~~~~~~~

Finally, our package provide some simple CLI commands in ``cli.py`` that will
be merged into a single CLI application that can used to manage a Flask
application.

The CLI is based on the `Click <http://click.pocoo.org/>`_ Python package which
has good extensive documentation.

.. literalinclude:: ../examples/mymodule/cli.py
   :language: python
   :linenos:
   :emphasize-lines: 18, 13

Flask-AppFactory expects to find a variable ``commands`` in ``cli.py``
with a list of commands to register (line 18). Using the
``@with_appcontext`` (line 13) decorator the commands can access the
Flask application context (e.g ``current_app``). Without the decorator
the application is not fully loaded in order to speed up the CLI.
