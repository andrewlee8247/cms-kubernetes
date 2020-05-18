import sys
import logging

sys.path.append("./app/api")
from app.api.lib import prediction


def test_prediction():
    result = prediction.predict(32, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0, 0, 0)
    logging.info(result)
    return
