from os.path import abspath, dirname, join
from os import environ
import app


class BaseConfig(object):
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

class DevelopmentConfig(BaseConfig):
    ...

class ProductionConfig(BaseConfig):
    ...

config = {'development': DevelopmentConfig,
          'production': ProductionConfig}

