from locust import HttpLocust, TaskSet, task, between
import json


class UserBehavior(TaskSet):
    @task(1)
    def create_post(self):
        headers = {"content-type": "application/json"}
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


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
