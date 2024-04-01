import os
import pandas as pd
import ml_logic.utils as u
import os
import ml_logic.preprocess as p
# 💡 Optional trick instead of writing each column name manually
def predict_new(
    departure_station,
    arrival_station,
    departure_date,
    departure_time,
    arrival_date,
    arrival_time,
    type_day,
    train_service_group_code,
    train_schedule_type,
    train_unit_class,
    train_manager,
    incident_reason,
    reactionary_reason,
    event_code):
    """
    Make a single delay prediction.
    """

    # 💡 Optional trick instead of writing each column name manually
    X_pred = pd.DataFrame({
        'departure_station': [departure_station],
        'arrival_station': [arrival_station],
        'departure_date': [departure_date],
        'departure_time': [departure_time],
        'arrival_date': [arrival_date],
        'arrival_time': [arrival_time],
        'type_day': [type_day],
        'train_service_group_code': [train_service_group_code],
        'train_schedule_type': [train_schedule_type],
        'train_unit_class': [train_unit_class],
        'train_manager': [train_manager],
        'incident_reason': [incident_reason],
        'reactionary_reason': [reactionary_reason],
        'event_code': [event_code]
    })    # Datetime conversion before pre-processing
    from datetime import datetime, date, time
    # dates transformation
    X_pred['PLANNED_ORIG_GBTT_DATETIME_AFF'] = X_pred.apply(lambda row: datetime.combine(row['departure_date'], row['departure_time']), axis=1)
    X_pred['PLANNED_DEST_GBTT_DATETIME_AFF'] = X_pred.apply(lambda row: datetime.combine(row['arrival_date'], row['arrival_time']), axis=1)
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
    model = u.download_model_from_GCP_storage(os.environ.get('SERVICE_ACCOUNT'), os.environ.get('BUCKET_NAME'), os.environ.get('MODEL_BUCKET'))
    y_pred = model.predict(X_preproc)
    return dict(fare_amount=float(y_pred))
