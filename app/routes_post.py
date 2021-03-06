from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment
from sqlalchemy import asc, desc
import datetime

post_bp = Blueprint("post", __name__, url_prefix="/posts")

@post_bp.route("/newpost", methods=["POST"])
def create_post():
    request_body = request.get_json()[0]
    date_time = datetime.datetime.utcnow()
    new_post = Post.from_json(request_body, date_time)
    db.session.add(new_post)
    db.session.commit()
    return make_response(new_post.make_post_json()), 200


@post_bp.route("/all", methods=["GET", "DELETE"])
def all_posts_all_users():
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    # if all_posts:
        # get all posts of all users
    if request.method == "GET":
        all_posts_response = []
        for post in all_posts:
            post_with_comments = make_post_response_with_comments(post)
            all_posts_response.append(post_with_comments)
        return jsonify(all_posts_response), 200
    
    # delete all posts of all users
    else:
        for post in all_posts:
            db.session.delete(post)
            db.session.commit()
        return {"details": "all posts were successfully deleted"}, 200

@post_bp.route("/<user_id>/all", methods=["GET", "DELETE"])
def all_posts_a_user(user_id): 
    all_posts = Post.query.filter_by(user_id=user_id).order_by(Post.date_posted.desc()).all()
    # get all posts of a specific user
    if request.method == "GET":
            all_posts_response = []
            for post in all_posts:
                post_with_comments = make_post_response_with_comments(post)
                all_posts_response.append(post_with_comments)
            return jsonify(all_posts_response), 200
    
    # delete all posts of a user
    else:
        for post in all_posts:
            db.session.delete(post)
            db.session.commit()
        return {"details": "all posts were successfully deleted"}, 200

@post_bp.route("/<post_id>", methods=["GET", "DELETE", "PUT", "PATCH"])
def a_post_a_user(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        # get all posts of a specific user
        if request.method == "GET":
            all_posts_response = []
            post_with_comments = make_post_response_with_comments(post)
            all_posts_response.append(post_with_comments)
            return jsonify(all_posts_response), 200
        
        # delete all posts of a user
        elif request.method == "DELETE":
            db.session.delete(post)
            db.session.commit()
            return {"details": "post was successfully deleted"}, 200

        elif request.method == "PUT":
            request_body = request.get_json()[0]
            post.title=request_body['title']
            post.text=request_body['text']
            db.session.commit()
            return jsonify(post.make_post_json()), 200
        
        elif request.method == "PATCH":
            post.likes = post.likes + 1
            db.session.commit()
            return jsonify(post.make_post_json()), 200
        
# helper function 
def make_post_response_with_comments(post):
    comments_to_post = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
    post_dict = post.make_post_json()
    post_dict["comments"] =  [comment.make_comment_json()for comment in comments_to_post]
    return post_dict 
    