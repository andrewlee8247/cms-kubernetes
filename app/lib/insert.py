from google.cloud import bigquery
import uuid
import logging
from lib import states


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
    state_code = states.state_search(state)

    # Impute none values and raise exceptions for incorrect input values
    if race not in (1, 2, 5):
        race = 3
    if alzheimers is None:
        alzheimers = 2
    elif alzheimers not in (None, 1, 2):
        raise Exception('Alzheimers must be 1 or 2')
    if heart_failure is None:
        heart_failure = 2
    elif heart_failure not in (1, 2):
        raise Exception('Heart failure must be 1 or 2')
    if kidney_disease is None:
        kidney_disease = 2
    elif kidney_disease not in (1, 2):
        raise Exception('Kidney disease must be 1 or 2')
    if cancer is None:
        cancer = 2
    elif cancer not in (1, 2):
        raise Exception('Cancer must be 1 or 2')
    if copd is None:
        copd = 2
    elif copd not in (1, 2):
        raise Exception('COPD must be 1 or 2')
    if depression is None:
        depression = 2
    elif depression not in (1, 2):
        raise Exception('Depression must be 1 or 2')
    if diabetes is None:
        diabetes = 2
    elif diabetes not in (1, 2):
        raise Exception('Diabetes must be 1 or 2')
    if heart_disease is None:
        heart_disease = 2
    elif heart_disease not in (1, 2):
        raise Exception('Heart disease must be 1 or 2')
    if osteoporosis is None:
        osteoporosis = 2
    elif osteoporosis not in (1, 2):
        raise Exception('Osteoporosis must be 1 or 2')
    if arthritis is None:
        arthritis = 2
    elif arthritis not in (1, 2):
        raise Exception('Arthritis must be 1 or 2')
    if stroke is None:
        stroke = 2
    elif stroke not in (1, 2):
        raise Exception('Stroke must be 1 or 2')
    if dx is None:
        dx = 0
    elif type(dx) is not int:
        raise Exception('Number of diagnosis must be a number')
    if px is None:
        px = 0
    elif type(px) is not int:
        raise Exception('Number of procedures must be a number')
    if hcpcs is None:
        hcpcs = 0
    elif type(hcpcs) is not int:
        raise Exception('Number of services outside of primary insurance must \
        be a number')

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
        print('Insert Job ID: ' + job_id + ' is ' + query_job.state)
        logging.info('Insert Job ID: ' + job_id + ' is ' + query_job.state)
    else:
        print('Insert Job ID: ' + job_id + ' error ' + query_job.errors)
        raise Exception('Insert Job ID: ' + job_id + ' error ' + query_job.errors)

    return id
