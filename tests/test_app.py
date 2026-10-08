import re

from app import app


def _message(hours):
    html = app.test_client().post("/", data={"hours": hours}).get_data(as_text=True)
    return re.search(r'class="(?:result|error)">(.*?)</p>', html).group(1)


def test_home_page_loads():
    assert app.test_client().get("/").status_code == 200


def test_valid_prediction():
    assert _message("9.25") == "Predicted score: <strong>92.91%</strong>"


def test_non_numeric_input():
    assert _message("abc") == "Please enter a number"


def test_out_of_range_input():
    assert _message("30") == "Hours must be between 0 and 24"


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_warns_outside_training_range():
    html = app.test_client().post("/", data={"hours": "12"}).get_data(as_text=True)
    assert "Predicted score" in html
    assert "less reliable" in html


def test_no_warning_inside_training_range():
    html = app.test_client().post("/", data={"hours": "5"}).get_data(as_text=True)
    assert "less reliable" not in html
