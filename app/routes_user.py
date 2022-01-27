from crypt import methods
import email
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.user import User

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/signup", methods=["POST"])
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


@user_bp.route("", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    all_users_response = [(user.make_user_json()) for user in all_users]
    return jsonify(all_users_response), 200

@user_bp.route("/<user_id>", methods=["GET"])
def get_a_specific_users(user_id):
    try: 
        user = User.query.get(user_id)
        return user.make_user_json(), 200;
    except:
        return  {"details": f"User {user_id} not found"}, 404

@user_bp.route("/login/verify", methods=["GET"])
def verify_a_specific_user():
    request_body = request.get_json()[0]
    # input_username = request_body['username']
    input_email = request_body['email']
    input_secret = request_body['secret']

    if input_email:
        user = User.query.filter_by(email = input_email).first()
    # elif input_username:
    #     user = User.query.filter(username = input_username).first()
    if user:
        if user.secret == input_secret:
            return jsonify([{"message":"login successfully"}]), 200
        else:
            return jsonify([{"message":"invalid password"}]), 400
    else:
        return jsonify([{"message":"invalid username or email"}]), 400


@user_bp.route("", methods=["DELETE"])
def delete_all_user():
    all_users = User.query.all()
    for user in all_users:
        db.session.delete(user)
        db.session.commit()
    return {"details": "all users were successfully deleted"}, 200
