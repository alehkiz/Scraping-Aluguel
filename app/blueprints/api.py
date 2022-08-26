import json
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
        im.price = predict['original']
        db.session.add(im)
        db.session.commit()
        return jsonify({'valor': predict['monetary'],
                        'id': im.id,
                        'url_validate': url_for('api.validate', id=im.id, type=True),
                        'url_correct': url_for('api.correct', id=im.id)})
    return abort(404)
@bp.route('/validate/<int:id>/<type>')
def validate(id:int, type: str):
    '''Valida um determinado ID'''
    im = Immobile.query.filter(Immobile.id == id).first_or_404()
    if not im.validate is None:
        return jsonify({'status': False, 'message':'Validação já feita, não é possível alterar'})
    if type == 'VALID':
        im.validate = True
    else:
        im.validate = False
    db.session.commit()
    return jsonify({'status':True})

@bp.route('correct/<int:id>', methods=['POST'])
def correct(id: int):
    'Corrige o valor do aluguel de acordo com informação inserida pelo usuário.'
    print(request.form.get('input-correct-value'))
    im = Immobile.query.filter(Immobile.id == id).first_or_404()
    if request.form.get('input-correct-value', False) != False:
        im.correct_value = request.form.get('input-correct-value')
        db.session.commit()
        return jsonify({'status': True})
    return jsonify({'status': False})