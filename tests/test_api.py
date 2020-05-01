import os
import sys
from app.api.lib import prediction


def test():
    result = prediction.predict(30,1,1,1,1,2,1,2,1,2,1,2,1,2,1,0,0,0)
    return result

