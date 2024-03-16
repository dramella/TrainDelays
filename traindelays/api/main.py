from fastapi import FastAPI
import pandas as pd
from traindelays import utils as u
from traindelays.params import *
from traindelays.ml_logic import preprocess as p
from dotenv import load_dotenv
load_dotenv('.env')

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
    # dates transformation
    X_pred['PLANNED_ORIG_GBTT_DATETIME_AFF'] = pd.to_datetime(X_pred['departure_date']) + pd.to_timedelta(X_pred['departure_time'].astype(str))
    X_pred['PLANNED_DEST_GBTT_DATETIME_AFF'] = pd.to_datetime(X_pred['arrival_date']) + pd.to_timedelta(X_pred['arrival_time'].astype(str))
    X_pred.drop(columns=['departure_date', 'departure_time', 'arrival_date', 'arrival_time'], inplace=True)
    lon_lat_df = u.read_data_from_bq(credentials = os.environ.get('SERVICE_ACCOUNT'),
                    gcp_project = os.environ.get('GCP_PROJECT_ID'), bq_dataset = os.environ.get('BQ_DATASET'),
                    table = os.environ.get('GEO_COOORDINATES_TABLE_ID'))
    X_pred = pd.merge(X_pred,lon_lat_df,left_on = 'departure_station',right_on='Station_Name')
    X_pred.drop(columns=['departure_station','Station_Name','Latitude', 'Longitude'],inplace=True)
    X_pred = X_pred.rename({'Stanox':'PLANNED_ORIG_LOC_CODE_AFF'},axis=1)

    X_pred = pd.merge(X_pred,lon_lat_df,left_on = 'arrival_station',right_on='Station_Name')
    X_pred.drop(columns=['arrival_station','Station_Name','Latitude', 'Longitude'],inplace=True)
    X_pred = X_pred.rename({'Stanox':'PLANNED_DEST_LOC_CODE_AFFECTED'},axis=1)
    # Extracting value from input strings
    X_pred['type_day'] = X_pred['type_day'].apply(lambda x: x.split()[0])
    X_pred['train_service_group_code'] = X_pred['train_service_group_code'].apply(lambda x: x.split()[0])
    X_pred['incident_reason'] = X_pred['incident_reason'].apply(lambda x: x.split()[0])
    X_pred = X_pred.rename({'train_schedule_type':'TRAIN_SCHEDULE_TYPE_AFFECTED',
                            'train_unit_class':'UNIT_CLASS_AFFECTED',
                            'train_manager': 'RESPONSIBLE_MANAGER',
                            'incident_reason': 'INCIDENT_REASON',
                            'reactionary_reason': 'REACTIONARY_REASON_CODE',
                            'event_code': 'APP_TIMETABLE_FLAG_AFF',
                            'type_day':'ENGLISH_DAY_TYPE',
                            'train_service_group_code':'TRAIN_SERVICE_GROUP_CODE'
                            },
                        axis=1)
    X_preproc = p.pipe.transform(X_pred)


    #model = app.state.model
   # X_processed = preprocess_features(X_pred)
   # y_pred = model.predict(X_processed)
   # return dict(fare_amount=float(y_pred))
