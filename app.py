# we're gonna download covid data from https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv
# the data is daily updated.
# for more information about data, see https://ourworldindata.org/coronavirus-source-data


import pandas as pd
import numpy as np

import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash_bootstrap_components as dbc
import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import datetime

#from pylab import *


# load data from github.
url_covid = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df = pd.read_csv(url_covid, parse_dates = ["date"])


# 21 February 
# columns: 59 columns ['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases',
      #  'new_cases_smoothed', 'total_deaths', 'new_deaths',
      #  'new_deaths_smoothed', 'total_cases_per_million',
      #  'new_cases_per_million', 'new_cases_smoothed_per_million',
      #  'total_deaths_per_million', 'new_deaths_per_million',
      #  'new_deaths_smoothed_per_million', 'reproduction_rate', 'icu_patients',
      #  'icu_patients_per_million', 'hosp_patients',
      #  'hosp_patients_per_million', 'weekly_icu_admissions',
      #  'weekly_icu_admissions_per_million', 'weekly_hosp_admissions',
      #  'weekly_hosp_admissions_per_million', 'new_tests', 'total_tests',
      #  'total_tests_per_thousand', 'new_tests_per_thousand',
      #  'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
      #  'positive_rate', 'tests_per_case', 'tests_units', 'total_vaccinations',
      #  'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
      #  'new_vaccinations_smoothed', 'total_vaccinations_per_hundred',
      #  'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred',
      #  'new_vaccinations_smoothed_per_million', 'stringency_index',
      #  'population', 'population_density', 'median_age', 'aged_65_older',
      #  'aged_70_older', 'gdp_per_capita', 'extreme_poverty',
      #  'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers',
      #  'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand',
      #  'life_expectancy', 'human_development_index']

# columns to group: 3 columns
group_list = ['iso_code', 'continent', 'location']

# columns unique value 
group_unique =[ 'population', 'population_density', 'median_age', 
              'aged_65_older', 'aged_70_older', 'gdp_per_capita', 'extreme_poverty', 
              'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers', 
              'male_smokers', 'hospital_beds_per_thousand', 
              'life_expectancy', 'human_development_index']

# columns of total characters
total_characters = [ 'total_cases', 'total_deaths','total_cases_per_million','total_deaths_per_million',
                  'total_tests', 'total_tests_per_thousand', 'total_vaccinations', 'people_vaccinated', 
                  'people_fully_vaccinated','total_vaccinations_per_hundred', 'people_vaccinated_per_hundred', 
                  'people_fully_vaccinated_per_hundred']

# columns of daily characters 23 columns
daily_characters = ['new_cases',
       'new_cases_smoothed', 'new_deaths',
       'new_deaths_smoothed',
       'new_cases_per_million', 'new_cases_smoothed_per_million',
       'new_deaths_per_million',
       'new_deaths_smoothed_per_million', 'icu_patients',
       'icu_patients_per_million', 'hosp_patients',
       'hosp_patients_per_million', 'weekly_icu_admissions',
       'weekly_icu_admissions_per_million', 'weekly_hosp_admissions',
       'weekly_hosp_admissions_per_million', 'new_tests', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
       'new_vaccinations',
       'new_vaccinations_smoothed',
       'new_vaccinations_smoothed_per_million']

# columns of rates
rate_characters = ['positive_rate', 'tests_per_case']

# all columns
all_characters = ['total_cases', 'new_cases',
       'new_cases_smoothed', 'total_deaths', 'new_deaths',
       'new_deaths_smoothed', 'total_cases_per_million',
       'new_cases_per_million', 'new_cases_smoothed_per_million',
       'total_deaths_per_million', 'new_deaths_per_million',
       'new_deaths_smoothed_per_million', 'reproduction_rate', 'icu_patients',
       'icu_patients_per_million', 'hosp_patients',
       'hosp_patients_per_million', 'weekly_icu_admissions',
       'weekly_icu_admissions_per_million', 'weekly_hosp_admissions',
       'weekly_hosp_admissions_per_million', 'new_tests', 'total_tests',
       'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
       'positive_rate', 'tests_per_case', 'tests_units', 'total_vaccinations',
       'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
       'new_vaccinations_smoothed', 'total_vaccinations_per_hundred',
       'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred',
       'new_vaccinations_smoothed_per_million', 'stringency_index',
       'population', 'population_density', 'median_age', 'aged_65_older',
       'aged_70_older', 'gdp_per_capita', 'extreme_poverty',
       'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers',
       'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand',
       'life_expectancy', 'human_development_index']

