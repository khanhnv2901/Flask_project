from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import views
from flask_login import login_required, login_user, logout_user, current_user
from flask import session

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                session.permanent = True
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password, try again!', category='error')
        else:
            flash("User doesn't exist!", category='error')
    return render_template('login.html', user=current_user)

@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_name = request.form['user_name']

        user = User.query.filter_by(email = email).first()

        if user:
            flash('User existed!', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category='error')
        elif len(password) < 6:
            flash("Password must be greater than or equal 6 characters.", category='error')
        elif confirm_password != password:
            flash("Password doesn't match!", category='error')
        else:
            password = generate_password_hash(password,method='sha256')
            new_user = User(email, password, user_name)
            
            try:
                db.session.add(new_user)
                db.session.commit()
                
                flash("User created!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            except:
                "error"
    return render_template('signup.html', user=current_user)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

