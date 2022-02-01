from turtle import title
from xmlrpc.client import DateTime
from app import db
from flask import current_app
import datetime
import _tkinter
import sys

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    # date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    # location = db.Column(db.String(100))   # need api
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all,delete-orphan')
    

    def make_post_json(self):
        return {
                "post_id": self.id,
                "title": self.title,
                "text": self.text, 
                # "date_posted": self.date_posted,
                "likes": self.likes,
                # "location": self.location,
                "user_id": self.user_id
        }
        
    @classmethod        # from FE to BE
    def from_json(cls, request_body):
        return cls(
            title=request_body['title'],
            text=request_body['text'],
            # date_posted=request_body['date_posted'],
            likes=request_body['likes'],
            # comments=request_body['comments'],
            user_id=request_body['user_id']
            )
    
