from fastapi import FastAPI
import pandas as pd
from traindelays import utils as u
from traindelays.params import *

app = FastAPI()
@app.get("/predict")
def predict(
    departure_station = str,
    arrival_station = str,
    departure_date = str,
    departure_time = str,
    arrival_date = str,
    arrival_time = str,
    type_day = str,
    train_service_group_code = str,
    train_schedule_type = str,
    train_unit_class = str,
    train_manager = str,
    incident_reason = str,
    reactionary_reason = str,
    event_code = str):
    """
    Make a single delay prediction.
    """

    # 💡 Optional trick instead of writing each column name manually
    X_pred = pd.DataFrame(locals(), index=[0])

    # Datetime conversion before pre-processing
    from datetime import datetime, date, time
    X_pred['departure_time'] = time(X_pred['departure_time'])
    X_pred['arrival_date'] = date(X_pred['arrival_date'])
    X_pred['arrival_time'] = time(X_pred['arrival_time'])
    X_pred['PLANNED_ORIG_GBTT_DATETIME_AFF'] = datetime.combine(X_pred['departure_date'], X_pred['departure_time'])
    X_pred['PLANNED_DEST_GBTT_DATETIME_AFF'] = datetime.combine(X_pred['arrival_date'], X_pred['arrival_time'])
    X_pred.drop(columns=['departure_date', 'departure_time', 'arrival_date', 'arrival_time'], inplace=True)

    # Geographical conversion before pre-processing
    lon_lat_df = u.read_data_from_bq(credentials = SERVICE_ACCOUNT,
                  gcp_project = GCP_PROJECT, bq_dataset = BQ_DATASET,
                  table = GEO_COOORDINATES_TABLE_ID)


    #model = app.state.model
   # X_processed = preprocess_features(X_pred)
   # y_pred = model.predict(X_processed)
   # return dict(fare_amount=float(y_pred))
