from crypt import methods
import email
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.user import User

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()[0]
    
    try: 
        new_user = User(username=request_body['username'], email=request_body['email'], secret=request_body['secret'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return make_response(new_user.make_user_json()), 200
    
    except KeyError as err:
        if "username" in err.args:
            return {"details" : f"Request body must include username with string type."}, 400
        if "email" in err.args:
            return {"details" : f"Request body must include email with string type."}, 400
        if "secret" in err.args:
            return {"details" : f"Request body must include secret with string type."}, 400
