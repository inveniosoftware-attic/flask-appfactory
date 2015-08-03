==================
 Flask-AppFactory
==================

.. image:: https://travis-ci.org/inveniosoftware/flask-appfactory.svg?branch=master
    :target: https://travis-ci.org/inveniosoftware/flask-appfactory
.. image:: https://coveralls.io/repos/inveniosoftware/flask-appfactory/badge.svg?branch=master
    :target: https://coveralls.io/r/inveniosoftware/flask-appfactory
.. image:: https://pypip.in/v/flask-appfactory/badge.svg
   :target: https://crate.io/packages/flask-appfactory/
.. image:: https://pypip.in/d/flask-appfactory/badge.svg
   :target: https://crate.io/packages/flask-appfactory/

Flask-AppFactory is an dynamic application loader.

It allows you to build reusable modules that can be easily be assembled into
full Flask applications using this loader. Each reusable module can provide
default configuration, blueprints and command line interface.

Installation
============
Flask-AppFactory is on PyPI so all you need is: ::

    pip install Flask-AppFactory

Documentation
=============
Documentation is available at <http://flask-appfactory.readthedocs.org> or can be build using Sphinx: ::

    pip install Sphinx
    python setup.py build_sphinx

Testing
=======
Running the tests are as simple as: ::

    python setup.py test

or (to also show test coverage) ::

    ./run-tests.sh
