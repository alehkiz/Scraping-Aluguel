from flask import Blueprint, current_app as app, render_template


bp = Blueprint('api', __name__, url_prefix='/')

@bp.route('/get_price')
def get_price():
    '''TODO: Criar função para receber um json com os dados do apartamento, 
    calcular o valor do preço do aluguel e retornar em reais.
    '''
    ...
@bp.route('/get_bairro')
def get_bairro():
    '''Retorna os bairros cadastrads previamente'''
    ...