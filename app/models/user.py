from enum import unique
from sqlalchemy import VARCHAR
from app import db
from flask import current_app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique= True, nullable=False)
    pronouns = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(50))
    campus = db.Column(db.String(50))
    bio = db.Column(db.String(100))
    posts = db.relationship('Post', backref='user', lazy='dynamic', cascade='all,delete-orphan')

    
    @classmethod        # from FE to BE
    def from_json(cls, request_body):
        return cls(
            username=request_body['username'],
            email=request_body['email'],
            password=request_body['password'],
            pronouns=request_body['pronouns'],
            class_name=request_body['class_name'],
            campus=request_body['campus'],
            bio=request_body['bio'],)
    
    # from BE to FE
    def make_user_json(self):
        return {
                "user_id": self.id,
                "username": self.username,
                "pronouns": self.pronouns,
                "email": self.email, 
                "password": self.password,
                "class_name": self.class_name,
                "campus": self.campus,
                "bio": self.bio,
                # "posts": self.posts  
        }