from flask import Blueprint, request, jsonify, make_response, url_for
from app import db
from app.models.user import User
from dotenv import load_dotenv
import os
import requests

user_bp = Blueprint("user", __name__, url_prefix="")



@user_bp.route("/signup", methods=["POST"])
def create_user():
    request_body = request.get_json()[0]
    new_user = User.from_json(request_body)
    db.session.add(new_user)
    db.session.commit()
    
    # send post request to ChatEngine
    data = {
        "username" : new_user.username,
        "secret" : new_user.password,
        "email" : new_user.email
    }
    headers_to_chat_engine = {"PRIVATE-KEY": os.environ.get("CHAT_ENGINE_KEY")}
    response = requests.post("https://api.chatengine.io/users/", headers=headers_to_chat_engine, data=data)
    response_body = response.json()
    print(f"response_body: {response_body}")
    new_user.user_id_chatengine = response_body["id"]
    db.session.commit()
    return jsonify(new_user.make_user_json()), 200



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


@user_bp.route("/users/profile/<user_id>", methods=["GET", "DELETE", "PUT"])
def edit_a_specific_users(user_id):
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
            # send delete request to ChatEngine
            user_id_chatengine = user.user_id_chatengine
            # user_id_chatengine=user_id_chatengine
            # , user_id_chatengine=166448
            # request_url = url_for("https://api.chatengine.io/users/{user_id_chatengine}/")  
            # response = requests.delete((request_url), headers=headers_to_chat_engine)
            # if response.status_code == 200:
            db.session.delete(user)
            db.session.commit()
            return {"details": "User was successfully deleted"}, 200
        else:
            return {"details": f"User {user_id} not found"}, 404
        
    # update a user's profile
    elif request.method == "PUT":
        request_body = request.get_json()[0]
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
    elif request.method == "PATCH":
        request_body = request.get_json()[0]
        if user:
            user.user_id_chatengine=request_body['user_id_chatengine']
            db.session.commit()
            return make_response(user.make_user_json()), 200


@user_bp.route("/login", methods=["POST"])
def verify_a_specific_user():
    # print(request.get_json())
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
