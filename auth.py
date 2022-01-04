from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        print("user w", email, password, remember)

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No account with that email exists.", category="warning")
            return redirect(url_for('auth.login'))
        
        if not check_password_hash(user.password, password):
            flash("The password entered is incorrect.", category="warning")
            return redirect(url_for('auth.login'))
        
        # user can be successfully logged in
        login_user(user, remember=remember) # provided by flask_login
        flash("Logged in. Hello!", category="info")
        return redirect(url_for('main.profile'))

    else:
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user() # provided by flask_login
    flash("Logged out. Goodbye!", category="info")
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        # validate and add user to database
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        password_confirm = request.form.get('password-confirm')

        # check if password and password-confirm match
        if password != password_confirm:
            flash('The passwords do not match.', category="warning")
            return redirect(url_for('auth.signup'))

        user = User.query.filter_by(email=email).first()

        # user already exists, try again
        if user:
            # send message to next request (redirect)
            flash('A user already exists with this email.', category="warning")
            return redirect(url_for('auth.signup'))

        # create new user with hashed password
        new_user = User(email=email, name=name, password=generate_password_hash(password, "sha256"))

        # add new user to database
        print(f"Adding user with email {email}, name: {name}, password: {password}")
        db.session.add(new_user)
        db.session.commit()

        # redirects user to login page after successful signup
        flash("Signed up successfully! Please log in.", category="info")
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')