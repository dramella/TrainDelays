import os
import numpy as np

GCP_PROJECT = str(os.environ.get('GCP_PROJECT'))
GCP_REGION = str(os.environ.get('GCP_REGION'))
BUCKET_NAME = str(os.environ.get('BUCKET_NAME'))
BQ_REGION = str(os.environ.get('BQ_REGION'))
BQ_DATASET = str(os.environ.get('BQ_DATASET'))
