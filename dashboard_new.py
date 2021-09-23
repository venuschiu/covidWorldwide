import data_prep

# pip3 install dash
import dash 
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime as dt

app = dash.Dash(__name__)

# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"


list_of_locations = data_prep.latest['country'].unique()
print(data_prep.values)
print(data_prep.ticks)


# App layout
# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H1("COVID WORLDWIDE"),
                        html.P(
                            """Select different days using the date picker or by selecting
                            different country."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2021, 9, 1),
                                    max_date_allowed=dt(2021, 9, 30),
                                    initial_visible_month=dt(2021, 9, 15),
                                    date=dt(2021, 9, 10).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_locations
                                            ],
                                            placeholder="Select a location",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            """
                            Source: [data.gov.hk](https://data.gov.hk/en-data/dataset/hk-dh-chpsebcddr-novel-infectious-agent/resource/8b5a8f82-94f6-427d-9a2f-3567d65ca79b)
                            Links: [Source Code](https://github.com/venuschiu/covidWorldwide) 
                            """
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                        ),
                        dcc.Graph(id="line_plot"),
                    ],
                ),
            ],
        )
    ]
)


# connect the plot with dash component

# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    Input("date-picker", "date")
)
def get_graph(selected_date):
    
    map_data = data_prep.latest.copy()
    map_result = map_data.loc[map_data['as_of_date'] == selected_date]

# https://plotly.com/python-api-reference/generated/plotly.express.choropleth
# https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-uber-rides-demo
    px.set_mapbox_access_token(mapbox_access_token)
    fig = px.choropleth_mapbox(
        data_frame=map_result,
        geojson=data_prep.geo_world_ok,
        locations='country',        
        color=map_result['confirmed_case_color'],
        color_continuous_scale=px.colors.sequential.Rainbow,
        range_color = (0, map_result['confirmed_case_color'].max()),
        hover_name = 'country',
        hover_data={'confirmed_case_color': False, 'country': False, 'confirmed_case': True},
        mapbox_style = 'stamen-toner',
        # mapbox_style = 'open-street-map',
        zoom = 1,
        center = {'lat': 19, 'lon': 11},
        opacity=0.5
    ); 
  
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      autosize=True,
                       coloraxis_colorbar = {
                           'title': 'Confirmed people' ,
                           'tickvals' : data_prep.values,
                           'ticktext': data_prep.ticks                          


                       } 
    
    )
    return fig


@app.callback(
    Output("line_plot", "figure"),
    Input("location-dropdown", "value")
)
def update_plot(selected_country):
    
    print(selected_country)
    map_data = data_prep.latest.copy()
    map_result = map_data
    if selected_country is not None:
        map_result = map_data.loc[map_data['country'] == selected_country]
    
    print(map_result)
    fig = px.line(map_result, 
        x="as_of_date", y="confirmed_case", color='country', markers = True)

    return fig

if __name__ == '__main__':
    app.run_server(debug = True)
