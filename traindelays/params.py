import os

GCP_PROJECT = str(os.environ.get('GCP_PROJECT_ID'))
GCP_REGION = str(os.environ.get('GCP_REGION'))
BUCKET_NAME = str(os.environ.get('BUCKET_NAME'))
BQ_REGION = str(os.environ.get('BQ_REGION'))
BQ_DATASET = str(os.environ.get('BQ_DATASET'))
SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT')
PROJECT_PATH = os.environ.get('PROJECT_PATH')
RAIL_DATA_TABLE_ID = os.environ.get('RAIL_DATA_TABLE_ID')
