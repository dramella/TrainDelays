"""
This is a function that attempts to clean the data, no matter which
year it comes from. To make it work one must first run the
following imports. 

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
"""

def NewCleaner(df):
    
    # Loop to handel multiple PFPI columns
    if 'NON_PFPI_MINUTES' in df.columns:
        df['PFPI_MINUTES'] = df['PFPI_MINUTES'] + df['NON_PFPI_MINUTES']
        df.drop(columns = ['NON_PFPI_MINUTES'])
        
    #Takes care of pointless column in 2020/21 data
    if 'Unnamed: 40' in df.columns:
        df = df.drop(columns = ['Unnamed: 40'])
    print(df.columns)
    #At this point everything has 39 columns. Time to name every
    #column the way the 2018 columns were named. 
    
    cols_to_rename = {
    #New name: old name
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
    
    df.rename(columns = cols_to_rename, inplace = True)
        
    #Now that the names are all the same we can mimic the earlier
    #2018-specific function.
    df_drop = df.drop(columns = ['FINANCIAL_YEAR_AND_PERIOD','TRUST_TRAIN_ID_AFFECTED',
        'PLANNED_DEST_WTT_DATETIME_AFF','PLANNED_ORIG_GBTT_DATETIME_AFF',
        'PLANNED_ORIG_WTT_DATETIME_AFF','PLANNED_DEST_GBTT_DATETIME_AFF',
        'PLANNED_DEST_WTT_DATETIME_AFF','TRAIN_SCHEDULE_TYPE_AFFECTED',
        'TRAIN_SERVICE_CODE_AFFECTED', 'SERVICE_GROUP_CODE_AFFECTED',
        'APP_TIMETABLE_FLAG_AFF', 
        'TRACTION_TYPE_AFFECTED','TRAILING_LOAD_AFFECTED',
        'TIMING_LOAD_AFFECTED','UNIT_CLASS_AFFECTED','INCIDENT_NUMBER',
        'INCIDENT_CREATE_DATE', 'INCIDENT_START_DATETIME',
        'INCIDENT_END_DATETIME', 'SECTION_CODE', 'INCIDENT_REASON',
        'NETWORK_RAIL_LOCATION_MANAGER', 'RESPONSIBLE_MANAGER',
        'ATTRIBUTION_STATUS', 'INCIDENT_EQUIPMENT', 'START_STANOX', 'END_STANOX',
        'INCIDENT_DESCRIPTION', 'REACTIONARY_REASON_CODE',
        'INCIDENT_RESPONSIBLE_TRAIN', 'EVENT_DATETIME',
        'RESP_TRAIN','REACT_TRAIN'])
    
    #drop na's and the irrelevant ZZ operator
    print(df_drop.isnull().sum())
    df_drop = df_drop.dropna(how="any")
    print(df_drop.shape)
    df_small = df_drop[df_drop['OPERATOR_AFFECTED'] != 'ZZ']
    print(df_small.shape)
    #One hot encoding
        
    ohe = OneHotEncoder(sparse = False)

    ohe.fit(df_small[['ENGLISH_DAY_TYPE']]) 

    df_small[ohe.get_feature_names_out()] = ohe.transform(df_small[['ENGLISH_DAY_TYPE']])

    ohe.fit(df_small[['PERFORMANCE_EVENT_CODE']]) 

    df_small[ohe.get_feature_names_out()] = ohe.transform(df_small[['PERFORMANCE_EVENT_CODE']])

    ohe.fit(df_small[['OPERATOR_AFFECTED']]) 

    df_small[ohe.get_feature_names_out()] = ohe.transform(df_small[['OPERATOR_AFFECTED']])

    #remove the now pointless columns
    
    df_big = df_small.drop(columns = ['ENGLISH_DAY_TYPE', 'PERFORMANCE_EVENT_CODE', 'OPERATOR_AFFECTED']) 

    #merge the canelation and delay categories and ditch the now pointless columns
    
    df_big['CANCELATIONS'] = df_big['PERFORMANCE_EVENT_CODE_A'] + df_big['PERFORMANCE_EVENT_CODE_M']

    df_big['DELAYS'] = df_big['PERFORMANCE_EVENT_CODE_C'] + df_big['PERFORMANCE_EVENT_CODE_D'] + df_big['PERFORMANCE_EVENT_CODE_O'] + df_big['PERFORMANCE_EVENT_CODE_P'] + df_big['PERFORMANCE_EVENT_CODE_S'] + df_big['PERFORMANCE_EVENT_CODE_F']

    df_big.drop(columns = ['PERFORMANCE_EVENT_CODE_A', 'PERFORMANCE_EVENT_CODE_M', 'PERFORMANCE_EVENT_CODE_C', 'PERFORMANCE_EVENT_CODE_D', 'PERFORMANCE_EVENT_CODE_O', 'PERFORMANCE_EVENT_CODE_P', 'PERFORMANCE_EVENT_CODE_S', 'PERFORMANCE_EVENT_CODE_F'], inplace=True)
    
    #scale the minutes of delay columns
    
    scaler = MinMaxScaler()
    scaler.fit(df_big[['PFPI_MINUTES']])
    df_big['PFPI_MINUTES'] = scaler.transform(df_big[['PFPI_MINUTES']])

    return df_big