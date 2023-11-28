import pandas as pd
from data import load_data_to_bq
from params import *

paths = ['2018 Train Delays',
         '2019 Train Delays',
         '2020 Train Delays',
         '2021 Train Delays',
         '2022 Train Delays',
         '2023 Train Delays']

def load_tables(df, path):
    load_data_to_bq(df, gcp_project=GCP_PROJECT, bq_dataset=BQ_DATASET, table=path)



P05_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P5.csv')
print('-----------Loading P05-----------')
load_tables(P05_2019, paths[1])
print('----------- P05 Uploaded -----------')

# P06_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P6.csv')
# print('-----------Loading P06-----------')
# load_tables(P06_2019, paths[1])
# print('----------- P06 Uploaded -----------')

# P07_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P7.csv')
# print('-----------Loading P07-----------')
# load_tables(P07_2019, paths[1])
# print('----------- P07 Uploaded -----------')

# P08_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P8.csv')
# print('-----------Loading P08-----------')
# load_tables(P08_2019, paths[1])
# print('----------- P08 Uploaded -----------')

# P09_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P9.csv')
# print('-----------Loading P09-----------')
# load_tables(P09_2019, paths[1])
# print('----------- P09 Uploaded -----------')

# P010_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P10.csv')
# print('-----------Loading P010-----------')
# load_tables(P010_2019, paths[1])
# print('----------- P010 Uploaded -----------')

# P011_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P11.csv')
# print('-----------Loading P011-----------')
# load_tables(P011_2019, paths[1])
# print('----------- P011 Uploaded -----------')

# P012_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P12.csv')
# print('-----------Loading P012-----------')
# load_tables(P012_2019, paths[1])
# print('----------- P012 Uploaded -----------')

# P013_2019 = pd.read_csv(f'data/2019 Train Delays/2019-20 P13.csv')
# print('-----------Loading P013-----------')
# load_tables(P013_2019, paths[1])
# print('----------- P013 Uploaded -----------')


# P01_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P1.csv')
# P02_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P2.csv')
# P03_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P3.csv')
# P04_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P4.csv')
# P05_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P5.csv')
# P06_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P6.csv')
# P07_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P7.csv')
# P08_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P8.csv')
# P09_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P9.csv')
# P010_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P10.csv')
# P011_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P11.csv')
# P012_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P12.csv')
# P013_2020 = pd.read_csv(f'data/2020 Train Delays/2020-21-P13.csv')

# P01_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P1.csv')
# P02_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P2.csv')
# P03_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P3.csv')
# P04_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P4.csv')
# P05_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P5.csv')
# P06_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P6.csv')
# P07_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P7.csv')
# P08_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P8.csv')
# P09_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P9.csv')
# P010_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P10.csv')
# P011_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P11.csv')
# P012_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P12.csv')
# P013_2021 = pd.read_csv(f'data/2021 Train Delays/2021-22 P13.csv')


# P01_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P1.csv')
# P02_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P2.csv')
# P03_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P3.csv')
# P04_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P4.csv')
# P05_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P5.csv')
# P06_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P6.csv')
# P07_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P7.csv')
# P08_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P8.csv')
# P09_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P9.csv')
# P010_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P10.csv')
# P011_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P11.csv')
# P012_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P12.csv')
# P013_2022 = pd.read_csv(f'data/2022 Train Delays/2022-23_P13.csv')

# P01_2023 = pd.read_csv(f'data/2023 Train Delays/2023-24 P1.csv')
# P02_2023 = pd.read_csv(f'data/2023 Train Delays/2023-24 P1.csv')
