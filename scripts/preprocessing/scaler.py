import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler

def scaler(df):
    # Define column we want to scale
    X = df[['PFPI_MINUTES']]
    # Fit the scaler on the data
    scaler = StandardScaler().fit(X)
    # Transform the column
    df['PFPI_MINUTES'] = scaler.transform(X)

    return df
