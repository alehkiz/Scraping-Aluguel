from flask import Flask
from app.core.configure import configure

def create_app(mode='production'):
    app = Flask(__name__)
    # app.config.from_object(config[mode])
    configure(app)
    return app