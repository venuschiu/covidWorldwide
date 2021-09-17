import data_init

# pip3 install dash
import dash 
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

# ------------------ Get the data -----------
# print(data_init.final_result.head())
data_init.final_result["As of date"] = pd.to_datetime(data_init.final_result["As of date"], format='%d/%m/%Y')

# print(data_init.final_result.groupby("As of date")["As of date"].count())
# print(data_init.Dtypes)
""" print(data_init.final_result.groupby(["As of date", "Countries/areas"]) \
                                    ["As of date", "Countries/areas", "Cumulative number of confirmed cases"].sum()\
                                        )
 """
""" y = data_init.final_result.groupby(["As of date", "Countries/areas"]) \
                                    ["As of date", "Countries/areas", "Cumulative number of confirmed cases"].sum()
 """""" print(y)
y = y.reset_index()
print(y)
 """

""" y = y.reset_index()
print(y["As of date"] .max())
print(y.loc[ y["As of date"] == y["As of date"] .max() ] .groupby(["As of date", "Countries/areas"], as_index = False) \
                                    [["As of date", "Countries/areas", "Cumulative number of confirmed cases"]].sum())
 """
latest = data_init.final_result.loc[ data_init.final_result["As of date"] == data_init.final_result["As of date"] .max() ] \
                                    .groupby(["As of date", "Countries/areas"], as_index = False) \
                                    [["As of date", "Countries/areas", "Cumulative number of confirmed cases"]].sum()

""" print(
    (data_init.final_result.nlargest(1, "As of date").groupby(["As of date", "Countries/areas"]) \
                                    ["As of date", "Countries/areas", "Cumulative number of confirmed cases"].sum())
)
x = (data_init.final_result.nlargest(1, "As of date").groupby(["As of date", "Countries/areas"]) \
                                    ["As of date", "Countries/areas", "Cumulative number of confirmed cases"].sum())

print(x.reset_index())
print(x) """


print(latest.head(5))






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
    
    map_data = latest.copy()

# https://plotly.com/python-api-reference/generated/plotly.express.choropleth
    container = "Latest worldwide COVID case provided by data.gov.hk "
    fig = px.choropleth(
        data_frame=map_data,
        locationmode='country names',
        locations='Countries/areas',
        scope="world",
        color='Cumulative number of confirmed cases',
        hover_data=['Countries/areas', 'Cumulative number of confirmed cases'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    ); 
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return container, fig
if __name__ == '__main__':
    app.run_server(debug = True)
