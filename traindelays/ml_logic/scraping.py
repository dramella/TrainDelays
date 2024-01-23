import os
import string
import requests
import pandas as pd
from bs4 import BeautifulSoup

def create_toc_operator_mapping(clean = True, to_csv = True):
    """
    Creates a dataframe mapping STANOX codes and locations name.
    Args:
        clean (bool) = If true, only Code and Train operators columns are kept.
        to_csv (bool) = If true, the dataframe is exported in CSV to the ../raw_data folder.
                        If folder does not exists, it is created.
    Returns:
        dataframe : cleaned dataframe containing only the Code and Train operators columns.
    """
    url = "http://www.railwaycodes.org.uk/operators/toccodes.shtm"
    response = requests.get(url=url, headers={"Accept-Language":"en-US"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # in each page select the table identified by the id "tablesort"
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
            row_data = [td.text.strip() for td in row.find_all('td')]
            data.append(row_data)
        # create df
        df = pd.DataFrame(data, columns=headers)
    else:
        print(response.status_code)
    if clean == True:
        df = df[['Code','Train operator']]
    if to_csv:
    # if param csv is true, dataframe is also saved as a .csv in the ../raw_data folder.
        folder_path = "../raw_data"
        file_name = "toc_operators_mapping.csv"
        # if raw_data folder does not exists, create it.
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        df.to_csv(os.path.join(folder_path, file_name))
        print(f"{file_name} saved in {folder_path}")
    return df

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
            # append df to list of dfs
            list_dfs.append(df)
        else:
            # print the status code if the request failed
            print(f"Letter {url} could not be scraped. Status Code: {response.status_code}")
    # return a dataframe with all the information scraped for each page
    return pd.concat(list_dfs)

def clean_stanox_mapping_df(df):
    """
    Cleans a dataframe obtained from scraping stanox codes.
    Args:
        df (dataframe) = DataFrame obtained by scraping stanox codes.

    Returns:
        dataframe : cleaned dataframe containing only the Location and STANOX columns.
    """
    #drop rows where Stanox codes are null
    null_mask = (df['STANOX'].isnull())
    df = df[~null_mask]
    #drop rows where Stanox codes are empty
    empty_mask = (df['STANOX'] == "")
    df = df[~empty_mask]
    # drop rows where Stanox codes are "-""
    invalid_mask = (df['STANOX'] == "-")
    df = df[~invalid_mask]
    #drop redundant cols
    return df

def create_stanox_location_mapping(clean = True, to_csv = True):
    """
    Creates a dataframe mapping STANOX codes and locations name.
    Args:
        clean (bool) = If true, rows with empty and null STANOX codes are dropped.
                        Only STANOX and Location columns are kept.
        to_csv (bool) = If true, the dataframe is exported in CSV to the ../raw_data folder.
                        If folder does not exists, it is created.
    Returns:
        dataframe : cleaned dataframe containing only the Location and STANOX columns.
    """
    # create a dataframe with all the data scraped from the http://www.railwaycodes.org.uk/
    df = scrape_stanox_codes()
    # if param clean is true, it removes empty, invalid and null STANOX codes. Keep only Location and Stanox Code column.
    if clean == True:
        df = clean_stanox_mapping_df(df)
    if to_csv == True:
    # if param csv is true, dataframe is also saved as a .csv in the ../raw_data folder.
        folder_path = "../raw_data"
        file_name = "stanox_locations_mapping.csv"
        # if raw_data folder does not exists, create it.
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        df.to_csv(os.path.join(folder_path, file_name))
        print(f"{file_name} saved in {folder_path}")
    return df