# list of countries
country_list = list(df['location'].unique())


# organize data in month
group_list_month = group_list + [pd.Grouper(key="date", freq="M")]
df_country_monthly = df.groupby(group_list_month)[daily_characters].sum()
df_country_monthly[rate_characters] = df.groupby(group_list_month)[rate_characters].mean()
df_country_monthly.reset_index(inplace = True)
df_country_monthly['month_year'] = df_country_monthly['date'].dt.strftime('%Y-%m')
first_month = df_country_monthly['month_year'].min()
last_month = df_country_monthly['month_year'].max()

# print(df_country_monthly.head())



# Start the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    
    dbc.Row(dbc.Col(html.H1("Covid 19 visualization"),
                    #    width={'size': 6, 'offset': 3},
                        style={'color': '#002699', 'text-align': 'center', 'font-size': '18px', 'font-family':'verdana'},
                        ),
                ),

    dbc.Row(dbc.Col(
            html.Div('Updated date: {}'.format(df['date'].max())),
            style={'color': '#002699', 'text-align': 'center', 'font-size': '16px', 'font-family':'verdana'},
            ),
        ),

   
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id = 'world_map',
                        options =[{"label": name.capitalize().replace('_', ' '), "value": name} for name in daily_characters],
                        multi = False,
                        value = 'new_cases',
                        style = {'width': "100%"}
                            ),
            width = {'size': 2, "offset": 0, 'order': 1}                
            ),
        dbc.Col(
            dcc.Dropdown(id = 'start_month',
                        options =[
                            {"label": month, "value": month} for month in np.sort(df_country_monthly['month_year'].unique())],
                        multi = False,
                        value = first_month,
                        style = {'width': "100%"}
                            ),
            width = {'size': 1, "offset": 1, 'order': 2}                
            ),
        dbc.Col(
            dcc.Dropdown(id = 'end_month',
                        options =[                            
                            {"label": month, "value": month} for month in np.sort(df_country_monthly['month_year'].unique())],
                        multi = False,
                        value = last_month,
                        style = {'width': "100%"}
                            ),
            width = {'size': 1, "offset": 0, 'order': 3}                
            ),
            
        dbc.Col(
            dcc.Dropdown(id = 'country',
                        options = [{"label": label, "value": label} for label in country_list],
                        multi = True,
                        value = ["France", "Italy"],
                        style = {'width': "100%"}
                            ),
            width = {'size': 3, "offset": 0, 'order': 4}
            ), 
        dbc.Col(
            dcc.Dropdown(id = 'variable',
                        options = [{"label": cha.capitalize().replace('_', ' '), "value": cha} for cha in all_characters],
                        multi = True,
                        value = ["total_cases", "total_deaths"],
                        style = {"width": "100%"}
                            ),
            width = {"size": 4, "offset": 0, 'order': 5}            
            ),
        ]),
    
    
    html.Br(),



    dbc.Row([
        dbc.Col(html.Div([
            dcc.Graph(id='my_map', figure={}),
            dcc.Graph(id='world_chart', figure={})]
            ),
            width = {'size': 6, "offset": 0, 'order': 1}
                ),
        dbc.Col(html.Div(dcc.Graph(id='my_chart', figure={}, style = {'height' : '900px'})
            ), 
            width = {'size': 6, "offset": 0, 'order': 2}
            ),
        ]),   
    
    ])



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
    [Output(component_id = 'my_map', component_property='figure'),
    Output(component_id = 'world_chart', component_property='figure'),    
    Output(component_id='my_chart', component_property='figure'),
    ],
    [Input(component_id='world_map', component_property='value'),
    Input(component_id='country', component_property='value'),
    Input(component_id = 'variable', component_property = 'value'),
    Input(component_id = 'start_month', component_property = 'value'),
    Input(component_id = 'end_month', component_property = 'value')
    ]
)


