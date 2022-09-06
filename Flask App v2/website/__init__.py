# this file makes the website folder a python package
# it imports the folder and whatever is inside the init.py will run automatically
# the __init__.py specifically makes the folder a python package that can
# be imported into other files
# sets up flask application
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # used for the database
from flask_login import LoginManager

db = SQLAlchemy() # initializes and defines a new db
DB_NAME = "database.db" # names the database database.db

def create_app():
  application = Flask(__name__)
  application.config['SECRET_KEY'] = 'hellohello' # secret key for my app
  application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # python code inside squiggly brackets and is evaluated as a string
  # code above, SQLAlchemy database is stored at sqlite:///{dbname} location
  # it stores the database in the website folder
  # now initialize db by giving it our flask app
  db.init_app(application)

  # now we define database models - the schema of what this db will look like


  # we then have to register our blueprints in init.py
  # we have to tell flask we have views and routes for the app, so here's where they are
  from .views import views
  from .auth import auth
  # then we register the blueprints with our flask app
  application.register_blueprint(views, url_prefix='/')
  application.register_blueprint(auth, url_prefix='/')
  # what the lines above are saying is all the url's that are stored inside of these blueprints file, how do we access them

  # after registering the blueprints and models.py schema is setup, we return here and create the database
  # we import models so that it defines the classes in models.py
  from .models import User, Note

  create_database(application)

  login_manager = LoginManager() # helps manage users
  login_manager.login_view = 'auth.login' # so should flask redirect us if not logged in?
  login_manager.init_app(application) # tells the login manager which app we are using

  @login_manager.user_loader # this tells flask how we load a user
  def load_user(id):
    return User.query.get(int(id)) # works similar to filter by, except by default query.get looks for the primary key, which checks the int version of whatever id is passed into load_user(id)

  return application


def create_database(application): # checks if database exists, if not, create one, if yes, don't override it because it has data in it already
  if not path.exists('website/' + DB_NAME):
    db.create_all(app=application)
    print('Created Database!')
    