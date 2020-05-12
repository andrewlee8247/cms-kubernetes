import sys
sys.path.append('./')
from app.api.api import app

try:
    with app.test_client() as c:
        response = c.get('/api/')
        assert response.status_code == 200
    print('Response Successful')
except Exception as e:
    print('Response Error {}'.format(str(e)))
