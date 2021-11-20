import hopkins_data
import pandas as pd
import plotly.express as px

class CovidData:

    def __init__(self):
        self.confirmed_df = hopkins_data.get_confirmed_by_country()
        self.death_df = hopkins_data.get_death_by_country()
        self.population_df = hopkins_data.get_population_by_country()
        assert len(set(self.confirmed_df.index)-set(self.population_df.index)) == 0
        self.seven_day_incidence = self.confirmed_df.diff(7, axis=1).divide(self.population_df, axis=0)*100000

    def create_overview(self):  # todo
        df = pd.concat([
            self.confirmed_df.diff(1, axis=1).iloc[:, -1].to_frame('confirmed_yesterday'),
            self.death_df.diff(1, axis=1).iloc[:, -1].to_frame('death_yesterday'),
            self.population_df,
            self.seven_day_incidence.iloc[:, -1].to_frame('weekly_incidence'),
            self.confirmed_df.iloc[:, -1].to_frame('confirmed_overall'),
            self.death_df.iloc[:, -1].to_frame('death_overall'),
            self.confirmed_df.iloc[:, -1].divide(self.population_df).to_frame('confirmed_100k'),
            self.death_df.iloc[:, -1].divide(self.population_df).to_frame('death_100k'),
            (self.death_df.iloc[:, -1]/self.confirmed_df.iloc[:, -1]).to_frame('confirmed_to_kill'),
        ], axis=1)
        return df.clip(lower=0).reset_index().rename(columns={'index': 'country'})

    def get_seven_day_incidences(self, countries=None):
        # clip negative values
        sdi = self.seven_day_incidence.clip(lower=0)
        if countries == None:
            # selct countries with incidence > 50
            sdi = sdi[sdi.iloc[:, -1] > 50]
        else:
            sdi = sdi.loc[countries]
        # stack data
        return sdi.stack().reset_index().rename(
            columns={'level_0': 'Country', 'level_1': 'Date', 0: 'Seven Day Incidence'})

    def get_confirmed_yesterday_100k(self, countries=None):
        df = self.confirmed_df.diff(1, axis=1).divide(self.population_df, axis=0)*100000
        # clip negative values
        df = df.clip(lower=0)
        if countries == None:
            # selct countries with incidence > 50
            df = df[df.iloc[:, -1] > 50]
        else:
            df = df.loc[countries]
        # stack data
        return df.stack().reset_index().rename(
            columns={'level_0': 'Country', 'level_1': 'Date', 0: 'Confirmed Yesterday / 100k'})

    def get_death_yesterday_100k(self, countries=None):
        df = self.death_df.diff(1, axis=1).divide(self.population_df, axis=0)*100000
        # clip negative values
        df = df.clip(lower=0)
        if countries == None:
            # selct countries with incidence > 50
            df = df[df.iloc[:, -1] > 50]
        else:
            df = df.loc[countries]
        # stack data
        return df.stack().reset_index().rename(
            columns={'level_0': 'Country', 'level_1': 'Date', 0: 'Death Yesterday / 100k'})

    def confirmed_sum_100k(self, countries=None):
        df = self.confirmed_df.divide(self.population_df, axis=0)*100000
        # clip negative values
        df = df.clip(lower=0)
        if countries == None:
            # selct countries with incidence > 50
            df = df[df.iloc[:, -1] > 50]
        else:
            df = df.loc[countries]
        # stack data
        return df.stack().reset_index().rename(
            columns={'level_0': 'Country', 'level_1': 'Date', 0: 'Confirmed Sum per 100k'})

    def death_sum_100k(self, countries=None):
        df = self.death_df.divide(self.population_df, axis=0)*100000
        # clip negative values
        df = df.clip(lower=0)
        if countries == None:
            # selct countries with incidence > 50
            df = df[df.iloc[:, -1] > 50]
        else:
            df = df.loc[countries]
        # stack data
        return df.stack().reset_index().rename(
            columns={'level_0': 'Country', 'level_1': 'Date', 0: 'Death Sum per 100k'})


if __name__ == '__main__':
    covid_data = CovidData()
    covid_data.create_overview()
    fig = px.line(covid_data.get_seven_day_incidences(), x='Date', y='Seven Day Incidence', color='Country', template='plotly_dark')
    fig.show()

    print('done')



