from crypt import methods
import email
from ssl import OP_NO_RENEGOTIATION
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.user import User

user_bp = Blueprint("user", __name__, url_prefix="")


@user_bp.route("/signup", methods=["POST"])
def create_user():
    request_body = request.get_json()[0]

    try:
        new_user = User.from_json(request_body)
        db.session.add(new_user)
        db.session.commit()
        return make_response(new_user.make_user_json()), 200

    except KeyError as err:
        if "username" in err.args:
            return {"details": f"Request body must include username with string type."}, 400
        if "email" in err.args:
            return {"details": f"Request body must include email with string type."}, 400
        if "secret" in err.args:
            return {"details": f"Request body must include password with string type."}, 400


@user_bp.route("/users", methods=["GET", "DELETE"])
def all_users():
    # get all users
    if request.method == "GET":
        all_users = User.query.all()
        all_users_response = [(user.make_user_json()) for user in all_users]
        return jsonify(all_users_response), 200
    
    # delete all users
    else:
        all_users = User.query.all()
        for user in all_users:
            db.session.delete(user)
            db.session.commit()
        return {"details": "all users were successfully deleted"}, 200


@user_bp.route("/users/profile", methods=["GET", "DELETE", "PUT"])

# since we store user data in global state variable currentUser, we will not use userid in URL
# instead, user info will be stored in global variable and used to render, so URL will be only /profile
# we need to update and test this when we build the profile in FE
def edit_a_specific_users():
    request_body = request.get_json()[0]
    user_id = request_body["id"]  # need to confirm the key name
    user = User.query.get(user_id)
    # get a user
    if request.method == "GET":
        if user:
            return user.make_user_json(), 200
        else:
            return {"details": f"User {user_id} not found"}, 404
        
    # delete a user
    elif request.method == "DELETE":
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"details": "User was successfully deleted"}, 200
        else:
            return {"details": f"User {user_id} not found"}, 404
        
    # update a user's profile
    elif request.method == "PUT":
        if user:
            user.username=request_body['username'],
            user.email=request_body['email'],
            user.secret=request_body['secret'],
            user.pronouns=request_body['pronouns'],
            user.class_name=request_body['className'],
            user.campus=request_body['campus'],
            user.bio=request_body['bio'],
            user.location=request_body['location']
            db.session.commit()
            return make_response(user.make_user_json()), 200
        else:
            return  {"details": f"User {user_id} not found"}, 404


@user_bp.route("/login", methods=["GET"])
def verify_a_specific_user():
    request_body = request.get_json()[0]
    if len(request_body) < 2:
        return jsonify([{"message": "missing email/username or password"}]), 404
    
    for key in request_body.keys():
        if key == "email":
            input_email = request_body['email']
            user = User.query.filter_by(email=input_email).first()
        if key == "secret":
            input_secret = request_body['secret']
    if user:
        if user.secret == input_secret:
            # send user dict back to use in FE to render user data
            return user.make_user_json(), 200
        else:
            return jsonify([{"message": "invalid password"}]), 400
    else:
        return jsonify([{"message": "invalid username or email"}]), 400


# @user_bp.route("", methods=["DELETE"])
# def delete_all_user():
#     all_users = User.query.all()
#     for user in all_users:
#         db.session.delete(user)
#         db.session.commit()
#     return {"details": "all users were successfully deleted"}, 200




# since we store user data in global state variable currentUser, we will not use userid in URL
# instead, user info will be stored in global variable and used to render, so URL will be only /delete
# we need to update and test this when we build the profile in FE and add a delete my profile button
# @user_bp.route("/<user_id>", methods=["DELETE"])
# def delete_a_specific_user(user_id):
#     try:
#         user = User.query.get(user_id)
#         db.session.delete(user)
#         db.session.commit()
#         return {"details": "User was successfully deleted"}, 200
#     except:
#         return {"details": f"User {user_id} not found"}, 404



# since we store user data in global state variable currentUser, we will not use userid in URL
# instead, user info will be stored in global variable and used to render, so URL will be only /updateprofile
# we need to update and test this when we build the profile in FE and add a update my profile button
# @user_bp.route("/profile/<user_id>", methods=["PUT"])



# update /patch user's info

# username: Mary
# email:elly@ elly.com
# password: 123
# campus: Maple
# about_me: Hi


# update user's location with google api
