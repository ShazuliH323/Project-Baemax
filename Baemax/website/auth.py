from flask import Blueprint, render_template, request , flash,redirect , url_for
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from .import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,Bio
from passlib.hash import sha256_crypt
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('incorrect password', category='error')
        else:
            flash('doesnt exist', category='error')

    return render_template("login.html" , user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']


        user = User.query.filter_by(username=username).first()
        
        if user:
            flash('username already exists', category='error')
        elif User.query.filter_by(email=email).first():
            flash('email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category ='error')
        elif password != confirmPassword:
            flash('Passwords do not match', category ='error')
        elif len(password) < 5:
            flash('Password must be greater than 5 characters', category ='error')
        else:
            #add user to database
            new_user = User(username=username , email = email , password= generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            print(new_user.id)
            new_bio = Bio(fullname=username , job="none" , bio="none" ,user_id=new_user.id )
            db.session.add(new_bio)
            db.session.commit()
            
            login_user(new_user, remember=True)
            
            flash('account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html" , user= current_user)