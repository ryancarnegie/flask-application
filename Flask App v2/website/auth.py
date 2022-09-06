from flask import Blueprint
from flask import render_template
from flask import request # to get information from the <form> on the server
from flask import flash
from .models import User # this is User from models.py
from werkzeug.security import generate_password_hash, check_password_hash 
from . import db
from flask import redirect, url_for # had to import redirect to redirect users
from flask_login import login_user, login_required, logout_user, current_user # flask functions

auth = Blueprint('auth', __name__) # auth blueprint

# in auth.py we define login, logout, and signup
# setting up the routes and url's
# routes need to know if we send them a get request, a post request, etc
# based on the type of request, each route will do something differently.
@auth.route('/login', methods=['GET', 'POST']) # we make sure login and signup can accept post requests and we do that by defining inside of the root that says methods = a list of strings of GET and POST
def login():
  if request.method == 'POST': # this checks if we are actually signed in, and if we are signing in, we want the email and the password from the form
    email = request.form.get('email')
    password = request.form.get('password1')
    # User is the database name
    user = User.query.filter_by(email=email).first() # this means filter all the users that have this email to check if it exists in the db.
    if user:
      if check_password_hash(user.password, password):
        flash('Logged in successfully!', category='success')
        login_user(user, remember=True) # the user on line 24 that we found, we pass in here to log in this user
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password', category='error')
    else:
      flash('Email does not exist!', category='error')

  data = request.form
  print(data)
  # return render_template('login.html', hello="Welcome,", user="Ryan", boolean=True)
  # return render_template('login.html', hello="Welcome,", user="Ryan", boolean=True) this was before we added auth to base.html
  return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    email = request.form.get('email')
    first_name = request.form.get('firstName')
    # lastName = request.form.get('lastName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = User.query.filter_by(email=email).first()
    if user:
      flash('User/email already exists!', category='error')
    # flash is part of flask. categories are part of flash
    elif len(email) < 4:
      flash('Email must be greater than 3 characters', category='error')
    elif len(first_name) < 2:
      flash('Name must be greater than 2 characters', category='error')
    elif password1 != password2:
      flash("Passwords don\'t match", category='error')
    elif len(password1) < 3:
      flash("Passed must be greater than 3 characters", category='error')
    # elif password1.isdigit():
    #   flash("Password must not only be numbers", category='error')
    else:
      new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')) # sha 256 is a hasing algorithm
      db.session.add(new_user) # adds the user to the database, then, 
      db.session.commit() # we made changes to the database, so commit updates it
      flash("Account successfully created!", category='success')
      login_user(new_user, remember=True)
      return redirect(url_for('views.home'))

  return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))