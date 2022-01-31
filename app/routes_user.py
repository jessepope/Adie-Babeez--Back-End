from crypt import methods
import email
from ssl import OP_NO_RENEGOTIATION
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.user import User

user_bp = Blueprint("user", __name__, url_prefix="/users")


@user_bp.route("/signup", methods=["POST"])
def create_user():
    request_body = request.get_json()[0]

    try:
        new_user = User(username=request_body['username'],
                        email=request_body['email'],
                        secret=request_body['secret'],
                        pronouns=request_body['pronouns'],
                        class_name=request_body['className'],
                        campus=request_body['campus'],
                        bio=request_body['bio'],
                        location=request_body['location']
                        )

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


@user_bp.route("", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    all_users_response = [(user.make_user_json()) for user in all_users]
    return jsonify(all_users_response), 200



# since we store user data in global state variable currentUser, we will not use userid in URL
# instead, user info will be stored in global variable and used to render, so URL will be only /profile
# we need to update and test this when we build the profile in FE
@user_bp.route("/profile/<user_id>", methods=["GET"])
def get_a_specific_users(user_id):
    try:
        user = User.query.get(user_id)
        return user.make_user_json(), 200
    except:
        return {"details": f"User {user_id} not found"}, 404




@user_bp.route("/login/verify", methods=["GET"])
def verify_a_specific_user():
    request_body = request.get_json()[0]
    if len(request_body) < 2:
        return jsonify([{"message": "missing email/username or password"}]), 404
    for key in request_body.keys():
        if key == "email":
            input_email = request_body['email']
            user = User.query.filter_by(email=input_email).first()
        # if key == "username":
        #     input_username = request_body['username']
        #     user = User.query.filter_by(username=input_username).first()
        if key == "secret":
            input_secret = request_body['secret']

    if user:
        if user.secret == input_secret:
            # send user dict back to use in FE to render user data
            return jsonify([{user}]), 200
        else:
            return jsonify([{"message": "invalid password"}]), 400
    else:
        return jsonify([{"message": "invalid username or email"}]), 400


@user_bp.route("", methods=["DELETE"])
def delete_all_user():
    all_users = User.query.all()
    for user in all_users:
        db.session.delete(user)
        db.session.commit()
    return {"details": "all users were successfully deleted"}, 200




# since we store user data in global state variable currentUser, we will not use userid in URL
# instead, user info will be stored in global variable and used to render, so URL will be only /delete
# we need to update and test this when we build the profile in FE and add a delete my profile button
@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_a_specific_user(user_id):
    try:
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"details": "User was successfully deleted"}, 200
    except:
        return {"details": f"User {user_id} not found"}, 404



# since we store user data in global state variable currentUser, we will not use userid in URL
# instead, user info will be stored in global variable and used to render, so URL will be only /updateprofile
# we need to update and test this when we build the profile in FE and add a update my profile button
@user_bp.route("/profile/<user_id>", methods=["PUT"])
def update_user_profile(user_id):
    try:
        user = User.query.get(user_id)
        request_body = request.get_json()[0]
        # for key, value in request_body.items():   # key ?
        #     user.key = value

            
        user.username = request_body["username"]
        user.secret = request_body['secret']
        user.email = request_body['email']
        db.session.commit()
        return make_response(user.make_user_json()), 200
    except:
        return  {"details": f"User {user_id} not found"}, 404


# update /patch user's info

# username: Mary
# email:elly@ elly.com
# password: 123
# campus: Maple
# about_me: Hi


# update user's location with google api
