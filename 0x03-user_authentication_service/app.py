#!/usr/bin/env python3
from auth import Auth
from flask import Flask, jsonify, request


app = Flask(__name__)
app.url_map.strict_slashes = False

AUTH = Auth()


@app.route("/")
def home():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST", "GET"])
def register_user():
    data = request.get_json()
    try:
        AUTH.register_user(email=data.get("email"),
                           password=data.get("password"))
        return jsonify({"email": data.get("email"),
                        "message": "user created"}, 201)
    except Exception:
        return jsonify({"message": "email already registered"}, 400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
