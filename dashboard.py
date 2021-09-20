import data_prep

# pip3 install dash
import dash 
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)







# App layout
app.layout = html.Div( [

    html.H1("My first dash app"),
    html.Div(id = 'output_container', children= []),
        dcc.Dropdown(id="select_date",
                 options=[
                     {"label": "2021-09-15", "value": '2021-09-15'},
                     {"label": "2021-09-14", "value": '2021-09-14'},
                     {"label": "2021-09-13", "value": '2021-09-13'},
                     {"label": "2021-09-12", "value": '2021-09-12'},
                     {"label": "2021-09-11", "value": '2021-09-11'}],
                 multi=False,
                 value='2021-09-15',
                 style={'width': "40%"}
                 ),
    html.Br(),
    dcc.Graph(id = 'my_covid_map', figure = {})

]

)

# connect the plot with dash component

@app.callback(
 [Output(component_id = 'output_container', component_property = 'children'),
 Output(component_id = 'my_covid_map', component_property = 'figure'),],
 [Input(component_id='select_date', component_property='value')]
) 


def get_graph(date_value):
    
    map_data = data_prep.latest.copy()

# https://plotly.com/python-api-reference/generated/plotly.express.choropleth
    container = "Latest worldwide COVID case provided by data.gov.hk "
    fig = px.choropleth(
        data_frame=map_data,
        geojson=data_prep.geo_world_ok,
        locations='country',
        
        color=map_data['confirmed_case_color'],
        #hover_data=['Countries/areas', 'Cumulative number of confirmed cases'],
        #color_continuous_scale=px.colors.sequential.YlOrRd,
        range_color = (0, map_data['confirmed_case_color'].max())
        
    ); 
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                       coloraxis_colorbar = {
                           'title': 'Confirmed people' ,
                           'tickvals' : data_prep.values,
                           'ticktext': data_prep.ticks



                       } 
    
    )

    return container, fig
if __name__ == '__main__':
    app.run_server(debug = True)
