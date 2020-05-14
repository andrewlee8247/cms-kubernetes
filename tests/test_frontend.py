import sys

sys.path.append("./app")
from frontend.app import server


def test_frontend():
    with server.test_client() as c:
        response = c.get("/")
        assert response.status_code == 200
