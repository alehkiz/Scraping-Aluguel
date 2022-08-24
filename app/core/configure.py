from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask.cli import with_appcontext
from app.blueprints import register_blueprints
from app.core.db import db
from app.models.app import Immobile

migrate = Migrate()
csrf = CSRFProtect()

def configure(app):
    register_blueprints(app)
    migrate.init_app(app, db)
    db.init_app(app)
    csrf.init_app(app)
    @app.shell_context_processor
    @with_appcontext
    def make_shell_context():
        app.config['SERVER_NAME'] = 'localhost'
        ctx = app.test_request_context()
        ctx.push()
        return dict(db=db, app=app, Immobile=Immobile)
    return app