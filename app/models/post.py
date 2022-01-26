from xmlrpc.client import DateTime
from app import db
from flask import current_app
import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    date_posted = db.Column(db.datetime)
    likes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
