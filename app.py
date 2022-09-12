import dash
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'Covid-19 Vaccinations'
sourceurl = 'https://www.kaggle.com/datasets/paultimothymooney/usa-covid19-vaccinations'
githublink = 'https://github.com/wangweiching/306-agriculture-exports-dropdown.git'
# here's the list of possible columns to choose from.
list_of_columns =['total_vaccinations','total_distributed','people_vaccinated']
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
# df = pd.DataFrame(us_state_to_abbrev, columns = ["location", "last_name", "age",
#                                            "Comedy_Score", "Rating_Score"])



########## Set up the chart

df = pd.read_csv('assets/us_state_vaccinations.csv')
df['Code'] = df['location'].map(us_state_to_abbrev)
# print(df['total_vaccinations'].value_counts().describe())
# print(df['total_distributed'].value_counts().describe())
# print(df['people_vaccinated'].value_counts().describe())
########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('2021 Covid-19 Vaccinations Stats, by State'),
    html.Div([
        html.Div([
                html.H6('Select a variable for analysis:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='total_vaccinations'
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mycolorbartitle = f'Number of {varname}'
    mygraphtitle = f'Covid-19 stats for {varname} in 2021'
    #mycolorscale = 'Teal' # Note: The error message will list possible color scales.

    colorscale = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                  "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                  "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                  "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                  "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                  "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                  "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                  "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                  "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"]

    values = df[varname].tolist()
    grouped_mean = df.groupby(varname).mean()
    data=go.Choropleth(
        locations=df['Code'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        #values = values, # Data to be color-coded
        z=df[varname].astype(float),
        colorscale = colorscale,
        marker_line_color='white',
        autocolorscale=False,
        colorbar_title = mycolorbartitle,
    )
    fig = go.Figure(data)
    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)