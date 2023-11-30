import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder

def encoder(df):
    # Define data
    data = df[['ENGLISH_DAY_TYPE', 'PERFORMANCE_EVENT_CODE', 'OPERATOR_AFFECTED']]

    # Instantiate train and transform OHE and put new columns into df
    ohe = OneHotEncoder(sparse=False).fit(data)
    df[ohe.get_feature_names_out()] = ohe.transform(data)

    # Drop existing columns and add new CANCELLATIONS and DELAYS
    df.drop(columns=['ENGLISH_DAY_TYPE', 'PERFORMANCE_EVENT_CODE', 'OPERATOR_AFFECTED'], inplace=True)
    df['CANCELLATIONS'] = df['PERFORMANCE_EVENT_CODE_A'] = df['PERFORMANCE_EVENT_CODE_M']
    df['DELAYS'] = df['PERFORMANCE_EVENT_CODE_C'] + df['PERFORMANCE_EVENT_CODE_D'] + df['PERFORMANCE_EVENT_CODE_O'] + df['PERFORMANCE_EVENT_CODE_P'] + df['PERFORMANCE_EVENT_CODE_S'] + df['PERFORMANCE_EVENT_CODE_F']

    # Drop the columns which made up the CANCELLATIONS and DELAYS column
    df.drop(columns=['PERFORMANCE_EVENT_CODE_A', 'PERFORMANCE_EVENT_CODE_C',
       'PERFORMANCE_EVENT_CODE_D', 'PERFORMANCE_EVENT_CODE_F',
       'PERFORMANCE_EVENT_CODE_M', 'PERFORMANCE_EVENT_CODE_O',
       'PERFORMANCE_EVENT_CODE_P', 'PERFORMANCE_EVENT_CODE_S'], inplace=True)
    return df
