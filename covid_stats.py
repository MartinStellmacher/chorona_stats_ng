import hopkins_data
import pandas as pd
import plotly.express as px

confirmed_df = hopkins_data.get_confirmed_by_country()
population_df = hopkins_data.get_population_by_country()

assert len(set(confirmed_df.index)-set(population_df.index)) == 0

seven_day_incidence = confirmed_df.diff(7, axis=1).divide(population_df, axis=0)*100000

# clip negative values
sdi = seven_day_incidence.clip(lower=0)
# selct countries with incidence > 50
sdi = sdi[sdi.iloc[:,-1]>50]
# sort by latest seven day incidence
sdi = sdi.sort_values(sdi.columns[-1], na_position='first')
# stack data
sdi = sdi.stack().reset_index().rename(columns={'level_0': 'Country', 'level_1': 'Date', 0: 'Seven Day Incidence'})

fig = px.line(sdi, x='Date', y='Seven Day Incidence', color='Country', template='plotly_dark')
fig.show()

print('done')



