import sys
sys.path.append('./')
from app.frontend.app import server

try:
    with server.test_client() as c:
        response = c.get('/')
        assert response.status_code == 200
    print('Response Successful')
except Exception as e:
    print('Response Error {}'.format(str(e)))
