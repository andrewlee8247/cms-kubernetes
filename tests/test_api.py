import sys

sys.path.append("./app/api")
from api import app


def test_api():
    with app.test_client() as c:
        response = c.get("/api/")
        assert response.status_code == 200
