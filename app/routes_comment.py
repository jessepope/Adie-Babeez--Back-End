from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment
from sqlalchemy import asc, desc
import datetime

comment_bp = Blueprint("comment", __name__, url_prefix="/comments")

@comment_bp.route("/newcomment", methods=["POST"])
def create_comment():
    request_body = request.get_json()[0]
    date_time = datetime.datetime.utcnow()
    new_comment = Comment.from_json(request_body, date_time)
    db.session.add(new_comment)
    db.session.commit()
    return make_response(new_comment.make_comment_json()), 200

@comment_bp.route("/<comment_id>", methods=["GET", "DELETE", "PUT"])
def a_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        # get a comment
        if request.method == "GET":
            return jsonify(comment.make_comment_json()), 200
        
        # delete a comment
        elif request.method == "DELETE":
            db.session.delete(comment)
            db.session.commit()
            return {"details": "comment was successfully deleted"}, 200

        elif request.method == "PUT":
            request_body = request.get_json()[0]
            comment.text=request_body['text']
            db.session.commit()
            return jsonify(comment.make_comment_json()), 200

    