from enum import unique
from sqlalchemy import VARCHAR
from app import db
from flask import current_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique= True, nullable=False)
    pronouns = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(50))
    campus = db.Column(db.String(50))
    bio = db.Column(db.String(100))
    location = db.Column(db.String(50))
    posts = db.relationship('Post', backref='user', lazy='dynamic', cascade='all,delete-orphan')
    
    # # constructor
    # def __init__(self, username, email, secret):
    #     self.username = username
    #     self.email = email
    #     self.secret = secret
    
    # we need all data to be sent back to FE to use for rendering user info
    def make_user_json(self):
        return {
                "user_id": self.id,
                "username": self.username,
                "pronouns": self.pronouns,
                "email": self.email, 
                "secret": self.secret,
                "class_name": self.class_name,
                "campus": self.campus,
                "bio": self.bio,
                "location": self.location,
                "posts": self.posts  
        }