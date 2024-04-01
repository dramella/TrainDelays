# Libraries
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import pytz
from ml_logic.params import *
from ml_logic import utils as u
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.pipeline import Pipeline


class DropColumnsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop = ['START_STANOX', 'END_STANOX',
    'PLANNED_ORIG_WTT_DATETIME_AFF', 'PLANNED_DEST_WTT_DATETIME_AFF',
    'FINANCIAL_YEAR_AND_PERIOD', 'ORIGIN_DEPARTURE_DATE', 'INCIDENT_CREATE_DATE',
    'INCIDENT_START_DATETIME', 'INCIDENT_END_DATETIME', 'TRAILING_LOAD_AFFECTED',
    'TIMING_LOAD_AFFECTED', 'REACT_TRAIN', 'INCIDENT_RESPONSIBLE_TRAIN', 'RESP_TRAIN',
    'INCIDENT_EQUIPMENT', 'INCIDENT_NUMBER', 'TRUST_TRAIN_ID_AFFECTED',
    'INCIDENT_RESPONSIBLE_TRAIN', 'RESP_TRAIN', 'INCIDENT_EQUIPMENT',
    'INCIDENT_NUMBER', 'INCIDENT_DESCRIPTION', 'EVENT_DATETIME',
    'TRAIN_SERVICE_CODE_AFFECTED','TRACTION_TYPE_AFFECTED','SECTION_CODE',
    'NETWORK_RAIL_LOCATION_MANAGER','PLANNED_ORIG_GBTT_DATETIME_AFF', 'PLANNED_DEST_GBTT_DATETIME_AFF']):
        self.columns_to_drop = columns_to_drop

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.columns_to_drop is not None:
            X_dropped = X.drop(columns=self.columns_to_drop, errors='ignore')
        else:
            X_dropped = X.copy()  # If no columns are specified, return a copy of the input DataFrame

        return X_dropped

    def get_params(self, deep=True):
        return {'columns_to_drop': self.columns_to_drop}

    def set_params(self, **parameters):
        self.columns_to_drop = parameters['columns_to_drop']
        return self

    def get_feature_names_out(self, input_features=None):
        return list(input_features.columns)  # Return the remaining columns

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y)
        return self.transform(X)



class BoxingDayHolidayNormalization(BaseEstimator, TransformerMixin):
    def __init__(self, english_day_col = 'ENGLISH_DAY_TYPE'):
        self.english_day_col = english_day_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed.loc[X_transformed[self.english_day_col] == 'BD', self.english_day_col] = 'BH'
        return X_transformed

    def get_params(self, deep=True):
        return {}

    def set_params(self, **parameters):
        return self

    def get_feature_names_out(self, input_features=None):
        return list(input_features)

class ApplyDstOffsetTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, zone='Europe/London', time_columns=['PLANNED_ORIG_GBTT_DATETIME_AFF', 'PLANNED_DEST_GBTT_DATETIME_AFF']):
        self.zone = zone
        self.time_columns = time_columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        target_timezone = pytz.timezone(self.zone)

        for col in self.time_columns:
            X[col] = X[col].apply(lambda dt: dt - target_timezone.dst(dt) if pd.notnull(dt) and dt.tzinfo is None else dt)

        return X

    def get_params(self, deep=True):
        return {"zone": self.zone}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

    def get_feature_names_out(self, input_features=None):
        return list(input_features)



class CyclicalFeatureTransformer(BaseEstimator, TransformerMixin):
    def __init__(self,time_columns = ['PLANNED_ORIG_GBTT_DATETIME_AFF', 'PLANNED_DEST_GBTT_DATETIME_AFF']):
        self.time_columns = time_columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()

        for col in self.time_columns:
            max_values = {'day':7,'week':53,'year':360}
            for d in max_values:
                X_transformed[col + '_' + d + '_sin'] = np.sin(2 * np.pi * X_transformed[col].dt.dayofweek / max_values[d])
                X_transformed[col + '_' + d + '_cos'] = np.cos(2 * np.pi * X_transformed[col].dt.dayofweek / max_values[d])

        return X_transformed

    def get_params(self, deep=True):
        return {}

    def set_params(self, **parameters):
        return self
    def get_feature_names_out(self, input_features=None):
        return list(input_features)


class GeographicalFeaturesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, service_account = SERVICE_ACCOUNT, gcp_project = GCP_PROJECT, bq_dataset = BQ_DATASET, geo_coordinates_table_id = GEO_COOORDINATES_TABLE_ID):
        self.service_account = service_account
        self.gcp_project = gcp_project
        self.bq_dataset = bq_dataset
        self.geo_coordinates_table_id = geo_coordinates_table_id

    def fit(self, X, y=None):
        # You can perform any necessary setup or computations here
        return self

    def transform(self, X):
        lon_lat_df = u.read_data_from_bq(
            credentials=self.service_account,
            gcp_project=self.gcp_project,
            bq_dataset=self.bq_dataset,
            table=self.geo_coordinates_table_id
        )

        lon_lat_df = lon_lat_df[['Stanox', 'Latitude', 'Longitude']]

        # Merge on ORIG location
        X = pd.merge(X, lon_lat_df, left_on='PLANNED_ORIG_LOC_CODE_AFF', right_on='Stanox', how='left')
        X.rename(columns={'Latitude': 'ORIG_LAT', 'Longitude': 'ORIG_LON'}, inplace=True)

        # Merge on DEST location
        X = pd.merge(X, lon_lat_df, left_on='PLANNED_DEST_LOC_CODE_AFFECTED', right_on='Stanox', how='left')
        X.rename(columns={'Latitude': 'DEST_LAT', 'Longitude': 'DEST_LON'}, inplace=True)

        # Drop unnecessary columns
        X.drop(columns=['PLANNED_ORIG_LOC_CODE_AFF', 'PLANNED_DEST_LOC_CODE_AFFECTED', 'Stanox_x', 'Stanox_y'], inplace=True)

        return X

    def get_params(self, deep=True):
        return {
            "service_account": self.service_account,
            "gcp_project": self.gcp_project,
            "bq_dataset": self.bq_dataset,
            "geo_coordinates_table_id": self.geo_coordinates_table_id
        }

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

    def get_feature_names_out(self, input_features=None):
        return list(input_features) + ['ORIG_LAT', 'ORIG_LON', 'DEST_LAT', 'DEST_LON']

class ResponsibleManagerGroupingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, manager_col = 'RESPONSIBLE_MANAGER', threshold=1500):
        self.threshold = threshold
        self.manager_col = manager_col
        self.other_managers_labels = None

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        value_counts = X[self.manager_col].value_counts()
        self.other_managers_labels = value_counts[value_counts < self.threshold].index
        X_copy = X.copy()
        X_copy[self.manager_col] = X_copy[self.manager_col].apply(
            lambda w: "Other" if w in self.other_managers_labels else w
        )
        return X_copy

    def get_params(self, deep=True):
        return {"threshold": self.threshold}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
    def get_feature_names_out(self, input_features=None):
        return list(input_features)


class IncidentReasonMappingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, incident_reason_col = 'INCIDENT_REASON', service_account=SERVICE_ACCOUNT, gcp_project=GCP_PROJECT, bq_dataset=BQ_DATASET, table=INCIDENT_REASON_CODES_TABLE_ID):
        self.service_account = service_account
        self.gcp_project = gcp_project
        self.bq_dataset = bq_dataset
        self.table = table
        self.incident_reason_col = incident_reason_col

    def fit(self, X, y=None):
        # No fitting necessary for this transformer
        return self

    def transform(self, X):
        incident_reason_mapping = u.read_data_from_bq(
            credentials=self.service_account,
            gcp_project=self.gcp_project,
            bq_dataset=self.bq_dataset,
            table=self.table
        )

        # Merge the DataFrame with incident_reason_mapping
        X = X.merge(
            incident_reason_mapping[['Incident_Reason', 'Incident_Category_Super_Group_Code']],
            right_on='Incident_Reason',
            left_on=self.incident_reason_col,
            how='left'
        )

        # Drop unnecessary columns
        X.rename(str.upper, axis='columns',inplace=True)
        X.drop(columns=[self.incident_reason_col, 'Incident_Reason'], inplace=True, errors='ignore')

        return X

    def get_params(self, deep=True):
        return {
            "service_account": self.service_account,
            "gcp_project": self.gcp_project,
            "bq_dataset": self.bq_dataset,
            "table": self.table
        }

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

    def get_feature_names_out(self, input_features=None):
        # Assuming transformation drops or modifies 'INCIDENT_REASON' and 'Incident_Reason' columns
        remaining_columns = [col for col in input_features if col not in ['INCIDENT_REASON', 'Incident_Reason']]
        return remaining_columns

class ReactionaryReasonCodeMapping(BaseEstimator, TransformerMixin):
    def __init__(self, react_reason_code = 'REACTIONARY_REASON_CODE'):
        self.react_reason_code = react_reason_code

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed[self.react_reason_code] = X_transformed[self.react_reason_code].map(lambda c: 'Primary' if c in [None, True] else 'Reactionary')
        return X_transformed

    def get_params(self, deep=True):
        return {}

    def set_params(self, **parameters):
        return self

    def get_feature_names_out(self, input_features=None):
        # Assuming you are only modifying the 'REACTIONARY_REASON_CODE' column
        output_features = input_features.copy()
        return output_features



numerical_steps = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scale', StandardScaler())])
categorical_steps = Pipeline(steps=[
    ('imp', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder())])

col_transf = ColumnTransformer(transformers=[
    ('numerical', numerical_steps, make_column_selector(dtype_include = 'float')),
    ('categorical', categorical_steps, make_column_selector(dtype_include='object'))
    ])

pipe = Pipeline([('daylight_saving',ApplyDstOffsetTransformer()),
                 ('cyclical_features',CyclicalFeatureTransformer()),
                 ('boxing_day_correction', BoxingDayHolidayNormalization()),
                 ('responsible_manager',ResponsibleManagerGroupingTransformer()),
                 ('reactionary_reason_code', ReactionaryReasonCodeMapping()),
                 ('incident_reason', IncidentReasonMappingTransformer()),
                 ('drop_redundant_cols', DropColumnsTransformer()),
                 ('geo_coordinates', GeographicalFeaturesTransformer()),
                 ('type_specific_tranform', col_transf)
                ])
