from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods = ['POST', 'GET'])
def signup():
  if request.method == 'POST':
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = User.query.filter_by(email=email).first()

    if user:
      flash('Email already in use.', category='error')
    elif len(first_name) < 1:
      flash('First Name must include characters', category='error')
    elif len(last_name) < 1:
      flash('Last name must include characters', category='error')
    elif password1 != password2:
      flash('Passwords do not match', category='error')
    elif len(password1) < 8:
      flash('Password must be longer than 7 characters', category='error')
    else:
      hashed_password = generate_password_hash(password1, 'sha256')
      new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
      flash('Account Created!', category='success')
      return redirect(url_for('views.home'))

  return render_template("signup.html")

@auth.route('/login')
def login():
  return render_template("login.html")