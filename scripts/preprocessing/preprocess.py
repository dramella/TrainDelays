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
                     'INCIDENT_RESPONSIBLE_TRAIN', 'EVENT_DATETIME'], inplace=True)
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

def mapping_stanox_geo_coordinates(df, lookup_csv_path = "../mapping_data/Stanox-Geo-Coordinates-Lookup.csv"):
    """
    Extracts the geographical coordinates (longitude and latitude) associated to a Stanox code. Coordinates are
    extracted from a .csv file available at
    https://github.com/alexfrancisross/NetworkRail/blob/master/Stanox-Station-Lookup.csv.

    Parameters:
        - df (DataFrame): the original or preprocessed version of the Delay attribution data.
        - lookup_csv_path (str) : the path where the mapping .csv file is saved.
    Return:
        - DataFrame: the input Dataframe plus the origin and destination coordinates.
    """
    # load mapping data with stanox codes and coordinates
    mapping_df = pd.read_csv(lookup_csv_path)
    # merge mapping dataset with train delays data to get latitude and longitude for origin stanox code
    origin_geo_locations = pd.merge(df,
                        mapping_df,
                        left_on ='PLANNED_ORIG_LOC_CODE_AFF',
                        right_on = 'Stanox' ,
                        how ='left')
    # drop observation w/o origin latitude and longitude, drop redundant columns
    origin_geo_locations = origin_geo_locations.dropna(subset=['Latitude', 'Longitude'])
    origin_geo_locations = origin_geo_locations.drop(columns = ['Stanox', 'PLANNED_ORIG_LOC_CODE_AFF'])
    new_column_names = {'Latitude': 'Lat_OR', 'Longitude': 'Lon_OR'}
    origin_geo_locations.rename(columns=new_column_names, inplace=True)

    # merge mapping dataset with the train delays data to get latitude and longitude for destination stanox code
    origin_dest_locations = pd.merge(origin_geo_locations,
                      mapping_df,
                      left_on ='PLANNED_DEST_LOC_CODE_AFFECTED',
                      right_on = 'Stanox' ,
                      how ='left')
    # drop observation w/o destination latitude and longitude, drop redundant columns
    origin_dest_locations = origin_dest_locations.dropna(subset=['Latitude', 'Longitude'])
    origin_dest_locations = origin_dest_locations.drop(columns = ['Stanox', 'PLANNED_DEST_LOC_CODE_AFFECTED'])
    new_column_names = {'Latitude': 'Lat_DES', 'Longitude': 'Lon_DES'}
    origin_dest_locations.rename(columns=new_column_names, inplace=True)

    return origin_dest_locations
