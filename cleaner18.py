"""
This is the code for a function that cleans the data for the files from the 2018/2019 data.

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler

#Must import the above first to make the function work.

!pwd

df = pd.read_csv('/home/ben/code/MathmoBen/TrainDelays/All Delays 2018-19.csv')

df.shape
"""
# 
def cleaner18(df):

    df_drop = df.drop(columns = ['FINANCIAL_YEAR_AND_PERIOD',
                 'PLANNED_DEST_WTT_DATETIME_AFF',
                 'PLANNED_ORIG_GBTT_DATETIME_AFF',
                 'PLANNED_ORIG_WTT_DATETIME_AFF',
                 'PLANNED_DEST_GBTT_DATETIME_AFF',
                 'PLANNED_DEST_WTT_DATETIME_AFF',
                 'TRAIN_SCHEDULE_TYPE_AFFECTED',
                 'TRACTION_TYPE_AFFECTED',
                 'TRAILING_LOAD_AFFECTED',
                 'TIMING_LOAD_AFFECTED',
                 'UNIT_CLASS_AFFECTED',
                 'INCIDENT_NUMBER',
                 'INCIDENT_CREATE_DATE', 'INCIDENT_START_DATETIME',
                 'INCIDENT_END_DATETIME', 'SECTION_CODE',
                 'NETWORK_RAIL_LOCATION_MANAGER', 'RESPONSIBLE_MANAGER',
                 'ATTRIBUTION_STATUS', 'INCIDENT_EQUIPMENT',
                 'INCIDENT_DESCRIPTION', 'REACTIONARY_REASON_CODE',
                 'INCIDENT_RESPONSIBLE_TRAIN', 'EVENT_DATETIME',
                 'TRUST_TRAIN_ID_RESP',
                 'TRUST_TRAIN_ID_REACT'
                ])

    df_drop = df_drop.dropna()

    df_small = df_drop[df_drop['OPERATOR_AFFECTED'] != 'ZZ']


    ohe = OneHotEncoder(sparse = False)

    ohe.fit(df_small[['ENGLISH_DAY_TYPE']]) 

    df_small[ohe.get_feature_names_out()] = ohe.transform(df_small[['ENGLISH_DAY_TYPE']])

    ohe.fit(df_small[['PERFORMANCE_EVENT_CODE']]) 

    df_small[ohe.get_feature_names_out()] = ohe.transform(df_small[['PERFORMANCE_EVENT_CODE']])

    ohe.fit(df_small[['OPERATOR_AFFECTED']]) 

    df_small[ohe.get_feature_names_out()] = ohe.transform(df_small[['OPERATOR_AFFECTED']])

    df_big = df_small.drop(columns = ['ENGLISH_DAY_TYPE', 'PERFORMANCE_EVENT_CODE', 'OPERATOR_AFFECTED']) 

    df_big['CANCELATIONS'] = df_big['PERFORMANCE_EVENT_CODE_A'] + df_big['PERFORMANCE_EVENT_CODE_M']

    df_big['DELAYS'] = df_big['PERFORMANCE_EVENT_CODE_C'] + df_big['PERFORMANCE_EVENT_CODE_D'] + df_big['PERFORMANCE_EVENT_CODE_O'] + df_big['PERFORMANCE_EVENT_CODE_P'] + df_big['PERFORMANCE_EVENT_CODE_S'] + df_big['PERFORMANCE_EVENT_CODE_F']

    df_big.drop(columns = ['PERFORMANCE_EVENT_CODE_A', 'PERFORMANCE_EVENT_CODE_M', 'PERFORMANCE_EVENT_CODE_C', 'PERFORMANCE_EVENT_CODE_D', 'PERFORMANCE_EVENT_CODE_O', 'PERFORMANCE_EVENT_CODE_P', 'PERFORMANCE_EVENT_CODE_S', 'PERFORMANCE_EVENT_CODE_F'], inplace=True)

    scaler = MinMaxScaler()
    scaler.fit(df_big[['PFPI_MINUTES']])
    df_big['PFPI_MINUTES'] = scaler.transform(df_big[['PFPI_MINUTES']])

    return df_big



 