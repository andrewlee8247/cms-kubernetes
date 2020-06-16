from google.cloud import bigquery
import uuid
import logging
from lib import convert

project = "healthcare-predictions"
dataset = "cms"
table_name = "prediction_requests"
table_id = "{}.{}.{}".format(project, dataset, table_name)


def insert_data(
    age,
    gender,
    race=None,
    state=None,
    alzheimers=None,
    heart_failure=None,
    kidney_disease=None,
    cancer=None,
    copd=None,
    depression=None,
    diabetes=None,
    heart_disease=None,
    osteoporosis=None,
    arthritis=None,
    stroke=None,
    dx=None,
    px=None,
    hcpcs=None,
):

    # Connect to database
    client = bigquery.Client(project=project)
    table = client.get_table(table_id)

    # Raise exceptions
    if type(age) is not int:
        raise Exception("Age must be a number")

    if gender not in (1, 2):
        raise Exception("Gender must be 1 or 2")

    # Lookup state code
    state_code = convert.converter.state(state)

    # Impute none values and raise exceptions for incorrect input values
    race = convert.converter.race(race)
    alzheimers = convert.converter.condition("alzheimers", alzheimers)
    heart_failure = convert.converter.condition("heart failure", heart_failure)
    kidney_disease = convert.converter.condition("kidney disease", kidney_disease)
    cancer = convert.converter.condition("cancer", cancer)
    copd = convert.converter.condition("COPD", copd)
    depression = convert.converter.condition("depression", depression)
    diabetes = convert.converter.condition("diabetes", diabetes)
    heart_disease = convert.converter.condition("heart disease", heart_disease)
    osteoporosis = convert.converter.condition("osteoporosis", osteoporosis)
    arthritis = convert.converter.condition("arthritis", arthritis)
    stroke = convert.converter.condition("stroke", stroke)
    dx = convert.converter.claims("claims based on diagnosis (dx)", dx)
    px = convert.converter.claims("claims based on procedures (px)", px)
    hcpcs = convert.converter.claims(
        "services outside of primary insurance (hcpcs)", hcpcs
    )

    # Assign unique id
    request_id = str(uuid.uuid4())

    # Insert data to table
    row_to_insert = [
        (
            "{}".format(request_id),
            age,
            gender,
            race,
            state_code,
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
    ]
    error = client.insert_rows(table, row_to_insert)

    if not error:
        logging.info("Insert job is done")
    else:
        raise Exception(error)

    return request_id
