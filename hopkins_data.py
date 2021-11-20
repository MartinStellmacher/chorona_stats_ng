from pathlib import Path
import requests
import pandas as pd
import datetime

# even when not using Git clone still keep the Hopkins filesystem structure
hopkins_confirmed_name = 'time_series_covid19_confirmed_global.csv'
hopkins_death_name = 'time_series_covid19_deaths_global.csv'
hopkins_data_path = Path('./data/COVID-19/csse_covid_19_data')
hopkins_time_series_path = hopkins_data_path / 'csse_covid_19_time_series'
hopkins_confirmed_path = hopkins_time_series_path / hopkins_confirmed_name
hopkins_death_path = hopkins_time_series_path / hopkins_death_name
hopkins_data_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
                   'csse_covid_19_time_series/'
hopkins_confirmed_url = hopkins_data_url + hopkins_confirmed_name
hopkins_killed_url = hopkins_data_url + hopkins_death_name
hopkins_population_path = hopkins_data_path / 'UID_ISO_FIPS_LookUp_Table.csv'


def curl_file(url, destination_path):
    if not destination_path.exists() or \
            datetime.datetime.fromtimestamp(destination_path.stat().st_mtime).date() != datetime.date.today():
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(url)
        open(destination_path, 'wb').write(r.content)


def get_time_series_data_by_country(remote_name, local_path):
    curl_file(hopkins_data_url + remote_name, local_path)
    df = pd.read_csv(local_path)
    # drop Province/State
    df = df.groupby('Country/Region').sum()
    # drop senseless summed Lat and Long columns
    df = df.iloc[:, 2:]
    # return deep copy
    return df.copy()


def get_confirmed_by_country():
    return get_time_series_data_by_country('time_series_covid19_confirmed_global.csv', hopkins_confirmed_path)


def get_death_by_country():
    return get_time_series_data_by_country('time_series_covid19_deaths_global.csv', hopkins_death_path)


def get_population_by_country():
    curl_file('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv',
              hopkins_population_path)
    df = pd.read_csv(hopkins_population_path)
    # for countries with Province/State there is one row with the sum ...
    df = df[df['Province_State'].isna()]
    # drop senseless summed Lat and Long columns
    df = df.set_index('Country_Region').Population
    # return deep copy
    return df.copy()
