# Regression_Test

Predicts a student's percentage score from the number of hours studied, using linear regression
(Score ≈ 9.78 × Hours + 2.48, cross-validated R² ≈ 0.92).

## Run locally

```
pip install -r requirements.txt
python train_model.py        # trains and saves student_score_model.joblib
python app.py                # open http://127.0.0.1:5000
```

`python train_model.py 3 5.5 8` also prints predictions for the given hours.

## Tests

```
pip install pytest
pytest -q
```

## Deployment

Every push to `main` runs the GitHub Action in `.github/workflows/deploy.yml`, which trains the model,
runs the tests and, if they pass, triggers a deploy on [Render](https://render.com) through a deploy hook.

One-time setup:

1. On Render, choose **New > Blueprint**, connect this repo and apply `render.yaml`.
2. In the new service, open **Settings > Deploy Hook** and copy the URL.
3. In GitHub, open **Settings > Secrets and variables > Actions** and add a repository secret
   named `STUDENTSCORE` with that URL.
4. Under **Settings > Secrets and variables > Actions > Variables**, add a repository variable named
   `APP_URL` with the site's address (for example `https://student-score-predictor.onrender.com`,
   no trailing slash). The deploy job uses it to wait until Render is serving the new commit.

## Failure alerts

Any failure turns a GitHub Actions run red, and GitHub emails you about failed runs:

- **Tests fail:** the `test` job fails and nothing is deployed.
- **Render build or start fails:** the `deploy` job waits up to 15 minutes for `/health` to report the
  pushed commit and fails if it never does.
- **Site goes down later:** `.github/workflows/uptime.yml` checks the live site daily at 06:00 UTC
  (and can be run by hand from the Actions tab).

Make sure email is on under GitHub **Settings > Notifications > System > Actions**
("Only notify for failed workflows"). Render can also email you about failed deploys under
**Workspace Settings > Notifications**.
