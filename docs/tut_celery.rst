Step 4: Celery based background tasks
=====================================

Flask-AppFactory includes optional support for Celery integration via the
`Flask-CeleryExt <http://flask-celeryext.readthedocs.org>`_ extension. If you
wish to use it, be sure to install Flask-AppFactory like this::

    pip install Flask-AppFactory[celery]

To enable Celery support we add one file to our application package, and one
file to our reusable package::

    myapp/celery.py
    mymodule/tasks.py


Configuration
-------------
In our configuration we first have to add the Flask-CeleryExt extension
(line 5) as well as define the Celery broker via the ``BROKER_URL`` variable
(line 13). Note in this example we use a local Redis installation. For other
options see the Celery documentation.

.. literalinclude:: ../examples/myapp/config.py
   :language: python
   :linenos:
   :emphasize-lines: 5, 13

The Flask-CeleryExt takes care of creating a minimal Celery application with
the correct configuration so Celery knows e.g. which broker to use. In addition
the minimal Celery application doesn't load any tasks to ensure faster startup
time.

See the `Celery documentation
<http://celery.readthedocs.org/en/latest/configuration.html>`_ for all the
possible configuration variables.

Celery application
------------------
Next, we create a small Celery application which is later used to start the
Celery worker from.

.. literalinclude:: ../examples/myapp/celery.py
   :language: python
   :linenos:

Reusable tasks
--------------
The reusable packages can easily define Celery tasks by adding a ``tasks.py``
file like this:

.. literalinclude:: ../examples/mymodule/tasks.py
   :language: python
   :linenos:
   :emphasize-lines: 8, 13


Notice the use of ``@shared_task`` decorator (line 8). This ensures that the
task can be reused by many different Celery applications. The Celery
application created above takes care of register the tasks.

Each task is executed within a Flask application context (notice the use of
e.g. ``current_app``). If you need to have a task executed in a request context
(e.g. if you need to ensure before first request functions have been run), you
just have to change the base class to use the ``RequestContextTask`` (line 13).

Running the worker
------------------

Next, you can start a Celery worker by simply pointing Celery to your new
Celery application in ``myapp.celery``:

.. code-block:: console

   $ celery worker -A myapp.celery


Sending tasks
-------------

Executing tasks requires you to have your Flask application initialized, hence
simply start a Python shell using your management script:

.. code-block:: console

   $ myapp shell
   ...
   >>> from mymodule.tasks import appctx
   >>> appctx.delay()
