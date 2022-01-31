from enum import unique
from sqlalchemy import VARCHAR
from app import db
from flask import current_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique= True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), default="")
    campus = db.Column(db.String(100), default="")
    about_me = db.Column(db.String(100), default="")
    location = db.Column(db.String(100), default="")
    posts = db.relationship('Post', backref='user', lazy='dynamic', cascade='all,delete-orphan')
    
    # # # constructor
    # def __init__(self, username, email, secret):
    #     self.username = username
    #     self.email = email
    #     self.secret = secret
    
    
    @classmethod
    def from_json(cls, request_body):
        for key in request_body.keys():
            if key == "username":
                username = request_body['username']
            if key == "email":
                email = request_body['email']
            if key == "secret":
                secret = request_body['secret']
            if key == "class_name":
                class_name = request_body['class_name']
            if key == "campus":
                campus = request_body['class_name']
            if key == "about_me":
                about_me = request_body['about_me']
            if key == "location":
                location = request_body['location']
        return cls(
            username=username,
            email=email,
            secret=secret, 
            class_name = class_name, 
            campus = campus, 
            about_me = about_me, 
            location = location)
    

    def make_user_json(self):
        return {
                "user_id": self.id,
                "username": self.username,
                "email": self.email, 
                "secret": self.secret, 
                "class_name": 
        }