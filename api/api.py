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
app.config['JSON_SORT_KEYS'] = False

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
    try:
        req_data = request.get_json()
        age = req_data['age']
        gender = req_data['gender']
        race = req_data['race']
        state = req_data['state']
        alzheimers = req_data['alzheimers']
        heart_failure = req_data['heart_failure']
        kidney_disease = req_data['kidney_disease']
        cancer = req_data['cancer']
        copd = req_data['copd']
        depression = req_data['depression']
        diabetes = req_data['diabetes']
        heart_disease = req_data['heart_disease']
        osteoporosis = req_data['osteoporosis']
        arthritis = req_data['arthritis']
        stroke = req_data['stroke']
        dx = req_data['dx']
        px = req_data['px']
        hcpcs = req_data['hcpcs']

        response = jsonify(prediction.predict(age, gender, race, state,
                                              alzheimers, heart_failure,
                                              kidney_disease, cancer, copd,
                                              depression, diabetes,
                                              heart_disease, osteoporosis,
                                              arthritis, stroke, dx, px, hcpcs))
        LOG.info(response)
        return response

    except Exception as e:
        LOG.error(e)
        error = {'error': 'Missing ' + str(e)}
        return error


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
