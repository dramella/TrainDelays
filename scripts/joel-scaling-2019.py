#!/usr/bin/env python
# coding: utf-8

# In[62]:


import pandas as pd
import numpy as np

get_ipython().system('pwd')

df = pd.read_csv("Delays-2019-20-P01.csv")
df

df.info()

df.drop(columns = ['FINANCIAL_YEAR_AND_PERIOD',
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
                 'INCIDENT_RESPONSIBLE_TRAIN', 'EVENT_DATETIME'
                ], inplace=True)

df.drop(columns=['TRAILING_LOAD_AFFECTED','TIMING_LOAD_AFFECTED', 'UNIT_CLASS_AFFECTED','INCIDENT_EQUIPMENT','TRUST_TRAIN_ID_REACT','TRUST_TRAIN_ID_RESP'], inplace=True)

df.head(30)

df.dropna(inplace=True)

df.shape

df

df.isnull().sum().sort_values(ascending = False)

import matplotlib.pyplot as plt

plt.hist(df.PFPI_MINUTES, bins=100);

df.PFPI_MINUTES.mean()

df.sort_values(by='PFPI_MINUTES', ascending=False)

df.PFPI_MINUTES.value_counts(ascending = False)

df.shape

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler

fitted = scaler.fit(df[['PFPI_MINUTES']])
fitted

scaled_transform = scaler.transform(df[['PFPI_MINUTES']])
scaled_transform




