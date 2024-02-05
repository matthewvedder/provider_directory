from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from celery import Celery

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
celery = Celery(__name__)

def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)
    ma.init_app(app)
    celery.conf.update(app.config)

    # Register Blueprints
    from .controllers.provider_controller import provider_blueprint
    app.register_blueprint(provider_blueprint, url_prefix='/api')

    return app
