import os
import tarfile
import urllib
def fetch_trains_data(url = 'https://sacuksprodnrdigital0001.blob.core.windows.net/historic-delay-attribution/',
                      financial_years = ['2018-19','2019-20','2020-21','2021-22','2022-23','2023-24'],
                      periods = ['P01','P02','P03','P04','PO5','P06','P07','PO8','P09','P10','P11','P12','P13'],
                      outpath = None):
    if outpath is None:
        outpath = os.makedirs('./data', exist_ok=True)
    for fy in financial_years:
        for p in periods:
            full_url = url + f'{fy}/All-Delays-{fy}-' + f'{p}.zip'
            zipped_data_path = os.makedirs('./zipped_data', exist_ok=True)
            urllib.request.urlretrieve(full_url,zipped_data_path)
            zipped_trains = tarfile.open(zipped_data_path)
            zipped_trains.extractall(outpath)
