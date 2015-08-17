Step 3: Creating an application
===============================

You now have a reusable package and an extension. The last step is to make
it into a fully functioning Flask application, and the step where
Flask-AppFactory will do all the heavy lifting for you.

Here's how the directory structure looks like::

    myapp/__init__.py  (empty)
    myapp/app.py
    myapp/cli.py
    myapp/config.py
    myapp/wsgi.py
    setup.py


Application configuration
-------------------------
First we define how our application is assembled by providing the default
application configuration:

.. literalinclude:: ../examples/myapp/config.py
   :language: python
   :linenos:

The ``PACKAGES`` defines the list of resuable packages that
Flask-AppFactory should load. The order of packages is important as templates,
translations etc. is loaded according to this order.

The ``EXTENSIONS`` defines the list of extensions that Flask-AppFactory
should load. You'll see that in addition to ``myexts.sqlalchemy`` we also
load ``flask_appfactory.ext.jinja2``. This extension is needed in order to make
the template loader aware of the order of packages. We also load
``flask_celeryext:FlaskCeleryExt``, which will be explained in detail in
Step 4 together with ``BROKER_URL``.


Application factory
-------------------
Next, we create our Flask `application factory <http://flask.pocoo.org/docs/latest/patterns/appfactories/>`_,
by using the ``flask_appfactory.appfactory()``. The ``appfactory``
method is passed:

- the name of the Flask application (line 7).
- the Python import path of our application configuration (line 8).
- whether to load just configuration or the entire application (line 9).
- and optional keyword arguments which will be merged with the configuration
  (line 10).

.. literalinclude:: ../examples/myapp/app.py
   :language: python
   :linenos:

The application factory will take care of loading all extensions and reusable
packages. In addition to the configuration provided in line 8, the factory
will try to load configuration from:

  1. Instance folder (``<instance folder>/<app name>.cfg``).
  2. The keyword arguments (``**kwargs_config``).
  3. Environment variables.

This allows you to have configuration for test/production environments or
ingesting configuration into the Flask application in e.g. docker containers.

Command Line Interface factory
------------------------------
Next, we create the CLI for our application that we can use to manage the
application and run e.g. the development server:

.. literalinclude:: ../examples/myapp/cli.py
   :language: python
   :linenos:

We simply import our application factory (line 5) and pass it to the
``flask_appfactory.clifactory()`` method (line 7).

The actual management script we install with an entry point in the package's
``setup.py`` (line 13):

.. literalinclude:: ../examples/setup.py
   :language: python
   :linenos:
   :emphasize-lines: 11-15

The new management script will besides your applications commands also have two
commands to 1) run a development server and 2) start a interactive Python shell
with the Flask application context.

.. code-block:: console

   $ myapp
   Usage: myapp [OPTIONS] COMMAND [ARGS]...

   Options:
     --help  Show this message and exit.

   Commands:
     initdb      Initialize database.
     run         Runs a development server.
     shell       Runs a shell in the app context.
     testapp     Command with application context.
     testsimple  Command without application context.

The command ``initdb`` was provided by our extension, while ``testapp`` and
``testsimple`` is provided by our reusable package.

.. note::
   It is also possible to use the ``flask`` command instead of creating a
   custom script. This can be achieved by creating a file ``manage.py``:

   .. literalinclude:: ../examples/manage.py
      :language: python
      :linenos:

   Next, export ``FLASK_APP`` environment variable and point it to your
   manage.py file:

   .. code-block:: console

      $ export FLASK_APP=/path/to/manage.py
      $ flask initdb

WSGI Application
----------------

Last but not least, you will likely need a WSGI file to run your service in
production environment:

.. literalinclude:: ../examples/myapp/wsgi.py
   :language: python
   :linenos:
