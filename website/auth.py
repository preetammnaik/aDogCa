from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if check_password_hash(user.password, password):
                flash('Loggedin successfully', category='success')
                login_user(user, remember=True)
                print(user.userType)
                if user.userType == 'buyer':
                    return redirect(url_for('views.home_buyer'))
                elif user.userType == 'seller':
                    return redirect(url_for('views.home_seller'))
            else:
                flash('Incorrect Password, Try again', category='error')
        else:
            flash('Email does not exist', category="error")
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        userType = request.form.get('userType')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email address must be greater than 3 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password is too short', category='error')
        else:
            new_user = User(email=email, firstName=firstName, userType=userType,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            if new_user.userType == 'buyer':
                return redirect(url_for('views.home_buyer'))
            elif new_user.userType == 'seller':
                return redirect(url_for('views.home_seller'))

    return render_template('register.html', user=current_user)
