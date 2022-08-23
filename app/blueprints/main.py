from asyncio.windows_utils import PipeHandle
from flask import Blueprint, current_app as app, render_template, url_for, redirect
from app.forms.tenement import Tenement
from app.kernel.sci import Pipeline

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = Tenement()
    if form.validate_on_submit():
        pipeline = Pipeline()
        pipeline.load(
            form.bedrooms.data, 
            form.bathrooms.data, 
            form.parking.data,
            form.area.data,
            form.neighborhood.data
            )
        predict = pipeline.predict()
        print(pipeline.data)
        print(pipeline.predict_value_real)
        return render_template('index.html', form=form, predict=predict)

    return render_template('index.html', form=form)