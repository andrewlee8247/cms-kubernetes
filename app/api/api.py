from flask import Flask
from flask import jsonify
from flask import request
from flasgger import Swagger
from flasgger import swag_from
import logging
from lib import prediction


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


@app.route("/api/prediction", methods=["POST"])
@swag_from("apidocs.yml")
def get_prediction():
    try:
        req_data = request.get_json()
        age = req_data["age"]
        gender = req_data["gender"]
        race = req_data["race"]
        state = req_data["state"]
        alzheimers = req_data["alzheimers"]
        heart_failure = req_data["heart_failure"]
        kidney_disease = req_data["kidney_disease"]
        cancer = req_data["cancer"]
        copd = req_data["copd"]
        depression = req_data["depression"]
        diabetes = req_data["diabetes"]
        heart_disease = req_data["heart_disease"]
        osteoporosis = req_data["osteoporosis"]
        arthritis = req_data["arthritis"]
        stroke = req_data["stroke"]
        dx = req_data["dx"]
        px = req_data["px"]
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
        if list(response.keys())[0] == "error":
            logging.error(response)
        else:
            logging.info(
                {"JSON payload": req_data, "prediction": response["prediction"]}
            )
        return jsonify(response)

    except Exception as e:
        logging.error({"error": "Missing {}".format(e)})
        error = {"error": "Missing {}".format(e)}
        return error


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port="8080")
