import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import pytz
from sklearn.utils import _safe_indexing
import joblib
from joblib import Parallel, delayed
from sklearn.base import clone
from traindelays import utils as u

from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.base import BaseEstimator, TransformerMixin

class DropColumnsTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_dropped = X.drop(columns=X.columns, errors='ignore')
        print(f"Dropped all columns.")
        return X_dropped

    def get_params(self, deep=True):
        return {}

    def set_params(self, **parameters):
        return self

    def get_feature_names_out(self, input_features=None):
        return []  # No remaining columns

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y)
        return self.transform(X)




class BoxingDayHolidayNormalization(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed.loc[X_transformed['ENGLISH_DAY_TYPE'] == 'BD', 'ENGLISH_DAY_TYPE'] = 'BH'
        return X_transformed

    def get_params(self, deep=True):
        return {}

    def set_params(self, **parameters):
        return self

    def get_feature_names_out(self, input_features=None):
        return list(input_features)

class ApplyDstOffsetTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, zone='Europe/London'):
        self.zone = zone

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        def apply_dst_offset_row(row):
            target_timezone = pytz.timezone(self.zone)
            return row.apply(lambda dt: dt - target_timezone.dst(dt) if pd.notnull(dt) and dt.tzinfo is None else dt)

        return X.apply(apply_dst_offset_row, axis=1)

    def get_params(self, deep=True):
        return {"zone": self.zone}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

    def get_feature_names_out(self, input_features=None):
        return list(input_features)

class CyclicalFeatureTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()

        for col in X_transformed.columns:
            max_values = {'day':7,'week':53,'year':360}
            for d in max_values:
                X_transformed[col + '_' + d + '_sin'] = np.sin(2 * np.pi * X_transformed[col].dt.dayofweek / max_values[d])
                X_transformed[col + '_' + d + '_cos'] = np.cos(2 * np.pi * X_transformed[col].dt.dayofweek / max_values[d])

        return X_transformed

    def get_params(self, deep=True):
        return {}

    def set_params(self, **parameters):
        return self


class GeographicalFeaturesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, service_account, gcp_project, bq_dataset, geo_coordinates_table_id):
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
    def __init__(self, threshold):
        self.threshold = threshold
        self.other_managers_labels = None

    def fit(self, X, y=None):
        value_counts = X['RESPONSIBLE_MANAGER'].value_counts()
        self.other_managers_labels = value_counts[value_counts < self.threshold].index
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy['RESPONSIBLE_MANAGER'] = X_copy['RESPONSIBLE_MANAGER'].apply(
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
    def __init__(self, service_account, gcp_project, bq_dataset, table):
        self.service_account = service_account
        self.gcp_project = gcp_project
        self.bq_dataset = bq_dataset
        self.table = table

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
            left_on='INCIDENT_REASON',
            how='inner'
        )

        # Drop unnecessary columns
        X.drop(columns=['INCIDENT_REASON', 'Incident_Reason'], inplace=True, errors='ignore')

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
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed['REACTIONARY_REASON_CODE'] = X_transformed['REACTIONARY_REASON_CODE'].map(lambda c: 'Primary' if c is None else 'Reactionary')
        return X_transformed

    def get_params(self, deep=True):
        return {}

    def set_params(self, **parameters):
        return self

    def get_feature_names_out(self, input_features=None):
        # Assuming you are only modifying the 'REACTIONARY_REASON_CODE' column
        output_features = input_features.copy()
        return output_features
