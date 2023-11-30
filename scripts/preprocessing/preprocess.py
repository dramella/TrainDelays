import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import FunctionTransformer, Pipeline

def process_2019(df, unique_vals):
    # Basic Data Cleaning
    df.drop(columns=['TRAILING_LOAD_AFFECTED','TIMING_LOAD_AFFECTED', 'UNIT_CLASS_AFFECTED',
                     'INCIDENT_EQUIPMENT','TRUST_TRAIN_ID_REACT','TRUST_TRAIN_ID_RESP',
                     'FINANCIAL_YEAR_AND_PERIOD',
                     'PLANNED_DEST_WTT_DATETIME_AFF',
                     'PLANNED_ORIG_GBTT_DATETIME_AFF',
                     'PLANNED_ORIG_WTT_DATETIME_AFF',
                     'PLANNED_DEST_GBTT_DATETIME_AFF',
                     'PLANNED_DEST_WTT_DATETIME_AFF',
                     'TRAIN_SCHEDULE_TYPE_AFFECTED',
                     'TRACTION_TYPE_AFFECTED',
                     'INCIDENT_NUMBER',
                     'INCIDENT_CREATE_DATE', 'INCIDENT_START_DATETIME',
                     'INCIDENT_END_DATETIME', 'SECTION_CODE',
                     'NETWORK_RAIL_LOCATION_MANAGER', 'RESPONSIBLE_MANAGER',
                     'ATTRIBUTION_STATUS',
                     'INCIDENT_DESCRIPTION', 'REACTIONARY_REASON_CODE',
                     'INCIDENT_RESPONSIBLE_TRAIN', 'EVENT_DATETIME',
                     'ORIGIN_DEPARTURE_DATE','TRUST_TRAIN_ID_AFFECTED','TRAIN_SERVICE_CODE_AFFECTED',
                     'SERVICE_GROUP_CODE_AFFECTED','APP_TIMETABLE_FLAG_AFF',
                     'INCIDENT_REASON','START_STANOX','END_STANOX'], inplace=True)
    df.dropna(inplace=True)

    # Preprocessing of data
    data = df[['ENGLISH_DAY_TYPE', 'PERFORMANCE_EVENT_CODE', 'OPERATOR_AFFECTED']]
    ohe = OneHotEncoder(sparse=False).fit(data)

    df[ohe.get_feature_names_out()] = ohe.transform(data)
    df.drop(columns=['ENGLISH_DAY_TYPE', 'PERFORMANCE_EVENT_CODE', 'OPERATOR_AFFECTED','OPERATOR_AFFECTED_ZZ'], inplace=True)
    df['CANCELLATIONS'] = df['PERFORMANCE_EVENT_CODE_A'] = df['PERFORMANCE_EVENT_CODE_M']
    df['DELAYS'] = df['PERFORMANCE_EVENT_CODE_C'] + df['PERFORMANCE_EVENT_CODE_D'] + df['PERFORMANCE_EVENT_CODE_O'] + df['PERFORMANCE_EVENT_CODE_P'] + df['PERFORMANCE_EVENT_CODE_S'] + df['PERFORMANCE_EVENT_CODE_F']

    df.drop(columns=['PERFORMANCE_EVENT_CODE_A', 'PERFORMANCE_EVENT_CODE_C',
       'PERFORMANCE_EVENT_CODE_D', 'PERFORMANCE_EVENT_CODE_F',
       'PERFORMANCE_EVENT_CODE_M', 'PERFORMANCE_EVENT_CODE_O',
       'PERFORMANCE_EVENT_CODE_P', 'PERFORMANCE_EVENT_CODE_S'], inplace=True)

    scaler = StandardScaler()
    X_fitted = scaler.fit(df[['PFPI_MINUTES']])
    df['PFPI_MINUTES'] = scaler.transform(df[['PFPI_MINUTES']])

    df = missing_columns(df, unique_vals)
    return df

# These function accounts for the missing TOC codes and adds them to each csv

# Gets the unique TOC values for the given CSV
def unique_vals(df):
    vals = df['OPERATOR_AFFECTED'].unique
    return vals

# Creates a unique list of all the values for the year (run this function 13 times)
def list_of_unique_vals_year(prev_vals, new_vals):
    unique_set = set(prev_vals.append(new_vals))
    return unique_set

# Checks if each value inside the unique list of values is in the DF and if not then add the column
def missing_columns(df, unique_vals):
    for val in unique_vals:
        if f'OPERATOR_AFFECTED_{val}' not in df.columns:
            df[f'OPERATOR_AFFECTED_{val}'] = 0
    return df
