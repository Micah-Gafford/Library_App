from . import db
from flask import Flask
from flask_login import UserMixin

# join table for history - book many-to-many relationship
books = db.Table(
    'histories_books',
    db.Column('history_id', db.Integer, db.ForeignKey('history.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')))


# schema for user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    books = db.relationship('Book', backref='user')
    history = db.relationship('History', backref='user')


# schema for book table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    checked_out = db.Column(db.Boolean)
    author = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# schema for history table
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    books = db.relationship('Book',
                            secondary=books,
                            backref='history',
                            lazy='select')
