from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Book, History
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    books = Book.query.filter_by(user_id=current_user.id).all()
    return_books = request.form.getlist("book")

    if request.method == 'POST':
        for returns in return_books:
            book = Book.query.filter_by(title=returns).first()
            book.user_id = None
            book.checked_out = False
            db.session.commit()
            flash('Books returned!', category='success')
        return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user, books=books)


@views.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():

    # handle add book "POST" request from front end
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')

        book = Book.query.filter_by(title=title).first()

        if book:
            flash('A book with this titile already exists.', category='error')
        elif len(title) < 1:
            flash('Please enter a title for the book.', category='error')
        elif len(author) < 1:
            flash('Please enter an author for the book', category='error')
        else:
            checked_out = False
            new_book = Book(title=title,
                            author=author,
                            checked_out=checked_out)
            db.session.add(new_book)
            db.session.commit()
            flash(f'{title} has been successfully added!')
            return redirect(url_for('views.home'))

    return render_template("add_book.html", user=current_user)


@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():

    if request.method == 'POST':

        history = History.query.filter_by(user_id=current_user.id).first()

        if not history:
            history = History(user_id=current_user.id)

        # get book titles from form to checkout
        for title in request.form.getlist("book"):
            book = Book.query.filter_by(title=title).first()
            book.checked_out = True
            book.user_id = current_user.id
            if book not in history.books:
                history.books.append(book)

        flash('Books have been successfully checked out!', category='success')
        db.session.commit()

        return redirect(url_for("views.home"))

    books = Book.query.filter_by(checked_out=False).all()
    return render_template("checkout.html", books=books, user=current_user)


@views.route('/history')
@login_required
def history():
    history = History.query.filter_by(user=current_user).first()
    books = history.books
    return render_template("history.html", user=current_user, books=books)
