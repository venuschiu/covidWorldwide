import data_init
import pandas as pd
import json
import numpy as np
# ------------------ Get the data -----------
# print(data_init.final_result.head())
data_init.final_result["As of date"] = pd.to_datetime(data_init.final_result["As of date"], format='%d/%m/%Y')

""" latest = data_init.final_result.loc[ data_init.final_result["As of date"] == data_init.final_result["As of date"] .max() ] \
                                    .groupby(["As of date", "Countries/areas"], as_index = False) \
                                    [["As of date", "Countries/areas", "Cumulative number of confirmed cases"]].sum() """


latest = data_init.final_result.groupby(["As of date", "Countries/areas"], as_index = False) \
                                        [["As of date", "Countries/areas", "Cumulative number of confirmed cases"]].sum()


# rename columns
latest = latest.rename(columns = {"As of date": 'as_of_date', 'Countries/areas': 'country', 'Cumulative number of confirmed cases': 'confirmed_case'})

print(latest.head(5))

print(latest.groupby(['as_of_date'])['as_of_date'].count())
print(latest.loc[latest['country'] == 'Afghanistan'])

# prepare the geo json data
world_geo_path = 'custom.geo.json'

with open(world_geo_path) as f:
    geo_world = json.load(f)


# set the country column to be the index
tmp = latest.set_index('country')

found = []
missing = []
countries_geo = []

country_conversion_dict = {
    'Bosnia and Herz.': 'Bosnia and Herzegovina',
    'Central African Rep.': 'Central African Republic',
    "Côte d'Ivoire": "C\u00f4te d\u2019Ivoire",
    'Czech Rep.' :  'Czech Republic',
    'Dem. Rep. Congo': 'Congo',
    'Dominican Rep.':'Dominican Republic',
    'Eq. Guinea':'Equatorial Guinea',
    'Korea': 'Korea',
    'Lao PDR':'Laos',
    'Myanmar':'Burma',
    'S. Sudan':'South Sudan',
    'Somaliland':'Somalia',
    'United States' : 'United States of America',
    'China' :'Mainland China',
    'Vietnam': 'Viet Nam',
    'Venezuela': 'Venezuela (Bolivarian Republic of)',
    'Brunei':'Brunei Darussalam',
    'Syria': 'Syrian Arab Republic',
    'Moldova': 'Republic of Moldova',
    'Tanzania':'United Republic of Tanzania'
}

for c in geo_world['features']:
    world_geo_country = c['properties']['name']

    world_geo_country = country_conversion_dict[world_geo_country] if world_geo_country in country_conversion_dict.keys() else world_geo_country
    
    if world_geo_country in tmp.index:
        # add country to the found list
        found.append(c)

        country_geometry = c['geometry']

        countries_geo.append({
            'type': 'Feature',
            'geometry': country_geometry,
            'id': world_geo_country

        })
    else:
        missing.append(world_geo_country)


print(f'Countries found: {len(found)}')
print(f'Countries not found: {len(missing)}')
print(missing)
geo_world_ok= {'type': 'FeatureCollection', 'features': countries_geo}


# the data set has values in a wide range, 
# so indead of using th linear scalre, we will logarithm it
latest['confirmed_case_color'] = latest['confirmed_case'].apply(np.log10)

print(latest.head(5))
print(latest.size)


# get the maximum value to cap display values
max_log = latest['confirmed_case_color'].max()
print(max_log)
max_val = int(max_log) + 1
print(max_val)

#prepare the range of the color bar
values = [i for i in range(max_val)]
ticks = [10**i for i in values]
