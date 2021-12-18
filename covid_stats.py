import hopkins_data
import pandas as pd


class CovidData:

    def __init__(self):
        self.confirmed_df = hopkins_data.get_confirmed_by_country()
        self.death_df = hopkins_data.get_death_by_country()
        self.population_df = hopkins_data.get_population_by_country()
        assert len(set(self.confirmed_df.index)-set(self.population_df.index)) == 0
        self.seven_day_incidence = self.confirmed_df.diff(7, axis=1).divide(self.population_df, axis=0)*100000
        self.seven_day_death_rate = self.death_df.diff(7, axis=1).divide(self.population_df, axis=0)*100000
        self.death_per_confirmed = 100 * self.seven_day_death_rate / self.seven_day_incidence

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
            self.seven_day_death_rate.iloc[:, -1].to_frame('weekly_death_rate'),
        ], axis=1)
        return df.clip(lower=0).reset_index().rename(columns={'index': 'country'})

    @staticmethod
    def create_time_series_data(df_in, countries, label):
        # select countries
        df = df_in.loc[countries]
        # clip negative values
        df = df.clip(lower=0)
        # stack data
        return df.stack().reset_index().rename(
            columns={'level_0': 'Country', 'level_1': 'Date', 0: label}), label

    def get_seven_day_incidences(self, countries, y_label):
        return CovidData.create_time_series_data(
            self.seven_day_incidence,
            countries, y_label)

    def get_seven_day_incidences_ranking(self, countries, y_label):
        return CovidData.create_time_series_data(
            self.seven_day_incidence.rank(ascending=False),
            countries, y_label)

    def get_confirmed_yesterday_100k(self, countries, y_label):
        return CovidData.create_time_series_data(
            self.confirmed_df.diff(1, axis=1).divide(self.population_df, axis=0)*100000, countries, y_label)

    def get_death_yesterday_100k(self, countries, y_label):
        return CovidData.create_time_series_data(
            self.death_df.diff(1, axis=1).divide(self.population_df, axis=0)*100000, countries, y_label)

    def confirmed_sum_100k(self, countries, y_label):
        return CovidData.create_time_series_data(
            self.confirmed_df.divide(self.population_df, axis=0)*100000, countries, y_label)

    def death_sum_100k(self, countries, y_label):
        return CovidData.create_time_series_data(
            self.death_df.divide(self.population_df, axis=0)*100000, countries, y_label)

    def death_rate(self, countries, y_label):
        return CovidData.create_time_series_data(self.seven_day_death_rate, countries, y_label)

    def death_rank(self, countries, y_label):
        return CovidData.create_time_series_data(self.seven_day_death_rate.rank(ascending=False), countries, y_label)

    def get_death_per_confirmed(self, countries, y_label):
        return CovidData.create_time_series_data(self.death_per_confirmed, countries, y_label)

    def get_death_per_confirmed_rank(self, countries, y_label):
        return CovidData.create_time_series_data(self.death_per_confirmed.rank(ascending=False), countries, y_label)

    def get_death_per_confirmed_shifted(self, countries, offset, y_label):
        df = 100 * self.seven_day_death_rate / self.seven_day_incidence.shift(offset, axis='columns')
        return CovidData.create_time_series_data(df.iloc[:,30+offset:], countries, y_label)
