from google.cloud import bigquery
import logging
import json
from app.lib import insert


def prediction(age, gender, race=None, state=None, alzheimers=None,
               heart_failure=None, kidney_disease=None, cancer=None,
               copd=None, depression=None, diabetes=None, heart_disease=None,
               osteoporosis=None, arthritis=None, stroke=None,
               dx=None, px=None, hcpcs=None):

    # Connect to database
    database = 'healthcare-predictions'
    client = bigquery.Client(database)

    try:
        # Input data to table
        id = insert.insert_data(age, gender, race, state, alzheimers,
                                heart_failure, kidney_disease, cancer, copd,
                                depression, diabetes, heart_disease,
                                osteoporosis, arthritis, stroke, dx, px, hcpcs)

        # Prediction query
        query = """
        SELECT *
        FROM
            ML.PREDICT(MODEL `cms.model_v1`,
                (
                SELECT *
                FROM 
                    `cms.predictions`
                WHERE ID = """ '\'' + id + '\'' \
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
            raise Exception('Prediction Job ID: ' + job_id + ' error ' + query_job.errors)
            print('Prediction Job ID: ' + job_id + ' error ' + query_job.errors)
            logging.error('Prediction Job ID: ' + job_id + ' error ' + query_job.errors)
            return

        # Get predicted annual cost
        for row in results:
            prediction = {'prediction': row.predicted_ANNUAL_COST}
            logging.info(prediction)
            print(prediction)
        return prediction

    except Exception as e:
        logging.error(e)
        error = {'error': str(e)}
        print(error)
        return error
