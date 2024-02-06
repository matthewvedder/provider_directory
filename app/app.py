import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .utils.celery_utils import make_celery

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_filename=None):
    app = Flask(__name__)

    # Default configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Override default configuration with config file if given
    if config_filename:
        app.config.from_pyfile(config_filename)
    
    # Celery configuration
    app.celery = make_celery(app.name)
    app.celery.conf.update(app.config)

    # Ensure Celery tasks have Flask app context
    TaskBase = app.celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    app.celery.Task = ContextTask

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .controllers.provider_controller import provider_blueprint
    app.register_blueprint(provider_blueprint)

    return app