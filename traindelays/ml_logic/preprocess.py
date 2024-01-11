import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression

def preprocessing_pipe():
    num_transformer = MinMaxScaler()

    cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output = False)

    transformer = make_column_transformer((num_transformer, ['Lat_OR','Lon_OR', 'Lat_DES','Lon_DES']),
                                  (cat_transformer, ['ENGLISH_DAY_TYPE', 'SERVICE_GROUP_CODE_AFFECTED', 'INCIDENT_REASON',
                                                        'UNIT_CLASS_AFFECTED', 'TRAIN_SERVICE_CODE_AFFECTED',
                                                     'PERFORMANCE_EVENT_CODE',
                                                     'APP_TIMETABLE_FLAG_AFF']),
                                remainder = 'passthrough')

    pipe = Pipeline([('transformer', transformer)])
    return pipe
