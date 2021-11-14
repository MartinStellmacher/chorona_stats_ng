from pathlib import Path
import pandas as pd
import datetime

hopkins_time_series_path = Path('./data/COVID-19') / 'csse_covid_19_data/csse_covid_19_time_series'
hopkins_confirmed_path = hopkins_time_series_path / "time_series_covid19_confirmed_global.csv"
hopkins_death_path = hopkins_time_series_path / "time_series_covid19_deaths_global.csv"
hopkins_recovered_path = hopkins_time_series_path / "time_series_covid19_recovered_global.csv"

hopkins_population_path = Path('./data/COVID-19') / 'csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv'


# git update
def update_git():
    import git

    repo = git.Repo('.')
    repo.submodule_update(recursive=True)
    # history ? e = list(repo.iter_submodules())[0].module().index.entries


def update_curl_confirmed():
    import requests

    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
          'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    hopkins_confirmed_path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    open(hopkins_confirmed_path, 'wb').write(r.content)


def update_curl_population():
    import requests

    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
          'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    hopkins_confirmed_path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    open(hopkins_confirmed_path, 'wb').write(r.content)


def get_confirmed_by_country():
    if not hopkins_confirmed_path.exists() or \
            datetime.datetime.fromtimestamp(hopkins_confirmed_path.stat().st_mtime).date() != datetime.date.today():
        update_curl_confirmed()
    df = pd.read_csv(hopkins_confirmed_path)
    # drop Province/State
    df = df.groupby('Country/Region').sum()
    # drop senseless summed Lat and Long columns
    df = df.iloc[:, 2:]
    # return deep copy
    return df.copy()


def get_population_by_country():
    if not hopkins_population_path.exists():
        update_curl_population()
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
