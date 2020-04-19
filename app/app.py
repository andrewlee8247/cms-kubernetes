from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect
from flask.logging import create_logger
from flasgger import Swagger
from lib import prediction
import logging


app = Flask(__name__)
Swagger(app)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route('/')
def home():
    """/ Route will redirect to API Docs: /apidocs"""
    return redirect('/apidocs')


@app.route('/prediction/api', methods=['GET', 'POST'])
def get_prediction():
    """ Make predictions on annual healthcare cost based on medical condition
    Documentation:

    Data used for predictions is based on data collected from the Centers for Medicare and Medicaid Services from
    2008 to 2010. Through this API, predictions can be made to help insurers estimate the annual cost for patients
    based on chronic medical condition. Since only Medicare and Medicaid data is used predictions will be lower
    than the annual cost of medical care for patients not receiving Medicare or Medicaid or are uninsured.  

    Required type of inputs for fields:

    Gender: 1 for Male, 2 for Female
    Race: 1 for White, 2 for Black, 3 for Other, 5 for Hispanic
    State: State abbreviation (case-insensitive)
    Medical Condition: 1 for Yes, 2 for No
    DX: Number of claims based on diagnosis.
    PX: Number of claims based on procedure.
    HCPCS: Number of services outside of primary insurance received.

    To get detailed documentation on the data, visit: https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF

    ---
        consumes: application/json
        parameters:
            -   in: query
                name: age
                type: integer
                description: Age
                required: True
            -   in: query
                name: gender
                type: integer
                description: Gender (1 for Male, 2 for Female)
                required: True
            -   in: query
                name: race
                type: integer
                description: Race (1 for White, 2 for Black, 3 for Other, 5 for Hispanic)
                required: False
            -   in: query
                name: state
                type: string
                description: State (abbreviation)
                required: False
            -   in: query
                name: alzheimers
                type: integer
                description: Alzheimers (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: heart_failure
                type: integer
                description: Heart Failure (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: kidney_disease
                type: integer
                description: Kidney disease (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: cancer
                type: integer
                description: Cancer (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: copd
                type: integer
                description: COPD (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: depression
                type: integer
                description: Depression (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: diabetes
                type: integer
                description: Diabetes (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: heart_disease
                type: integer
                description: Heart Disease (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: osteoporosis
                type: integer
                description: Osteoporosis (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: arthritis
                type: integer
                description: Arthritis (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: stroke
                type: integer
                description: Stroke (1 for Yes, 2 for No)
                required: False
            -   in: query
                name: dx
                type: integer
                description: Number of claims annually based on diagnosis.
                required: False
            -   in: query
                name: px
                type: integer
                description: Number of claims annually based on procedure.
                required: False
            -   in: query
                name: hcpcs
                type: integer
                description: Number of services outside of primary insurance received.
                required: False

        responses:
            200:
                description: Returns prediction result.

    """
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

    response = jsonify(prediction.prediction(age, gender, race, state,
                                             alzheimers, heart_failure,
                                             kidney_disease, cancer, copd,
                                             depression, diabetes,
                                             heart_disease, osteoporosis,
                                             arthritis, stroke, dx, px, hcpcs))
    return response


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
