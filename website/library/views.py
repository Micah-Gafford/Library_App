from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
  return render_template("home.html", user=current_user)

@views.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():

  # if request.method == 'POST':
  #   title = request.form.get('title')

  return render_template("add_book.html", user=current_user)
