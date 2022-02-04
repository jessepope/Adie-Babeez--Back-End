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


@comment_bp.route("/<post_id>/all", methods=["GET", "DELETE"])
def all_comments_one_post(post_id):
    all_comments = Comment.query.filter_by(post_id=post_id).all()
    # get all comments of a specific post
    if request.method == "GET":
        all_comments_response = [(comment.make_comment_json()) for comment in all_comments]
        return jsonify(all_comments_response), 200
    
#     # delete all comments of a post
#     else:
#         for comment in all_comments:
#             db.session.delete(comment)
#             db.session.commit()
#         return {"details": "all comments were successfully deleted"}, 200




# @comment_bp.route("/<post_id>", methods=["GET", "DELETE", "PUT"])
# def a_post_a_user():
#     request_body = request.get_json()[0]
#     user_id = request_body["user_id"]
#     post_id = request_body["post_id"]  
#     post = Post.query.filter_by(user_id=user_id, post_id=post_id)
#     if post:
#         # get all posts of a specific user
#         if request.method == "GET":
#             return jsonify(post.make_post_json()), 200
        
#         # delete all posts of a user
#         elif request.method == "DELETE":
#             db.session.delete(post)
#             db.session.commit()
#             return {"details": "post was successfully deleted"}, 200

#         elif request.method == "PUT":
#             post.title=request_body['title']
#             post.text=request_body['text']
#             post.user_id=request_body['user_id']
#             return jsonify(post.make_post_json()), 200

# def make_post_response_with_comments(post):
#     post_dict = post.make_post_json()
#     comments_to_post = Comment.query.filter_by(post_id=post.id).all()
#     post_dict["comments"] =  [comment.make_comment_json()for comment in comments_to_post]
#     return post_dict 
    