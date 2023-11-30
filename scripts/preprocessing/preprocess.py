# Data manipulation
import pandas as pd
import numpy as np

# ML Processes
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline, FunctionTransformer
from sklearn.compose import ColumnTransformer

# External function
from cleaner import cleaner, missing_columns
from encoder import *
from scaler import *

def preprocessing(df, unique_vals):
    df_clean = cleaner(df)
    df_encoded = encoder(df_clean)
    df = scaler(df_encoded)
    df = missing_columns(df, unique_vals=unique_vals)
    print(f"done preprocessing with shape {df.shape}")
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
