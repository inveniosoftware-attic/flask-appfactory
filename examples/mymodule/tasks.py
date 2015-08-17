# mymodule/tasks.py

from celery import shared_task
from flask import current_app, request
from flask_celeryext import RequestContextTask


@shared_task
def appctx():
    current_app.logger.info(current_app.config['BROKER_URL'])


@shared_task(base=RequestContextTask)
def reqctx():
    current_app.logger.info(request.method)
