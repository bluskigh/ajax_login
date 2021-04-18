"""
TODO:
    - Use JWTs when signing in the user / deleting user account (validity)
    - ajax api calls to to get information
"""
from flask import Flask, redirect, session, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('/forms/layout.html', endpoint='/signin', title='Sign In')
@app.route('/signin', methods=['POST'])
def signin_submission():
    username = request.form.get('username')
    password = request.form.get('password')
    print(username, password)
    return redirect('/signin')

@app.route('/signup')
def signup():
    return render_template('/forms/layout.html', endpoint='/signup', title='Sign Up')

@app.route('/signup', methods=['POST'])
def signup_submission():
    pass

