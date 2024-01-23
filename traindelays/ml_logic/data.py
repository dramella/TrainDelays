import os
import tarfile
import urllib
import requests
import string
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

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


def scrape_stanox_codes():
    """
    Scrapes CRS, NLC, TIPLOC and STANOX Codes from http://www.railwaycodes.org.uk/.
    Returns:
        dataframe : dataframe containing the output scraped from all the letters.
    """
    # create a list of all letters
    letters = list(string.ascii_lowercase)
    # initialize list of dfs to fill with each letter dataframe
    list_dfs = []
    for letter in letters:
        # for each letter build a custom URL
        url = f"http://www.railwaycodes.org.uk/crs/crs{letter}.shtm"
        # send request
        response = requests.get(url=url, headers={"Accept-Language":"en-US"})
        # if the request is successful
        if response.status_code == 200:
            # parse html page
            soup = BeautifulSoup(response.content, "html.parser")
            # select the table identified by the id "tablesort" from the soup
            table = soup.find('table', {'id': 'tablesort'})
            # initialize empty data and headers list
            data = []
            headers = []
            # extract header row
            header_row = table.find('tr')
            for th in header_row.find_all('th'):
                headers.append(th.text.strip())
            # extract rows
            for row in table.find_all('tr')[1:]:
                row_data = [td.text.strip() for td in row.find_all('td')[:6]]
                data.append(row_data)
            # create df
            df = pd.DataFrame(data, columns=headers)
            df.replace(['', '-'], np.nan, inplace=True)
            df = df.map(lambda x: x.split('\n')[0] if isinstance(x, str) else x)
            # append df to list of dfs
            list_dfs.append(df)
        else:
            # print the status code if the request failed
            print(f"Letter {url} could not be scraped. Status Code: {response.status_code}")
    # return a dataframe with all the information scraped for each page
    return pd.concat(list_dfs)


