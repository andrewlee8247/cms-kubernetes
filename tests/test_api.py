import sys
sys.path.append('./')
from app.api.api import app


print('\n ============================ API test session start ============================')
try:
    with app.test_client() as c:
        response = c.get('/api/')
        assert response.status_code == 200
    print('Response Successful')
    print('\n =============================== API test passed ================================')
except Exception as e:
    print('Response Error {}'.format(str(e)))
    print('\n =============================== API test failed ================================')
