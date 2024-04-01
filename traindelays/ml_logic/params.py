import os

GCP_PROJECT = str(os.environ.get('GCP_PROJECT_ID'))
GCP_REGION = str(os.environ.get('GCP_REGION'))
BUCKET_NAME = str(os.environ.get('BUCKET_NAME'))
BQ_REGION = str(os.environ.get('BQ_REGION'))
BQ_DATASET = str(os.environ.get('BQ_DATASET'))
SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT')
PROJECT_PATH = os.environ.get('PROJECT_PATH')
RAIL_DATA_TABLE_ID = os.environ.get('RAIL_DATA_TABLE_ID')
GEO_COOORDINATES_TABLE_ID = os.environ.get('GEO_COOORDINATES_TABLE_ID')
TRAIN_SERVICE_CODE_TABLE_ID = os.environ.get('TRAIN_SERVICE_CODE_TABLE_ID')
INCIDENT_REASON_CODES_TABLE_ID = os.environ.get('INCIDENT_REASON_CODES_TABLE_ID')
MODEL_BUCKET = os.environ.get('MODEL_BUCKET')
