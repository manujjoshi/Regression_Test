"""Simple web UI for predicting a student's percentage from study hours.

Usage:
    python app.py
then open http://127.0.0.1:5000 in a browser (set FLASK_DEBUG=1 for debug mode).
In production it is served by gunicorn (see render.yaml).
(Run train_model.py first if student_score_model.joblib does not exist.)
"""
import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

MODEL_PATH = Path(__file__).parent / "student_score_model.joblib"

app = Flask(__name__)
model = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET", "POST"])
def index():
    hours = request.form.get("hours", "")
    score = error = None
    if request.method == "POST":
        try:
            value = float(hours)
        except ValueError:
            error = "Please enter a number"
        else:
            if not 0 <= value <= 24:
                error = "Hours must be between 0 and 24"
            else:
                pred = model.predict(pd.DataFrame({"Hours": [value]}))[0]
                score = f"{min(max(pred, 0), 100):.2f}"
    return render_template("index.html", hours=hours, score=score, error=error)


@app.route("/health")
def health():
    # RENDER_GIT_COMMIT is set by Render; CI uses it to confirm the new code is live
    return jsonify(status="ok", commit=os.environ.get("RENDER_GIT_COMMIT", "local"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
