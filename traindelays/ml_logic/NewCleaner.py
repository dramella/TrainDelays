import numpy as np
import pandas as pd

def network_rail_data_cleaner(df):
    # Remove quotes
    df = df.applymap(lambda x: x.replace('"', '') if isinstance(x, str) else x)

    # Uppercase column names
    df.columns = df.columns.str.upper().str.replace('"', '')

    # Rename columns in case old convention is used
    cols_to_rename = {
    'APPLICABLE_TIMETABLE_FLAG': 'APP_TIMETABLE_FLAG_AFF',
    'FINANCIAL_YEAR_PERIOD': 'FINANCIAL_YEAR_AND_PERIOD',
    'INCIDENT_RESP_TRAIN': 'INCIDENT_RESPONSIBLE_TRAIN',
    'NR_LOCATION_MANAGER': 'NETWORK_RAIL_LOCATION_MANAGER',
    'EVENT_TYPE': 'PERFORMANCE_EVENT_CODE',
    'PLANNED_DEST_GBTT_DATETIME':'PLANNED_DEST_GBTT_DATETIME_AFF',
    'PLANNED_DEST_LOCATION_CODE':'PLANNED_DEST_LOC_CODE_AFFECTED',
    'PLANNED_DEST_WTT_DATETIME':'PLANNED_DEST_WTT_DATETIME_AFF',
    'PLANNED_ORIGIN_GBTT_DATETIME':'PLANNED_ORIG_GBTT_DATETIME_AFF',
    'PLANNED_ORIGIN_LOCATION_CODE':'PLANNED_ORIG_LOC_CODE_AFF',
    'PLANNED_ORIGIN_WTT_DATETIME':'PLANNED_ORIG_WTT_DATETIME_AFF',
    'REACT_REASON':'REACTIONARY_REASON_CODE',
    'SERVICE_GROUP_CODE':'SERVICE_GROUP_CODE_AFFECTED',
    'TIMING_LOAD':'TIMING_LOAD_AFFECTED',
    'TRACTION_TYPE': 'TRACTION_TYPE_AFFECTED',
    'TRAILING_LOAD': 'TRAILING_LOAD_AFFECTED',
    'TRAIN_SCHEDULE_TYPE' : 'TRAIN_SCHEDULE_TYPE_AFFECTED',
    'TRAIN_SERVICE_CODE': 'TRAIN_SERVICE_CODE_AFFECTED',
    'UNIT_CLASS':'UNIT_CLASS_AFFECTED',
    'TOC_CODE' : 'OPERATOR_AFFECTED',
    'TRUST_TRAIN_ID': 'TRUST_TRAIN_ID_AFFECTED',
    'RESP_MANAGER' : 'RESPONSIBLE_MANAGER',
    'TRUST_TRAIN_ID_REACT' : 'REACT_TRAIN',
    'TRUST_TRAIN_ID_RESP' : 'RESP_TRAIN'
    }
    df.rename(columns=cols_to_rename, inplace=True)
    df.drop(columns=list(cols_to_rename.keys()), errors='ignore', inplace=True)

    # select only delayed (not cancelled) London Overground trains, where the delay cause is sure
    overground_delayed_trains = (df['OPERATOR_AFFECTED'] == 'EK') & (df['PERFORMANCE_EVENT_CODE'].isin(['A', 'M'])) & (df['ATTRIBUTION_STATUS'].str.contains('Attribution Agreed'))
    df = df[overground_delayed_trains]
    df.drop(columns=['OPERATOR_AFFECTED', 'PERFORMANCE_EVENT_CODE', 'ATTRIBUTION_STATUS'], inplace=True)


    # if minutes of delays are in two columns, sum them into one
    if 'NON_PFPI_MINUTES' in df.columns:
        df['PFPI_MINUTES'] += df['NON_PFPI_MINUTES']
        df.drop(columns=['NON_PFPI_MINUTES'], inplace=True)

    # handles error columns
    df.drop(columns=['UNNAMED: 40', 'UNNAMED: 41'], errors='ignore', inplace=True)
    # fix columns dtypes
    false_float_column_list = ['PLANNED_ORIG_LOC_CODE_AFF','PLANNED_DEST_LOC_CODE_AFFECTED',
                   'TRAIN_SERVICE_CODE_AFFECTED', 'UNIT_CLASS_AFFECTED', 'INCIDENT_NUMBER',
                   'START_STANOX','END_STANOX']
    df[false_float_column_list] = df[false_float_column_list].apply(pd.to_numeric, errors='coerce', downcast='integer')
    df = df.astype('str')
    dates_cols = ['PLANNED_ORIG_GBTT_DATETIME_AFF',
    'PLANNED_ORIG_WTT_DATETIME_AFF',
    'PLANNED_DEST_GBTT_DATETIME_AFF',
    'PLANNED_DEST_WTT_DATETIME_AFF',
    'INCIDENT_CREATE_DATE',
    'INCIDENT_START_DATETIME',
    'INCIDENT_END_DATETIME',
    'EVENT_DATETIME']
    df[dates_cols] = df[dates_cols].apply(pd.to_datetime)
    df['PFPI_MINUTES'] = pd.to_numeric(df['PFPI_MINUTES'],errors='ignore')
    df = df.replace('nan', np.NaN)
    df = df.dropna(subset=['PFPI_MINUTES'])
    return df
