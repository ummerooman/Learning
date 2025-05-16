# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    db.init_app(app)

    # Import your models so that they’re registered on the metadata
    from app import models  

    with app.app_context():
        db.create_all()

    from app.routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
