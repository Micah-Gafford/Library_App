from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

def create_app():
  """ Construct the core application."""
  app = Flask(__name__, instance_relative_config=False)
  app.config['SECRET_KEY'] = 'mysecretkey'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import User

  create_database(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))

  return app

def create_database(app):
  if not path.exists('website/library/library.db'):
    db.create_all(app=app)
    print('created database!')
