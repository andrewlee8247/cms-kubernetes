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
            print('Prediction Job ID: ' + job_id + ' is ' + query_job.state)
            logging.info('Prediction Job ID: ' + job_id + ' is ' + query_job.state)
        else:
            print('Prediction Job ID: ' + job_id + ' error ' + query_job.errors)
            raise Exception('Prediction Job ID: ' + job_id + ' error ' + query_job.errors)

        # Get predicted annual cost
        for row in results:
            prediction = {'prediction': round(row.predicted_ANNUAL_COST, 2)}
            logging.info(prediction)
            print(prediction)
        return prediction

    except Exception as e:
        logging.error(e)
        error = {'error': str(e)}
        print(error)
        return error
