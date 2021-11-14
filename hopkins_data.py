from pathlib import Path
import requests
import pandas as pd
import datetime

# even when not using Git clone still keep the Hopkins filesystem structure
hopkins_data_path = Path('./data/COVID-19/csse_covid_19_data')
hopkins_time_series_path = hopkins_data_path / 'csse_covid_19_time_series'
hopkins_confirmed_path = hopkins_time_series_path / 'time_series_covid19_confirmed_global.csv'
hopkins_population_path = hopkins_data_path / 'UID_ISO_FIPS_LookUp_Table.csv'


def curl_file(url, dest_path):
    if not dest_path.exists() or \
            datetime.datetime.fromtimestamp(dest_path.stat().st_mtime).date() != datetime.date.today():
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(url)
        open(dest_path, 'wb').write(r.content)


def get_confirmed_by_country():
    curl_file('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', hopkins_confirmed_path)
    df = pd.read_csv(hopkins_confirmed_path)
    # drop Province/State
    df = df.groupby('Country/Region').sum()
    # drop senseless summed Lat and Long columns
    df = df.iloc[:, 2:]
    # return deep copy
    return df.copy()


def get_population_by_country():
    curl_file('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv', hopkins_population_path)
    df = pd.read_csv(hopkins_population_path)
    # drop Province/State
    df = df.groupby('Country_Region').sum()
    # drop senseless summed Lat and Long columns
    df = df.Population
    # return deep copy
    return df.copy()


if __name__ == '__main__':
    df_c = get_confirmed_by_country()
    df_p = get_population_by_country()
