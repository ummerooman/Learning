from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    db.init_app(app)

    # ensure tables are created
    with app.app_context():
        db.create_all()

    # register our routes blueprint
    from app.routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
