from app import db
from flask import current_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    class_name = db.Column(db.String)
    campus = db.Column(db.String)
    about_me = db.Column(db.String)
    location = db.Column(db.String)
    secret = db.Column(db.String)