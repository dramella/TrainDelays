# Data manipulation
import pandas as pd
import numpy as np

# ML Processes
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline, FunctionTransformer
from sklearn.compose import ColumnTransformer

# External function
from cleaner import *
from encoder import *
from scaler import *

def preprocessing_raw(df):
    # Cleaning then converting stanox codes into lon and lat values
    df_cleaned = cleaner(df)
    return df_cleaned

def preprocessing(df, unique_vals):
    df_encoded = encoder(df)
    df = scaler(df_encoded)
    print(f"done preprocessing with shape {df.shape}")
    return df

def data_cleaning(df):
    df_clean = cleaner(df)
    return df_clean
