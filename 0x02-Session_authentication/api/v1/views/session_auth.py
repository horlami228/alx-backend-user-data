#!/usr/bin/env python3

""" Routes for all the endpoints of the Session Authentication """

from api.v1.views import app_views
from models.user import User
from flask import jsonify, request
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth_session_login() -> str:
    """POST /api/v1/auth_session/login"""

    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):

            from api.v1.app import auth

            session_id = auth.create_session(user.id)

            SESSION_NAME = os.getenv("SESSION_NAME")

            response = jsonify(user.to_json())

            print(SESSION_NAME)
            response.set_cookie(SESSION_NAME, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401
