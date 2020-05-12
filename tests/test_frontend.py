import sys
sys.path.append('./')
from app.frontend.app import server


print('\n ========================= front-end test session start =========================')
try:
    with server.test_client() as c:
        response = c.get('/')
        assert response.status_code == 200
    print('Response Successful')
    print('\n ============================ front-end test passed =============================')
except Exception as e:
    print('Response Error {}'.format(str(e)))
    print('\n ============================ front-end test failed =============================')