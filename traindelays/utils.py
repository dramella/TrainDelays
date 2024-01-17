from zlib import crc32
import numpy as np
import pandas as pd
from google.cloud import bigquery

def print_summary_stats(df, cols_list):
    with pd.option_context('display.max_rows', None):
        print("Missing Values:")
        print(df[cols_list].isna().sum() / len(df))

        print("\nUnique Values:")
        print(df[cols_list].nunique())

        print("\nValue Counts:")
        for col in cols_list:
            print(f"\n{df[col].value_counts(dropna=False)}")

def load_data_to_bq(
        credentials: str,
        data: pd.DataFrame,
        gcp_project:str,
        bq_dataset:str,
        table: str,
        truncate: bool):
    """
    - Save the DataFrame to BigQuery
    - Empty the table beforehand if `truncate` is True, append otherwise
    """

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{gcp_project}.{bq_dataset}.{table}"

    data.columns = [f"_{column}" if not str(column)[0].isalpha() and not str(column)[0] == "_" else str(column) for column in data.columns]

    client = bigquery.Client.from_service_account_json(credentials)

    # Define write mode and schema
    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    print(f"\n{'Write' if truncate else 'Append'} {full_table_name} ({data.shape[0]} rows)")

    # Load data
    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete

    print(f"✅ Data saved to bigquery, with shape {data.shape}")

def read_data_from_bq(
        credentials: str,
        gcp_project:str,
        bq_dataset:str,
        table: str):
    """
    - Read BigQuery table as a DataFrame
    """
    client = bigquery.Client.from_service_account_json(credentials)
    # Fetch the data from BigQuery into a DataFrame
    query_job = client.query(f"SELECT * FROM {gcp_project}.{bq_dataset}.{table}")
    return query_job.to_dataframe()


# Function to check test set's identifier.
def test_set_check(identifier, test_ratio):
    return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2**32

# Function to split train/test
def split_train_test_by_id(data, test_ratio, id_column):
    data = data.sample(frac=1, random_state=42)
    if id_column == 'index':
        ids = pd.Series(data.index)
    else:
        ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]