def update_graph(option_case, option_country, option_variable, start_time, end_time):
    
    # world map with any chosen period.
    if option_case is None or start_time is None or end_time is None:
        raise PreventUpdate
    else:
        # prepare data for worl map
        dff = df_country_monthly.copy()
        dff = dff[(dff['date']>= pd.to_datetime(start_time)) & (dff['date']< pd.to_datetime(end_time))]
        dff0 = dff.groupby(group_list)[daily_characters].sum()
        dff0[rate_characters] = dff.groupby(group_list)[rate_characters].mean()
        dff0.reset_index(inplace = True)

        # World map.
        fig1 = px.choropleth(
            data_frame=dff0,
            locations='iso_code',
            scope='world',
            color=option_case,
            hover_name='location',
            color_continuous_scale=px.colors.sequential.YlOrRd
        )

        fig1.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=10, r=10, t=10, b=0))

        
    #Chart to compare chosen countries on certain properties.
    if len(option_country)==0 or len(option_variable)==0:
        raise PreventUpdate
    else:
        # prepare data for country level chart
        dff = df.copy()
        dff = dff[dff['location'].isin(list(option_country))]
    
        # Plotly chart
        col = len(option_variable)
        font = dict(size=24, family='verdana', color='#0052cc')
        # cmap = cm.get_cmap('tab20', 10)    # PiYG
        # colours = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]
        colours = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#c49c94','#f7b6d2','#c7c7c7','#dbdb8d','#9edae5']

        fig2 = make_subplots(rows=col, cols=1, shared_xaxes=False,
            subplot_titles=['{}'.format(var.capitalize().replace('_', ' ')) for var in option_variable])
        
        for i, var in enumerate(option_variable): 
            show_legend = False
            if i == 0:
                show_legend = True 
            for j, country in enumerate(option_country):
                fig2.add_trace(go.Scatter(x=dff[dff["location"]==country]["date"], y=dff[dff["location"]==country][var],
                    name = '{}'.format(country), showlegend = show_legend, line = dict(color = colours[j]),
                        ), 
                    row=i+1, col=1
                    )
        for i in fig2.layout.annotations:
            i["font"] = font
            
        
        fig2.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        fig2.update_layout(legend ={'x': 0, 'y': 1} )

        
    #  World chart for some main characters

    # prepare data.    
    dff = df.copy()
    dff = dff.groupby(['date'])[['total_cases', 'total_deaths', 'new_cases_smoothed', 'new_deaths_smoothed']].sum()
    dff.reset_index(inplace=True)

    # chart   
    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        x = dff["date"], y = dff["total_cases"],
        name="Total cases", line_color = "#1f77b4"
    ))


    fig3.add_trace(go.Scatter(
        x = dff["date"], y = dff["total_deaths"], name = " Total deaths",
        yaxis="y2", line_color = "#4633FF"
    ))

    fig3.add_trace(go.Scatter(
        x = dff["date"], y = dff["new_cases_smoothed"], name = "Daily cases",
        yaxis="y3", line_color = "#FFA533"
    ))

    fig3.add_trace(go.Scatter(
        x = dff["date"], y = dff["new_deaths_smoothed"], name = "Daily deaths",
        yaxis="y4", line_color = "#820A2F"
    ))

    fig3.update_layout(
        xaxis=dict(
        domain=[0.05, 0.9]
            ),
        yaxis=dict(
            title="Total cases",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="Total deaths",
            titlefont=dict(
                color="#4633FF"
            ),
            tickfont=dict(
                color="#4633FF"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0.025
        ),
        yaxis3=dict(
            title="Daily cases",
            titlefont=dict(
                color="#FFA533"
            ),
            tickfont=dict(
                color="#FFA533 "
            ),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        yaxis4=dict(
            title="Daily deaths",
            titlefont=dict(
                color="#820A2F"
            ),
            tickfont=dict(
                color="#820A2F"
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position=0.925
        )
    )

    fig3.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=1, r=1, t=5, b=5))
    fig3.update_layout(legend ={'x': 0.1, 'y': 1} )

    

    return fig1, fig3, fig2



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)








