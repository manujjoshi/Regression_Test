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

BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "student_score_model.joblib"
DATA_PATH = BASE_DIR / "student_scores.csv"

app = Flask(__name__)
model = joblib.load(MODEL_PATH)

# Range of study hours the model was trained on, used to flag less reliable predictions
_train_hours = pd.read_csv(DATA_PATH)["Hours"]
MIN_HOURS, MAX_HOURS = _train_hours.min(), _train_hours.max()
FORMULA = f"Score = {model.coef_[0]:.2f} x Hours + {model.intercept_:.2f}"


@app.route("/", methods=["GET", "POST"])
def index():
    hours = request.form.get("hours", "")
    score = error = warning = None
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
                if not MIN_HOURS <= value <= MAX_HOURS:
                    warning = (
                        f"The model was trained on {MIN_HOURS} to {MAX_HOURS} hours of study, "
                        "so this prediction is less reliable."
                    )
    return render_template(
        "index.html", hours=hours, score=score, error=error, warning=warning, formula=FORMULA
    )


@app.route("/health")
def health():
    # RENDER_GIT_COMMIT is set by Render; CI uses it to confirm the new code is live
    return jsonify(status="ok", commit=os.environ.get("RENDER_GIT_COMMIT", "local"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
