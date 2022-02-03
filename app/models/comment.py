from app import db
from flask import current_app
import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String)
    date_posted = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)
    
    
    # def make_comment_json(self):
    #     return {
    #             "comment_id": self.id,
    #             "text": self.text, 
    #             "date_posted": self.date_posted,
    #             "user_id" : self.user_id,
    #             "post_id": self.post_id
    #     }
        
    # @classmethod        # from FE to BE
    # def from_json(cls, request_body):
    #     return cls(
    #         title=request_body['title'],
    #         text=request_body['text'],
    #         # date_posted=request_body['date_posted'],
    #         # comments=request_body['comments'],
    #         user_id=request_body['user_id']
    #         )
    
