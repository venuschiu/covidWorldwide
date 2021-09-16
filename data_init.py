import utilities
from datetime import datetime, timedelta
import requests
import json
import pandas as pd

file_list = []
dfs = []
for x in range(1, 5):
    print(x)
    print((datetime.now() - timedelta(days =  x)).strftime("%d/%m/%Y"))
    date_value = (datetime.now() - timedelta(days =  x))
    print(utilities.get_api_url(date_filter = 'eq', date_value = date_value))
    api_url = utilities.get_api_url(date_filter = 'eq', date_value = date_value)
    json_data = requests.get(api_url).json()
    file_name = f'data/data_{date_value.strftime("%Y%m%d")}.json'
    file_list.append(file_name)
    
    with open(file_name, 'w') as f:
        json.dump(json_data, f) 
for file in file_list:
    print(file)
    result = pd.read_json(file)    
    dfs.append(result)

print(len(dfs))

final_result = pd.concat(dfs, ignore_index=True)

print(f"size: {final_result.size}")
print(final_result.head())
print(final_result.groupby("As of date")["As of date"].size())
print(final_result.groupby("As of date")["As of date"].count())


    