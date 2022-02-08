from app import db
from flask import current_app
import datetime
from app.models.user import User

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all,delete-orphan')
    

    def make_post_json(self):
        user = User.query.get(self.user_id)
        return {
                "post_id": self.id,
                "title": self.title,
                "text": self.text, 
                "date_posted": self.date_posted,
                "likes": self.likes,
                "user_id": self.user_id, 
                "username" :  user.username
        }
        
    @classmethod        # from FE to BE
    def from_json(cls, request_body, date_time):
        return cls(
            title=request_body['title'],
            text=request_body['text'],
            user_id=request_body['user_id'], 
            date_posted = date_time
            )
    
