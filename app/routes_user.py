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
        return jsonify(new_user.make_user_json()), 200

    except KeyError as err:
        if "username" in err.args:
            return {"details": f"Request body must include username with string type."}, 400
        if "email" in err.args:
            return {"details": f"Request body must include email with string type."}, 400
        if "password" in err.args:
            return {"details": f"Request body must include password with string type."}, 400


@user_bp.route("/users/all", methods=["GET", "DELETE"])
def all_users():
    all_users = User.query.all()
    # get all users
    if request.method == "GET":
        all_users_response = [(user.make_user_json()) for user in all_users]
        return jsonify(all_users_response), 200
    
    # delete all users
    else:
        for user in all_users:
            db.session.delete(user)
            db.session.commit()
        return {"details": "all users were successfully deleted"}, 200


@user_bp.route("/users/profile", methods=["GET", "DELETE", "PUT"])
def edit_a_specific_users():
    request_body = request.get_json()[0]
    user_id = request_body["user_id"]  
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
            user.password=request_body['password'],
            user.pronouns=request_body['pronouns'],
            user.class_name=request_body['class_name'],
            user.campus=request_body['campus'],
            user.bio=request_body['bio'],
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
        if key == "password":
            input_password = request_body['password']
    if user:
        if user.password == input_password:
            # send user dict back to use in FE to render user data
            return user.make_user_json(), 200
        else:
            return jsonify([{"message": "invalid password"}]), 400
    else:
        return jsonify([{"message": "invalid username or email"}]), 400

# update user's location with google api
