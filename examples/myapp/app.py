# myapp/app.py

from flask_appfactory import appfactory

def create_app(load=True, **kwargs_config):
    return appfactory(
        "myapp",
        "myapp.config",
        load=load,
        **kwargs_config
    )
