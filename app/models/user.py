from enum import unique
from sqlalchemy import VARCHAR
from app import db
from flask import current_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique= True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100))
    campus = db.Column(db.String(100))
    about_me = db.Column(db.String(100))
    location = db.Column(db.String(100))
    
    # # constructor
    # def __init__(self, username, email, secret):
    #     self.username = username
    #     self.email = email
    #     self.secret = secret
        
    def make_user_json(self):
        return {
                "user_id": self.id,
                "username": self.username,
                "email": self.email, 
                "secret": self.secret
        }