import sys
from locust import HttpUser, TaskSet, task, between
import json

sys.path.append("./app/api")
from lib import secrets

token = secrets.access_token()


class UserBehavior(TaskSet):
    @task(1)
    def create_post(self):
        headers = {
            "content-type": "application/json",
            "x-access-token": token 
        }
        self.client.post(
            "/api/prediction",
            data=json.dumps(
                {
                    "age": 65,
                    "gender": 1,
                    "race": 3,
                    "state": 54,
                    "alzheimers": 2,
                    "heart_failure": 2,
                    "kidney_disease": 1,
                    "cancer": 2,
                    "copd": 1,
                    "depression": 1,
                    "diabetes": 2,
                    "heart_disease": 1,
                    "osteoporosis": 2,
                    "arthritis": 2,
                    "stroke": 2,
                    "dx": 1,
                    "px": 2,
                    "hcpcs": 2,
                }
            ),
            headers=headers,
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5.0, 9.0)
