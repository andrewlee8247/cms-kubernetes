from google.cloud import bigquery
import logging
from . import insert


def predict(age, gender, race=None, state=None, alzheimers=None,
            heart_failure=None, kidney_disease=None, cancer=None,
            copd=None, depression=None, diabetes=None, heart_disease=None,
            osteoporosis=None, arthritis=None, stroke=None,
            dx=None, px=None, hcpcs=None):

    # Connect to database
    database = 'healthcare-predictions'
    client = bigquery.Client(database)

    try:
        # Input data to table
        request_id = insert.insert_data(age, gender, race, state, alzheimers,
                                        heart_failure, kidney_disease, cancer,
                                        copd, depression, diabetes,
                                        heart_disease, osteoporosis, arthritis,
                                        stroke, dx, px, hcpcs)

        # Prediction query
        query = """
        SELECT *
        FROM
            ML.PREDICT(MODEL `cms.model_v1`,
                (
                SELECT *
                FROM
                    `cms.prediction_requests`
                WHERE ID = """ '\'' + request_id + '\'' \
                """
                )
            )"""

        # Run query
        query_job = client.query(query)
        results = query_job.result()
        job_id = query_job.job_id
        if query_job.state == 'DONE':
            logging.info('Prediction Job ID: {0} is {1}'.format(job_id, query_job.state))
        else:
            raise Exception('Prediction Job ID: {0} error {1}'.format(job_id, query_job.errors))

        # Get predicted annual cost
        for row in results:
            prediction = {'prediction': round(row.predicted_ANNUAL_COST, 2)}
        return prediction

    except Exception as e:
        error = {'error': str(e)}
        return error
