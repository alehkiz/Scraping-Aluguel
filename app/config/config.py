from os.path import abspath, dirname, join
from os import environ
import app
import locale

class BaseConfig(object):

    locale = locale
    locale.setlocale( locale.LC_ALL, 'Portuguese_Brazil.1252' )
    PROJECT_NAME = 'Vega'
    SITE_TITLE = environ.get('PROJECT_NAME') or 'Calculadora'
    SECRET_KEY = environ.get(
        'SERVER_KEY')
    APP_DIR = abspath(dirname(app.__file__))
    BASE_DIR = abspath(join(APP_DIR, '..'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
    SECURITY_CHANGEABLE = True
    BLUEPRINTS_DIR = join(APP_DIR, 'blueprints')
    LOG_DIR = join(BASE_DIR, r'logs')
    MODELS = join(BASE_DIR, r'models')
    ORDINAL_ENCODER = join(MODELS, 'ordinal_encoder.joblib')
    PIPELINE = join(MODELS, 'pipe_rfr.joblib')

class DevelopmentConfig(BaseConfig):
    ...

class ProductionConfig(BaseConfig):
    ...

config = {'development': DevelopmentConfig,
          'production': ProductionConfig}

