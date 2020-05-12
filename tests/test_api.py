import sys
sys.path.append('./')
from app.api.api import app

print('=====================API test session starts======================')
try:
    with app.test_client() as c:
        response = c.get('/api/')
        assert response.status_code == 200
    print('Response Successful')
    print('========================API test passed===========================')
except Exception as e:
    print('Response Error {}'.format(str(e)))
    print('========================API test failed===========================')
