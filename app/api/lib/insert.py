from google.cloud import bigquery
import uuid
import logging
from . import convert


def insert_data(age, gender, race=None, state=None, alzheimers=None,
                heart_failure=None, kidney_disease=None, cancer=None,
                copd=None, depression=None, diabetes=None, heart_disease=None,
                osteoporosis=None, arthritis=None, stroke=None, dx=None,
                px=None, hcpcs=None):

    # Connect to database
    database = 'healthcare-predictions'
    client = bigquery.Client(database)

    # Raise exceptions
    if type(age) is not int:
        raise Exception('Age must be a number')

    if gender not in (1, 2):
        raise Exception('Gender must be 1 or 2')

    # Lookup state code
    state_code = convert.converter.state(state)

    # Impute none values and raise exceptions for incorrect input values
    race = convert.converter.race(race)
    alzheimers = convert.converter.condition('alzheimers', alzheimers)
    heart_failure = convert.converter.condition('heart failure', heart_failure)
    kidney_disease = convert.converter.condition('kidney disease', kidney_disease)
    cancer = convert.converter.condition('cancer', cancer)
    copd = convert.converter.condition('COPD', copd)
    depression = convert.converter.condition('depression', depression)
    diabetes = convert.converter.condition('diabetes', diabetes)
    heart_disease = convert.converter.condition('heart disease', heart_disease)
    osteoporosis = convert.converter.condition('osteoporosis', osteoporosis)
    arthritis = convert.converter.condition('arthritis', arthritis)
    stroke = convert.converter.condition('stroke', stroke)
    dx = convert.converter.claims('claims based on diagnosis', dx)
    px = convert.converter.claims('claims based on procedures', px)
    hcpcs = convert.converter.claims('services outside of primary insurance', hcpcs)

    # Assign unique id
    request_id = str(uuid.uuid4())

    # Insert data to table
    query = """
    INSERT INTO `cms.prediction_requests`
    VALUES(""" \
        + '\'' + request_id + '\'' + ',' \
        + str(age) + ',' \
        + str(gender) + ',' \
        + str(race) + ',' \
        + str(state_code) + ',' \
        + str(alzheimers) + ',' \
        + str(heart_failure) + ',' \
        + str(kidney_disease) + ',' \
        + str(cancer) + ',' \
        + str(copd) + ',' \
        + str(depression) + ',' \
        + str(diabetes) + ',' \
        + str(heart_disease) + ',' \
        + str(osteoporosis) + ',' \
        + str(arthritis) + ',' \
        + str(stroke) + ',' \
        + str(dx) + ',' \
        + str(px) + ',' \
        + str(hcpcs) + ')'

    # Run query
    query_job = client.query(query)
    query_job.result()
    job_id = query_job.job_id
    if query_job.state == 'DONE':
        logging.info('Insert Job ID: {0}  is {1}'.format(job_id, query_job.state))
    else:
        raise Exception('Insert Job ID: {0} error {1}'.format(job_id, query_job.errors))

    return request_id
