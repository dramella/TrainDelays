
import pytz
import pandas as pd

def drop_columns(df, columns_to_drop = ['START_STANOX', 'END_STANOX',
    'PLANNED_ORIG_WTT_DATETIME_AFF', 'PLANNED_DEST_WTT_DATETIME_AFF',
    'FINANCIAL_YEAR_AND_PERIOD', 'ORIGIN_DEPARTURE_DATE', 'INCIDENT_CREATE_DATE',
    'INCIDENT_START_DATETIME', 'INCIDENT_END_DATETIME', 'TRAILING_LOAD_AFFECTED',
    'TIMING_LOAD_AFFECTED', 'REACT_TRAIN', 'INCIDENT_RESPONSIBLE_TRAIN', 'RESP_TRAIN',
    'INCIDENT_EQUIPMENT', 'INCIDENT_NUMBER', 'TRUST_TRAIN_ID_AFFECTED',
    'INCIDENT_RESPONSIBLE_TRAIN', 'RESP_TRAIN', 'INCIDENT_EQUIPMENT',
    'INCIDENT_NUMBER', 'INCIDENT_DESCRIPTION', 'EVENT_DATETIME']):
    """
    Drops columns from a DataFrame if any of them is present.

    Parameters:
    - df (pd.DataFrame): The DataFrame to modify.
    - columns_to_drop (list): List of column names to drop.

    Returns:
    - pd.DataFrame: DataFrame with specified columns dropped.
    """
    existing_columns = set(df.columns)
    columns_to_drop = [col for col in columns_to_drop if col in existing_columns]

    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
        print(f"Dropped columns: {', '.join(columns_to_drop)}")
    else:
        print("No columns to drop.")

    return df

def boxing_day_holiday_normalization(data):
    data.loc[data['ENGLISH_DAY_TYPE'] == 'BD','ENGLISH_DAY_TYPE'] = 'BH'
    return data

def apply_dst_offset(row,zone='Europe/London'):
    target_timezone = pytz.timezone(f'{zone}')
    return row.apply(lambda dt: dt - target_timezone.dst(dt) if pd.notnull(dt) and dt.tzinfo is None else dt)
