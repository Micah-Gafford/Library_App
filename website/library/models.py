from . import db
from flask_login import UserMixin

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(100))
  last_name = db.Column(db.String(100))
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))

class Book(db.Model):
  id = db.Column(db.Integer, primiary_key=True)
  title = db.Column(db.String(100), unique=True)
  checked_out = db.Column(db.Boolean)
  author = db.Column(db.String(100))


