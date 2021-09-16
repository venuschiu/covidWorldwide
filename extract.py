import requests
import json
import urllib.parse
import pandas as pd
from configparser import ConfigParser
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text, Table, MetaData, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import Column 
import seaborn as sns
import matplotlib.pyplot as plt

api = "https://api.data.gov.hk/v2/filter?q="

params2 = '{"resource":"http://www.chp.gov.hk/files/misc/countries_areas_have_reported_cases_eng.csv", \
            "section":1,"format":"json","filters":[ [1,"eq",["09/09/2021"]]  ]}'

# read the read teh params in the config files
configure = ConfigParser()
print (configure.read('config.ini'))
print ("Sections : ", configure.sections())
print ("api params : ", configure.get('api_params','resource'))
print ("api params : ", configure.get('api_params','section'))
print ("api params : ", configure.get('api_params','format'))
print ("api params : ", configure.get('api_params','date_col_index'))
print ("api params : ", configure.get('api_params','date_col_filter'))

params_dic = {}
params_dic['resource'] = configure.get('api_params','resource')
params_dic['section'] = configure.get('api_params','section')
params_dic['format'] = configure.get('api_params','format')


filter_list = []
filter_date_col = []
filter_date_col.append(configure.get('api_params','date_col_index')) 
filter_date_col.append(configure.get('api_params','date_col_filter')) 
filter_date_col.append([ (datetime.now()- timedelta( days= int(configure.get('api_params', 'date_col_time_delta') )))\
                .strftime("%d/%m/%Y") ]) 
filter_list.append(filter_date_col)

params_dic['filters'] = filter_list 


""" 
params_dic = {}
params_dic['resource'] = 'http://www.chp.gov.hk/files/misc/countries_areas_have_reported_cases_eng.csv'
params_dic['section'] = 1
params_dic['format'] = 'json'


filter_list = []
filter_date_col = []
filter_date_col.append(1) 
filter_date_col.append('eq') 
filter_date_col.append(["09/09/2021"]) 
filter_list.append(filter_date_col)

print(filter_list)

params_dic['filters'] = filter_list 
"""

json_param = json.dumps(params_dic)
print(json_param)

url = api + urllib.parse.quote_plus(json_param)
#print(urllib.parse.quote_plus(params2))
print(url)


json_data = requests.get(url).json()
# print(json_data)
# print(json_data)


with open('data/data.json', 'w') as f:
    json.dump(json_data, f)

print(json_data[1]['Countries/areas'])

print(type(json_data))
print(len(json_data))


json_list = pd.read_json('data/data.json')
print(json_list.head(5))
print(type(json_list))

""" for i, row in json_list.iterrows():
    print(row) """



# test the db connections
engine = create_engine(configure.get('database_connections', 'database_conn_uri'), echo=True)

# just to test the connections
result = engine.execute(
    text(
        "SELECT id   \
        from covid.persons;"
    )
)

print(result)
print(f"Selected {result.rowcount} rows.")
for row in result.fetchall():
    print(row)

Base = declarative_base()


metadata = MetaData(engine,schema="covid")
metadata.reflect()
print(metadata.tables)
  
class persons(Base):
    __table__ = Table(
        'persons',
        metadata,
        autoload_with=engine
    )

class persons_nopk(Base):
    __table__ = Table(
        "persons_nopk",
        metadata,
        Column("ID", Integer, primary_key=True),      
        extend_existing=True
    )

Session = sessionmaker(bind=engine)
session = Session()
res = session.query(persons).all()
print(type(res))
for x in range(len(res)):
    print(res[x].ID)
    print(res[x].LastName)
    print(res[x].FirstName)

res = session.query(persons_nopk).all()
print(type(res))
for x in range(len(res)):
    print(res[x].ID)
    print(res[x].LastName)
    print(res[x].FirstName)
    
""" 
new_person = persons(
    ID = 5555,
    LastName = 'superman',
    FirstName = 'kksuperman'
)

session.add(new_person)
session.commit()
"""
vv = session.query(persons).filter(persons.ID == 1234).first()
print(vv.ID)
vv.FirstName = 'vv changed name'
session.commit()

# data initialization
for x in range(1, 5):
    print(x)
    print((datetime.now() - timedelta(days =  x)).strftime("%d/%m/%Y"))


df = pd.read_sql("select * from covid.persons", engine)
print(df.head())

x = df['LastName']
y = df['Age']

sns.barplot(x = x, y =y)
plt.show()
