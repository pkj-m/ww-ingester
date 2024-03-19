# Insert values in a table
import time
import os

from google.cloud import bigquery

from google.oauth2 import service_account
from config import load_config

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp-cred.json'


def write_event_bigquery(event):
    config = load_config(section='bigquery')

    bqcreds = service_account.Credentials.from_service_account_file('gcp-cred.json', scopes=[
        'https://www.googleapis.com/auth/cloud-platform'])

    client = bigquery.Client(credentials=bqcreds, project=bqcreds.project_id, )

    now = time.time()

    # Define the BigQuery schema
    schema = [
        bigquery.SchemaField("msg", "JSON"),
        bigquery.SchemaField("timestamp", "TIMESTAMP")
    ]

    # Prepare the data to be inserted into BigQuery
    rows_to_insert = [(event, now)]

    table_id = config['bq_table_id']

    table = client.get_table(table_id)
    errors = client.insert_rows(table, rows_to_insert, schema)

    if errors:
        print(f'Errors occurred: {errors}')
    else:
        print('Data inserted successfully.')
