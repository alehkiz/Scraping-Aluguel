from flask import Blueprint, current_app as app, render_template, url_for, redirect
from app.forms.tenement import Tenement

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = Tenement()
    if form.validate_on_submit():
        pass

    return render_template('index.html', form=form)