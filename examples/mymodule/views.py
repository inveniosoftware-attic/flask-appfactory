# mymodule/views.py

from flask import Blueprint, current_app, render_template

blueprint = Blueprint(
    'mymodule',
    __name__,
    template_folder='templates',
)

@blueprint.route("/")
def index():
    return render_template(
        'mymodule.html',
        greeting=current_app.config['MYMODULE_GREETING'],
    )
