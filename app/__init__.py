from flask import Flask

from app.commands import register_commands
from app.config import Config
from app.extensions import db
from app.routes import catalog_bp, checkout_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(checkout_bp)
    register_commands(app)

    return app
