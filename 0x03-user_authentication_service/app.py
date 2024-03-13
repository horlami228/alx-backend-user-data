#!/usr/bin/env python3
from flask import Flask, jsonify


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def home():
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
