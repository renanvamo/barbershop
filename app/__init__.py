from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
babel = Babel()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    babel.init_app(app)

    with app.app_context():
        from app import routes, models
        db.create_all()  # Cria o banco de dados e as tabelas

    return app

@babel.localeselector
def get_locale():
    return 'pt_BR'  # Define a localidade para pt_BR
