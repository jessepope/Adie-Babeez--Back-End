# # get all - sort(asc, dsc based on date), show me the most liked
# # delete a post (own post, delete all comments)
# # edit post (own post)
# # like post (update like count)
# # 

from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.post import Post
from app.models.user import User

post_bp = Blueprint("post", __name__, url_prefix="/posts")

@post_bp.route("", methods=["POST"])
def create_post():
    request_body = request.get_json()[0]
    try: 
        new_post = Post.from_json(request_body)
        db.session.add(new_post)
        db.session.commit()
        return make_response(new_post.make_post_json()), 200
    
    except:
        return {"error": "missing a key"}, 400


@post_bp.route("/all", methods=["GET", "DELETE"])
def all_posts():
    all_posts = Post.query.all()
    # get all posts
    if request.method == "GET":
        all_posts_response = [(post.make_post_json()) for post in all_posts]
        return jsonify(all_posts_response), 200
    
    # delete all users
    else:
        for post in all_posts:
            db.session.delete(post)
            db.session.commit()
        return {"details": "all posts were successfully deleted"}, 200



