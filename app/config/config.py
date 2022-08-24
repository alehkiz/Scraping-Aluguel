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

    _SQLALCHEMY_DATABASE_NAME = environ.get('DATABASE', False) or PROJECT_NAME.lower()
    _SQLALCHEMY_DATABASE_HOST = environ.get('DB_HOST')
    _SQLALCHEMY_DATABASE_USERNAME = environ.get('DB_USER')
    _SQLALCHEMY_DATABASE_PASSWORD = environ.get('DB_PASS')
    _SQLALCHEMY_DATABASE_PORT = environ.get('DB_PORT')
    

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{BaseConfig._SQLALCHEMY_DATABASE_USERNAME}:{BaseConfig._SQLALCHEMY_DATABASE_PASSWORD}@{BaseConfig._SQLALCHEMY_DATABASE_HOST}:{BaseConfig._SQLALCHEMY_DATABASE_PORT}/{BaseConfig._SQLALCHEMY_DATABASE_NAME}'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{BaseConfig._SQLALCHEMY_DATABASE_USERNAME}:{BaseConfig._SQLALCHEMY_DATABASE_PASSWORD}@{BaseConfig._SQLALCHEMY_DATABASE_HOST}:{BaseConfig._SQLALCHEMY_DATABASE_PORT}/{BaseConfig._SQLALCHEMY_DATABASE_NAME}'

config = {'development': DevelopmentConfig,
          'production': ProductionConfig}

