"""Serves a plain HTML page used to learn CI/CD.

Usage:
    python app.py
then open http://127.0.0.1:5000 in a browser (set FLASK_DEBUG=1 for debug mode).
In production it is served by gunicorn (see render.yaml).
"""
import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    # RENDER_GIT_COMMIT is set by Render; CI uses it to confirm the new code is live
    return jsonify(status="ok", commit=os.environ.get("RENDER_GIT_COMMIT", "local"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
