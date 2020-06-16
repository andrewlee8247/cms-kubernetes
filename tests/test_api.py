import sys

sys.path.append("./app/api")
from api import app
from lib import secrets


def test_api():
    with app.test_client() as c:
        response = c.get("/api/")
        assert response.status_code == 200


def test_payload():
    with app.test_client() as c:
        auth_header = {
            "content-type": "application/json",
            "x-access-token": secrets.access_token(),
        }
        data = {"age": 55, "gender": 2, "alzheimers": 1}
        response = c.post("/api/prediction", json=data, headers=auth_header)
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["prediction"] == 1096.26
