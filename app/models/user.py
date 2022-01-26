from app import db
from flask import current_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)