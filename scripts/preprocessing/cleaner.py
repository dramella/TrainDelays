import pandas as pd
import numpy as np
import math

def cleaner(df):
    df = df[df['TRAIN_SERVICE_CODE_AFFECTED'] != 22216001.0]

    df = df[(df['PERFORMANCE_EVENT_CODE'] == 'A') | (df['PERFORMANCE_EVENT_CODE'] == 'M')]

    df.dropna(axis=0, subset=['INCIDENT_REASON'], inplace=True)

    df.dropna(axis=0, subset=['UNIT_CLASS_AFFECTED'], inplace=True)

    df['INCIDENT_REASON'] = df['INCIDENT_REASON'].apply(lambda x: x[0])

    df = df[df['TRACTION_TYPE_AFFECTED'] == 'EMU']

    df.drop(columns=['TRAILING_LOAD_AFFECTED', 'TIMING_LOAD_AFFECTED', 'FINANCIAL_YEAR_AND_PERIOD',
                     'END_STANOX', 'START_STANOX','PLANNED_ORIG_LOC_CODE_AFF', 'INCIDENT_NUMBER','PLANNED_ORIG_GBTT_DATETIME_AFF','PLANNED_DEST_GBTT_DATETIME_AFF',
                     'PLANNED_DEST_LOC_CODE_AFFECTED', 'INCIDENT_START_DATETIME', 'INCIDENT_END_DATETIME',
                     'SECTION_CODE', 'ATTRIBUTION_STATUS', 'INCIDENT_EQUIPMENT', 'INCIDENT_DESCRIPTION',
                     'TRAIN_SCHEDULE_TYPE_AFFECTED', 'INCIDENT_RESPONSIBLE_TRAIN', 'EVENT_DATETIME', 'RESP_TRAIN',
                     'REACT_TRAIN', 'NETWORK_RAIL_LOCATION_MANAGER', 'OPERATOR_AFFECTED', 'ORIGIN_DEPARTURE_DATE',
                     'INCIDENT_REASON_DESCRIPTION', 'INCIDENT_CREATE_DATE',
                     'TRUST_TRAIN_ID_AFFECTED', 'RESPONSIBLE_MANAGER', 'REACTIONARY_REASON_CODE', 'TRACTION_TYPE_AFFECTED',
                     'STATION_OR', 'STATION_DES'], inplace=True)

    df.loc[:, 'PLANNED_ORIG_WTT_DATETIME_AFF'] = pd.to_datetime(df.PLANNED_ORIG_WTT_DATETIME_AFF)
    df.loc[:, 'ORIG_MONTH'] = df.PLANNED_ORIG_WTT_DATETIME_AFF.dt.month
    df.loc[:, 'ORIG_DAY'] = df.PLANNED_ORIG_WTT_DATETIME_AFF.dt.day
    df.loc[:, 'ORIG_HOUR'] = df.PLANNED_ORIG_WTT_DATETIME_AFF.dt.hour
    df.loc[:, 'ORIG_MINUTE'] = df.PLANNED_ORIG_WTT_DATETIME_AFF.dt.minute
    df.drop(columns='PLANNED_ORIG_WTT_DATETIME_AFF', inplace = True)

    df.loc[:, 'PLANNED_DEST_WTT_DATETIME_AFF'] = pd.to_datetime(df.PLANNED_DEST_WTT_DATETIME_AFF)
    df.loc[:, 'DEST_MONTH'] = df.PLANNED_DEST_WTT_DATETIME_AFF.dt.month
    df.loc[:, 'DEST_DAY'] = df.PLANNED_DEST_WTT_DATETIME_AFF.dt.day
    df.loc[:, 'DEST_HOUR'] = df.PLANNED_DEST_WTT_DATETIME_AFF.dt.hour
    df.loc[:, 'DEST_MINUTE'] = df.PLANNED_DEST_WTT_DATETIME_AFF.dt.minute
    df.drop(columns='PLANNED_DEST_WTT_DATETIME_AFF', inplace = True)

    sin_cos_df = df[['ORIG_MONTH','ORIG_DAY','ORIG_HOUR','ORIG_MINUTE','DEST_MONTH','DEST_DAY','DEST_HOUR','DEST_MINUTE']]

    for col in sin_cos_df.columns:
        final_df = col_transform(col, df)

    return final_df



def col_transform(col_name, df):
    df[f'{col_name}_SIN'] = sin_cos_df[f'{col_name}'].apply(lambda x: math.sin(2 * math.pi * x / 60))
    df[f'{col_name}_COS'] = sin_cos_df[f'{col_name}'].apply(lambda x: math.cos(2 * math.pi * x / 60))
    df.drop(columns=[col_name], inplace=True)
    return df
