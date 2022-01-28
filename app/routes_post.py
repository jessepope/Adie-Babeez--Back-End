# get all - sort(asc, dsc based on date), show me the most liked
# delete a post (own post, delete all comments)
# edit post (own post)
# like post (update like count)
# 

from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.post import Post
from app.models.user import User

post_bp = Blueprint("post", __name__, url_prefix="/posts")

@post_bp.route("", methods=["POST"])
def create_post():
    request_body = request.get_json()[0]
    try: 
        new_post = Post(
            username=request_body['username'], 
            email=request_body['email'], 
            secret=request_body['secret']
            )
        
        db.session.add(new_post)
        db.session.commit()
        
        return make_response(new_post.make_user_json()), 200
    
    except KeyError as err:
        if "username" in err.args:
            return {"details" : f"Request body must include username with string type."}, 400
        if "email" in err.args:
            return {"details" : f"Request body must include email with string type."}, 400
        if "secret" in err.args:
            return {"details" : f"Request body must include secret with string type."}, 400




