from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from os import path
import os

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=False)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)


def create_app():
    """ Construct the core application."""
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
    cwd = os.getcwd()
    if not path.exists(cwd + '\library\library.db'):
        db.create_all(app=app)
        print('created database!')


@app.cli.command('initdb')
def reset_database():
    """ Reset Database to default """
    db.drop_all()
    db.create_all()

    print('reset database')


@app.cli.command('bootstrap')
def boostrap():
    """ Populate database with boostrap data """
    db.drop_all()
    db.create_all()

    from .models import User, Book
    password = generate_password_hash('password', 'sha256')

    db.session.add(
        User(first_name='Max',
             last_name='Mcdaniels',
             email='max@gmail.com',
             password=password))

    db.session.add(
        User(first_name='Lindon',
             last_name='Cradle',
             email='lindon@gmail.com',
             password=password))

    db.session.add(
        User(first_name='Daniel',
             last_name='Black',
             email='daniel@gmail.com',
             password=password))

    db.session.add(
        Book(title="The Wise Man's Fear",
             author='Patrick Rothfuss',
             checked_out=False))

    db.session.add(
        Book(title='The Hound of Rowan',
             author='Henry Neff',
             checked_out=False))

    db.session.add(Book(title='Cradle', author='Will Wight',
                        checked_out=False))

    db.session.commit()

    print('Populated database!')
