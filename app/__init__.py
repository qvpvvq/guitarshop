from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager

migrate = Migrate()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Указываем Flask, что шаблоны и статика теперь в других местах относительно этого файла
    app = Flask(__name__, 
                template_folder='templates', 
                static_folder='../static')
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'super-secret-key-123'
    # База будет лежать в корне проекта, на один уровень выше папки app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, '..', 'guitar.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    db.init_app(app)
    migrate.init_app(app, db)


    login_manager.init_app(app)
    login_manager.login_view = 'login' 
    with app.app_context():
        # Важно: импортируем маршруты ВНУТРИ контекста, чтобы избежать циклической ссылки
        from . import routes
        from .models import Guitar, User
        
    return app

    