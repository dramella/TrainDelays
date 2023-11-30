import pandas as pd

from google.cloud import bigquery
from google.oauth2 import service_account
from pathlib import Path

from params import *

def get_data_from_bq(
    gcp_project: str,
    query: str):
    client = bigquery.Client()
    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()
    return df

def load_data_to_bq(
    data: pd.DataFrame,
    gcp_project: str,
    bq_dataset: str,
    table: str
) -> None:
    'Save the dataframes to BigQuery'

    # Checking if data is in dataframe format
    assert isinstance(data, pd.DataFrame)
    # Assigning a name to the table
    table_name = f'{gcp_project}.{bq_dataset}.{table}'
    print(table_name)
    # Calling big query client
    credentials = service_account.Credentials.from_service_account_file('BQ_Service_Account.json')
    client = bigquery.Client(credentials=credentials)

    write_mode = 'WRITE_APPEND'
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)
    job_config.schema_update_options = ['ALLOW_FIELD_ADDITION', 'ALLOW_FIELD_RELAXATION']

    job = client.load_table_from_dataframe(data, table_name, job_config=job_config)
    result = job.result()

    print(f'✅ Data saved to BQ')
