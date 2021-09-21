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



list_of_locations = data_prep.latest['country'].unique()
print(list_of_locations)


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
                        html.A(
                            html.Img(
                                className="logo",
                                src=app.get_asset_url("dash-logo-new.png"),
                            ),
                            href="https://plotly.com/dash/",
                        ),
                        html.H2("COVID WORLDWIDE"),
                        html.P(
                            """Select different days using the date picker or by selecting
                            different countries."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2021, 9, 10),
                                    max_date_allowed=dt(2021, 9, 15),
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
                            Source: [FiveThirtyEight](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data)
                            Links: [Source Code](https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-uber-rides-demo) | [Enterprise Demo](https://plotly.com/get-demo/)
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
                            children=[
                                "Select any of the bars on the histogram to section data by time."
                            ],
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
        zoom = 1,
        center = {'lat': 19, 'lon': 11},
        opacity=0.5
    ); 
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
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
    map_result = map_data.loc[map_data['country'] == selected_country]
    print(map_result)
    fig = px.line(map_result, 
        x="as_of_date", y="confirmed_case", color='country')

    return fig

if __name__ == '__main__':
    app.run_server(debug = True)
