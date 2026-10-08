"""Predict a student's percentage score from the number of hours studied.

Usage:
    python train_model.py              # train, evaluate and save the model
    python train_model.py 9.25 4 6.5   # also predict scores for these study hours
"""
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split

DATA_PATH = "student_scores.csv"
MODEL_PATH = "student_score_model.joblib"

# 1. Load data
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows")
print(df.describe().round(2), "\n")
print(f"Correlation (Hours vs Scores): {df['Hours'].corr(df['Scores']):.3f}\n")

X = df[["Hours"]]
y = df["Scores"]

# 2. Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Train
model = LinearRegression()
model.fit(X_train, y_train)
print(f"Model: Score = {model.coef_[0]:.3f} * Hours + {model.intercept_:.3f}\n")

# 4. Evaluate on held-out test set
y_pred = model.predict(X_test)
results = pd.DataFrame({"Hours": X_test["Hours"], "Actual": y_test, "Predicted": y_pred.round(2)})
print("Test set predictions:")
print(results.to_string(index=False), "\n")
print(f"MAE : {mean_absolute_error(y_test, y_pred):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print(f"R2  : {r2_score(y_test, y_pred):.3f}")

# Cross-validation gives a more reliable estimate on such a small dataset
cv_r2 = cross_val_score(LinearRegression(), X, y, cv=5, scoring="r2")
print(f"5-fold CV R2: {cv_r2.mean():.3f} +/- {cv_r2.std():.3f}\n")

# 5. Refit on all data and save
model.fit(X, y)
joblib.dump(model, MODEL_PATH)
print(f"Final model (all data): Score = {model.coef_[0]:.3f} * Hours + {model.intercept_:.3f}")
print(f"Saved to {MODEL_PATH}\n")

# 6. Predict for hours given on the command line (default: 9.25 hrs/day)
hours = [float(h) for h in sys.argv[1:]] or [9.25]
preds = model.predict(pd.DataFrame({"Hours": hours}))
for h, p in zip(hours, preds):
    print(f"Predicted score for {h} hours of study: {min(max(p, 0), 100):.2f}%")
