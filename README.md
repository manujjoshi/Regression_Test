# Regression_Test

A plain HTML page served by Flask, used to learn CI/CD with GitHub Actions and Render.
Edit `templates/index.html`, push to `main`, and the change goes live automatically.

## Run locally

```
pip install -r requirements.txt
python app.py                # open http://127.0.0.1:5000
```

## Tests

```
pip install pytest
pytest -q
```

## How the pipeline works

Every push to `main` runs `.github/workflows/deploy.yml`:

1. **test**: installs the dependencies and runs the tests.
2. **deploy** (only if the tests pass): calls the Render deploy hook, then waits until the live
   site's `/health` page reports the pushed commit.

`.github/workflows/uptime.yml` also checks the live site daily at 06:00 UTC.

One-time setup:

1. On [Render](https://render.com), choose **New > Blueprint**, connect this repo and apply `render.yaml`.
2. In the new service, open **Settings > Deploy Hook** and copy the URL.
3. In GitHub, open **Settings > Secrets and variables > Actions** and add a repository secret
   named `STUDENTSCORE` with that URL.
4. On the **Variables** tab of the same page, add a repository variable named `APP_URL` with the
   site's address (no trailing slash).

## Failure alerts

Any failure turns a GitHub Actions run red, and GitHub emails you about failed runs:

- **Tests fail:** the `test` job fails and nothing is deployed.
- **Render build or start fails:** the `deploy` job waits up to 15 minutes for `/health` to report the
  pushed commit and fails if it never does.
- **Site goes down later:** the daily uptime check fails.

Make sure email is on under GitHub **Settings > Notifications > System > Actions**
("Only notify for failed workflows"). Render can also email you about failed deploys under
**Workspace Settings > Notifications**.
