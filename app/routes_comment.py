# post a comment
# delete a comment (own comment or own post )  /** need to explore it */
# edit a comment (own comment)
# get all (sort by asc, dsc)


# # get all - sort(asc, dsc based on date), show me the most liked
# # delete a post (own post, delete all comments)
# # edit post (own post)
# # like post (update like count)
# # 

from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment

comment_bp = Blueprint("comment", __name__, url_prefix="/comments")

@comment_bp.route("/newcomment", methods=["POST"])
def create_comment():
    request_body = request.get_json()[0]
    # try: 
    new_comment = Comment.from_json(request_body)
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

    