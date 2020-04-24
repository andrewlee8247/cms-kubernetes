from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect
from flask.logging import create_logger
from flasgger import Swagger
from flasgger import swag_from
import logging
from lib import prediction


app = Flask(__name__)

template = {
    "swagger": "2.0",
    "info": {
        "title": "Healthcare Predictions API",
        "description": "API for Making Healthcare Predictions",
        "version": "1.0",
        "schemes": [
            "http",
            "https"
        ],
    }
}

Swagger(app, template=template)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route('/')
def home():
    """/ Route will redirect to API Docs: /apidocs"""
    return redirect('/apidocs')


@app.route('/api/prediction', methods=['POST'])
@swag_from('apidocs.yml')
def get_prediction():
    age = request.args.get('age', type=int)
    gender = request.args.get('gender', type=int)
    race = request.args.get('race', type=int)
    state = request.args.get('state', type=str)
    alzheimers = request.args.get('alzheimers', type=int)
    heart_failure = request.args.get('heart_failure', type=int)
    kidney_disease = request.args.get('kidney_disease', type=int)
    cancer = request.args.get('cancer', type=int)
    copd = request.args.get('copd', type=int)
    depression = request.args.get('depression', type=int)
    diabetes = request.args.get('diabetes', type=int)
    heart_disease = request.args.get('heart_disease', type=int)
    osteoporosis = request.args.get('osteoporosis', type=int)
    arthritis = request.args.get('arthritis', type=int)
    stroke = request.args.get('stroke', type=int)
    dx = request.args.get('dx', type=int)
    px = request.args.get('px', type=int)
    hcpcs = request.args.get('hcpcs', type=int)

    response = jsonify(prediction.predict(age, gender, race, state,
                                          alzheimers, heart_failure,
                                          kidney_disease, cancer, copd,
                                          depression, diabetes,
                                          heart_disease, osteoporosis,
                                          arthritis, stroke, dx, px, hcpcs))
    LOG.info(response)
    return response


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)