import dash
from dash import dash_table
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.dash_table.Format import Format, Scheme
from dash.dash_table import FormatTemplate

import plotly.express as px
import plotly.graph_objects as go

from covid_stats import CovidData

covid_data = CovidData()
overview_df = covid_data.create_overview()

column_names = {
    'country': 'Country',
    'confirmed_yesterday': 'Confirmed Yesterday',
    'death_yesterday': 'Death Yesterday',
    'Population': 'Population',
    'weekly_incidence': 'Weekly Incidence',
    'confirmed_overall': 'Confirmed Overall',
    'death_overall': 'Death Overall',
    'confirmed_100k': 'Confirmed',
    'death_100k': 'Death',
    'confirmed_to_kill': 'Killed/confirmed',
    'weekly_death_rate': 'Weekly Death Rate',
}

integer_format = Format().group(True)

column_formats = {
    'country': Format(),
    'confirmed_yesterday': integer_format,
    'death_yesterday': integer_format,
    'Population': integer_format,
    'weekly_incidence': Format(precision=2, scheme=Scheme.fixed),
    'confirmed_overall': integer_format,
    'death_overall': integer_format,
    'confirmed_100k': FormatTemplate.percentage(3),
    'death_100k': FormatTemplate.percentage(6),
    'confirmed_to_kill': FormatTemplate.percentage(3),
    'weekly_death_rate': Format(precision=2, scheme=Scheme.fixed),
}

sub_graphs = ['daily-confirmed-graph', 'daily-death-graph', 'incidence-graph', 'incidence-rank-graph',
              'confirmed-graph', 'death_rate-graph', 'death_rank-graph', 'death-graph', 'death_per_confirmed',
              'death_per_confirmed_rank']

app = dash.Dash(__name__)

app.layout = html.Div(
    # className="w3-black",
    children=[
        dash_table.DataTable(
            id='table',
            columns=[{"name": column_names[i], "id": i, "type": 'numeric', "format": column_formats[i]}
                     for i in overview_df.columns],
            data=overview_df.to_dict('records'),
            page_action="native",
            page_current=0,
            page_size=15,
            row_selectable="multi",
            selected_rows=[overview_df.index[overview_df.country == 'Germany'][0]],
            filter_action="native",
            sort_action="native",
            sort_mode="single",
        )] + [dcc.Graph(id=sub_graph, config={"displaylogo": False}, figure=go.Figure()) for sub_graph in sub_graphs] +
        [html.Div(style={"margin-top": 30}),
         dcc.Slider(id="shift_slider", min=-20, max=20, step=1, value=0, included=True,
                    tooltip={'always_visible': True, 'placement': 'bottom'}),
         dcc.Graph(id="death_per_confirmed_shifted", config={"displaylogo": False}, figure=go.Figure())]
)


def create_px_line(df, column):
    return px.line(df, x='Date', y=column, color='Country')


@app.callback(
    *[Output(component_id=sub_graph, component_property='figure') for sub_graph in sub_graphs],
    Output(component_id="death_per_confirmed_shifted", component_property='figure'),
    Input(component_id='shift_slider', component_property='value'),
    Input(component_id='table', component_property='selected_rows')
)
def update_output_div(offset, countries):
    selected_countries = overview_df[overview_df.index.isin(countries)].country.to_list()
    return \
        create_px_line(*covid_data.get_confirmed_yesterday_100k(selected_countries, 'Confirmed Yesterday / 100k')), \
        create_px_line(*covid_data.get_death_yesterday_100k(selected_countries, 'Death Yesterday / 100k')), \
        create_px_line(*covid_data.get_seven_day_incidences(selected_countries, 'Seven Day Incidence')), \
        create_px_line(*covid_data.get_seven_day_incidences_ranking(selected_countries, 'Seven Day Incidence Rank')), \
        create_px_line(*covid_data.confirmed_sum_100k(selected_countries, 'Confirmed Sum per 100k')), \
        create_px_line(*covid_data.death_rate(selected_countries, 'Seven Day Death Rate')), \
        create_px_line(*covid_data.death_rank(selected_countries, 'Seven Day Death Rank')), \
        create_px_line(*covid_data.death_sum_100k(selected_countries, 'Death Sum per 100k')), \
        create_px_line(*covid_data.get_death_per_confirmed(selected_countries, 'Death / Confirmed [%]')), \
        create_px_line(*covid_data.get_death_per_confirmed_rank(selected_countries, 'Death / Confirmed Rank')), \
        create_px_line(*covid_data.get_death_per_confirmed_shifted(selected_countries, offset, 'Death / Confirmed [%]'))


if __name__ == '__main__':
    app.run_server(debug=True)
