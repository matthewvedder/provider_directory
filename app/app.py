import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_filename=None):
    app = Flask(__name__)

    # Default configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Override default configuration with config file if given
    if config_filename:
        app.config.from_pyfile(config_filename)

    db.init_app(app)
    ma.init_app(app)

    # Import and register Blueprints here, if any
    # from yourapplication.some_module import some_blueprint
    # app.register_blueprint(some_blueprint)

    return app