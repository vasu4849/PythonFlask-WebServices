from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users' #if we don't specify it then class name would be used as tablename implicitly

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    #represent the output data to be displayed in str format
    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password
        })
    
    #this would verify if the username and password entered by user matches or not. Returns a boolean value
    def username_password_match(_username, _password):
        user = Users.query.filter_by(username=_username).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True
    
    # get list of all users
    def getAllUsers():
        return Users.query.all()         #this would print the data in repr format as shown below

    #create a new user
    def createUser(_username, _password):
        new_user = Users(username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()
    

    
