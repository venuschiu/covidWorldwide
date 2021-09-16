import data_init

# pip3 install dash
import dash 
from dash import html
from dash.dependencies import Output
import pandas as pd
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


# App layout
app.layout = html.Div( [

    html.H1("My first dash app"),
    html.Div(id = 'output_container', children= []),
    html.Br(),
    dss.Graph(id = 'my_covid_map', figure = {})

]

)

# connect the plot with dash component
@app.callback(
 Output(component_id = 'output_container', component_property = 'children')
)

def get_graph():
    

if __name__ == '__main__':
    app.run_server(debug = True)
