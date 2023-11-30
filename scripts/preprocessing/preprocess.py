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
