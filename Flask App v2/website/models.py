# we need a db model for our users, and another db model for our notes
from . import db # imports from current package, the db object. (the db = SQLAlchemy). should be the same as from website import db

from flask_login import UserMixin # custom class that inherits user object some things specific for our flask login
from sqlalchemy.sql import func # imported for line 11, stores default date and time

# need a class called Note
class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(5000))
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # type of column is integer, and by specifying foreign key, we must pass a valid id of an existing user to this column when we create a note object. 1 to many relationship. 1 user that has many notes. 1 object has amy children. 
# you put user.id. id is the primary key of the other object that you're referencing, could be id or email or name for example


# the class below is the User model. all users will be stored in a schema that looks like this. can have multiple users, all will have id, email, pw, fname
class User(db.Model, UserMixin): # whenever you make a new db model/store type of object, define name of object (User), then it will inherit from dbModel
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True) # need a str length
  password = db.Column(db.String(150))
  first_name = db.Column(db.String(150))
  notes = db.relationship('Note') # sets up relationship with Note table. it will be a list that represents all the different notes


# now that the database is setup by defining what it will look like, now we return to __init__.py and create the database