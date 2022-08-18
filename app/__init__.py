from flask import Flask
from app.core.configure import configure
from app.config.config import config


def create_app(mode='production'):
    app = Flask(__name__)
    app.config.from_object(config[mode])
    configure(app)
    return app