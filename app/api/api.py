import sys
from flask import Flask
from flask import jsonify
from flask import request
import jwt
from functools import wraps
from flasgger import Swagger
from flasgger import swag_from
from google.cloud.logging.handlers import ContainerEngineHandler
import logging
from lib import prediction, secrets

formatter = logging.Formatter("%(message)s")
handler = ContainerEngineHandler(stream=sys.stderr)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
root = logging.getLogger()
root.addHandler(handler)
root.setLevel(logging.INFO)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["SWAGGER"] = {
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/api/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/api/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/",
}

# Setup template for Swagger UI
template = {
    "swagger": "2.0",
    "info": {
        "title": "Healthcare Predictions API",
        "description": "API for Making Healthcare Predictions",
        "version": "1.0",
        "schemes": ["http", "https"],
    },
}

Swagger(app, template=template)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = secrets.access_token
        # Check if token is in headers
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            logging.error("A valid token is missing")
            return jsonify({"error": "A valid token is missing"})
        # Check if token is valid
        try:
            access = jwt.decode(token, "secret", algorithm="HS256")
        except Exception:
            logging.error("Token is invalid")
            return jsonify({"error": "Token is invalid"})

        return f(access, *args, **kwargs)

    return decorator


@app.route("/api/prediction", methods=["POST"])
@token_required
@swag_from("apidocs.yml")
def get_prediction(access):
    try:
        req_data = request.get_json()
        age = req_data["age"]
        gender = req_data["gender"]
        race = None
        if "race" in req_data:
            race = req_data["race"]
        state = None
        if "state" in req_data:
            state = req_data["state"]
        alzheimers = None
        if "alzheimers" in req_data:
            alzheimers = req_data["alzheimers"]
        heart_failure = None
        if "heart_failure" in req_data:
            heart_failure = req_data["heart_failure"]
        kidney_disease = None
        if "kidney_disease" in req_data:
            kidney_disease = req_data["kidney_disease"]
        cancer = None
        if "cancer" in req_data:
            cancer = req_data["cancer"]
        copd = None
        if "copd" in req_data:
            copd = req_data["copd"]
        depression = None
        if "depression" in req_data:
            depression = req_data["depression"]
        diabetes = None
        if "diabetes" in req_data:
            diabetes = req_data["diabetes"]
        heart_disease = None
        if "heart_disease" in req_data:
            heart_disease = req_data["heart_disease"]
        osteoporosis = None
        if "osteoporosis" in req_data:
            osteoporosis = req_data["osteoporosis"]
        arthritis = None
        if "arthritis" in req_data:
            arthritis = req_data["arthritis"]
        stroke = None
        if "stroke" in req_data:
            stroke = req_data["stroke"]
        dx = None
        if "dx" in req_data:
            dx = req_data["dx"]
        px = None
        if "px" in req_data:
            px = req_data["px"]
        hcpcs = None
        if "hcpcs" in req_data:
            hcpcs = req_data["hcpcs"]

        response = prediction.predict(
            age,
            gender,
            race,
            state,
            alzheimers,
            heart_failure,
            kidney_disease,
            cancer,
            copd,
            depression,
            diabetes,
            heart_disease,
            osteoporosis,
            arthritis,
            stroke,
            dx,
            px,
            hcpcs,
        )
        logging.info({"JSON payload": req_data, "prediction": response["prediction"]})
        return jsonify(response)

    except Exception as e:
        logging.error(e)
        error = {"error": "{}".format(e)}
        return jsonify(error)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port="8080")
