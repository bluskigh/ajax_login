"""
TODO:
    - Use JWTs when signing in the user / deleting user account (validity)
    - ajax api calls to to get information
"""
from flask import Flask, redirect, session, render_template, request, jsonify, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# init app with current directory name
app = Flask(__name__)
# config from the file config.py
app.config.from_object('config')
# connecting to the database
db = SQLAlchemy(app)

# setting up migration for schemas defined in this file
Migrate(app, db)

#----
#Models
#----
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

# create all

@app.route('/')
def index():
    if session.get('userid'):
        return render_template('signedin.html')
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('/forms/layout.html', endpoint='/signin', title='Sign In')
@app.route('/signin', methods=['POST'])
def signin_submission():
    username = request.form.get('username')
    password = request.form.get('password')
    user = db.session.query(User).filter(User.username==username).one_or_none()
    if user is None:
        flash('User was not found...', 'error');
    if not check_password_hash(user.password, password):
        flash('Invalid password', 'error')
        return redirect('/signin')
    
    flash('Signed in!', 'success')
    session['userid'] = user.id
    return redirect('/')

@app.route('/signup')
def signup():
    return render_template('/forms/layout.html', endpoint='/signup', title='Sign Up')

@app.route('/signup', methods=['POST'])
def signup_submission():
    """
    Not to be used as an api call, used after form is submitted.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation') 
    # attempt to find the user
    user = db.session.query(User).filter(User.username==username).one_or_none()
    if user is not None:
        flash('Username already in use', 'error')
        return redirect('/signup')

    # check password with confirmation
    if password is None:
        flash('Did not provide password', 'error')
        return redirect('/signup')
    if confirmation is None:
        flash('Did not provide confirmation.', 'error')
        return redirect('/signup')
    if password != confirmation:
        # TODO: try returning the password and confirmation, but hide let user hover over to see them
        flash('Password and confirmation do not match', 'error')
        return redirect('/signup')

    try:
        # create new user
        pw_hash = generate_password_hash(password)
        # transient stage
        user = User(username=username, password=pw_hash)
        # pending stage
        db.session.add(user)
        # committed stage
        db.session.commit()
        flash('user created.', 'success')
        return redirect('/')
    except Exception as e:
        print(e)
        db.session.rollback()
        flash('Internal server error.', 'info')
        return redirect('/signup')

#---
# Api Calls
#---
@app.route('/username_exists/<string:username>')
def check_username(username):
    if len(username) == 0:
        return jsonify({'message': 'Please provide a valid username.'}), 401

    user = db.session.query(User).filter(User.username==username).one_or_none()
    if user is not None:
        return jsonify({'exists': True}), 404
    return jsonify({'exists': False}), 200

@app.route('/signout')
def signout():
    session.clear()
    flash('You\'re now signed out', 'info')
    return redirect('/')
