from app import db
from flask import current_app
import datetime
from app.models.user import User

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)
    
    
    def make_comment_json(self):
        user = User.query.get(self.user_id)
        return {
                "comment_id": self.id,
                "text": self.text, 
                "date_posted": self.date_posted,
                "user_id" : self.user_id,
                "post_id": self.post_id,
                "username" : user.username
        }
        
    @classmethod        # from FE to BE
    def from_json(cls, request_body, date_time):
        return cls(
            text=request_body['text'],
            user_id=request_body['user_id'],
            post_id=request_body['post_id'],
            date_posted = date_time,
            )
    

# make helper function to turn python object into json so comments can be sent with post requests (refer to line 36 in post routes)
