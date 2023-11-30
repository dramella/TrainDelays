import pandas as pd
import numpy as np

def cleaner(df):
    # print(df.columns)
    # Turn columns to upper case
    columns = [col.upper() for col in list(df.columns)]
    df.columns = columns

    # Loop to handel multiple PFPI columns
    if 'NON_PFPI_MINUTES' in df.columns:
        df['PFPI_MINUTES'] = df['PFPI_MINUTES'] + df['NON_PFPI_MINUTES']
        df = df.drop(columns = ['NON_PFPI_MINUTES'])

    #Takes care of pointless column in 2020/21 data
    if 'UNNAMED: 40' in df.columns:
        df = df.drop(columns = ['UNNAMED: 40'])

    if 'UNNAMED: 41' in df.columns:
        df = df.drop(columns = ['UNNAMED: 41'])

    # Defining columns which need to be renamed
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

    # Renaming the columns
    df.rename(columns = cols_to_rename, inplace = True)

    # Dropping the unwanted columns from the df
    df.drop(columns = ['FINANCIAL_YEAR_AND_PERIOD','TRUST_TRAIN_ID_AFFECTED',
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
        'RESP_TRAIN','REACT_TRAIN'], inplace=True)

    # Drop na's and remove 'ZZ' operator
    df = df.dropna(how="any")
    df = df[df['OPERATOR_AFFECTED'] != 'ZZ']
    df = df[df['PFPI_MINUTES'] != 0.0]
    return df

# Maps the stanox codes to the long and latitudes
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
    origin_geo_locations = origin_geo_locations.drop(columns = ['Stanox'])
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
    origin_dest_locations = origin_dest_locations.drop(columns = ['Stanox'])
    new_column_names = {'Latitude': 'Lat_DES', 'Longitude': 'Lon_DES'}
    origin_dest_locations.rename(columns=new_column_names, inplace=True)

    return origin_dest_locations


# Checks if each value inside the unique list of values is in the DF and if not then add the column
def missing_columns(df, unique_vals):
    for val in unique_vals:
        if f'OPERATOR_AFFECTED_{val}' not in df.columns:
            df[f'OPERATOR_AFFECTED_{val}'] = 0
    return df
