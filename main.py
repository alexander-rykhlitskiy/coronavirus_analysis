import pandas as pd

democracy_url = 'https://en.wikipedia.org/wiki/Democracy_Index'
tables = pd.read_html(democracy_url,header=0)
democracy_pd = tables[2]

coronavirus_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
coronavirus_pd = pd.read_csv(coronavirus_url)
coronavirus_pd = coronavirus_pd.groupby(['Country/Region']).sum() # do not split by Province/State
# coronavirus_pd = coronavirus_pd.groupby(['Country/Region']).agg({x:'sum' for x in coronavirus_pd.columns[3:]}) # do not split by Province/State
# coronavirus_pd.groupby(['Country/Region']).agg({**{'Lat':'mean', 'Long':'mean'}, **{x:'sum' for x in coronavirus_pd.columns[3:]}})

df = pd.merge(democracy_pd, coronavirus_pd, left_on='Country', right_on='Country/Region')#[['Country', 'Score'] + coronavirus_pd.columns[3:].values]

weeks_number = 3
weeks_names = [f'week {i}' for i in range(weeks_number)]
cases_column = []
for row_index, row in df.iterrows():
    initial_date_index = 13
    dates = row[initial_date_index:]
    cases = {}
    for index, value in enumerate(dates.values):
        min_cases_number = 90
        if value >= min_cases_number:
            for i in range(weeks_number):
                last_index = index + i * 7
                if last_index < len(dates):
                    cases[weeks_names[i]] = dates[last_index]
                else:
                    break
            break
    cases_column.append(cases)

df_cases = pd.DataFrame.from_records(cases_column)

result = pd.concat([df, df_cases], axis=1)[['Country'] + weeks_names].sort_values('week 1', ascending=True)

print(result.head(100).to_string(index=False))
