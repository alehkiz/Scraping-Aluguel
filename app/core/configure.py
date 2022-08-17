from app.blueprints import register_blueprints


def configure(app):
    register_blueprints(app)
    return app