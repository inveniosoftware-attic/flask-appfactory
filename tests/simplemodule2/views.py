# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from __future__ import absolute_import, unicode_literals, print_function

from flask import Blueprint, render_template

blueprint = Blueprint(
    'simplemodule2',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@blueprint.route("/")
def index():
    return 'TEST'


@blueprint.route("/simplemodule2")
def template_test():
    return render_template('test.html')
