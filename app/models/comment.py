# from app import db
# from flask import current_app
# import datetime

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     text = db.Column(db.String)
#     date_posted = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
#     post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)