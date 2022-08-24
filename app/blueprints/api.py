from flask import Blueprint, current_app as app, render_template, request, jsonify, abort, url_for

from app.forms.tenement import Tenement
from app.kernel.sci import Pipeline
from app.models.app import Immobile
from app.core.db import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/get_price', methods=['POST'])
def get_price():
    '''TODO: Criar função para receber um json com os dados do apartamento, 
    calcular o valor do preço do aluguel e retornar em reais.
    '''
    form = Tenement()
    im = Immobile()
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
        im.bedrooms = form.bedrooms.data
        im.bathrooms = form.bathrooms.data
        im.parking = form.parking.data
        im.area = form.area.data
        im.s_neighborhood = form.neighborhood.data 
        im.neighborhood = pipeline.get_neighborhood_id(im.s_neighborhood)
        db.session.add(im)
        db.session.commit()
        return jsonify({'valor': predict,
                        'id': im.id,
                        'url_validate': url_for('api.validate', id=im.id, type=True)})
    return abort(404)
@bp.route('/validate/<int:id>/<type>')
def validate(id:int, type: str):
    '''Valida um determinado ID'''
    im = Immobile.query.filter(Immobile.id == id).first_or_404()
    if type == 'VALID':
        im.validate = True
    else:
        im.validate = False
    db.session.commit()
    return {'status':True}