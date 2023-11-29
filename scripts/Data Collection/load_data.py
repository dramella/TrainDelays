import pandas as pd
from data import load_data_to_bq
from params import *

paths = ['2018 Train Delays',
         '2019 Train Delays',
         '2020 Train Delays',
         '2021 Train Delays',
         '2022 Train Delays',
         '2023 Train Delays']

def load_tables(df, path):
    load_data_to_bq(df, gcp_project=GCP_PROJECT, bq_dataset=BQ_DATASET, table=path)
