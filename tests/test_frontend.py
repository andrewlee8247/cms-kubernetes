import sys

sys.path.append("./app")
from frontend.web import server


def test_frontend():
    with server.test_client() as c:
        response = c.get("/")
        assert response.status_code == 200
