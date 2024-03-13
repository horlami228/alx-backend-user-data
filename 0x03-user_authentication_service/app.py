#!/usr/bin/env python3
from auth import Auth
from flask import Flask, jsonify, request


app = Flask(__name__)
app.url_map.strict_slashes = False

AUTH = Auth()


@app.route("/")
def home():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Register a user """

    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email,
                           password)
        return jsonify({"email": email,
                        "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
