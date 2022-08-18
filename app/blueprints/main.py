from flask import Blueprint, current_app as app, render_template, url_for, redirect


bp = Blueprint("main", __name__, url_prefix="/")

@bp.route('/')
def index():
    return render_template('index.html')