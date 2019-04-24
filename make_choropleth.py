import os

import folium
import pandas as pd

geo = os.path.join('data', 'japan.geojson')

py_workshop = os.path.join('data', 'python_workshop_list.csv')

base_df = pd.read_csv(py_workshop)
base_df.dropna(subset=['prefecture'], inplace=True)
grouped  = base_df.groupby('prefecture')

pref_count = grouped.count().reset_index()

all = len(pref_count)

pref_count['rate'] = pref_count['month'].astype('int64')
# pref_count['rate'] = pref_count['rate'].apply(lambda x: x/all)
pref_count.drop(['month', 'title', 'address', 'lat', 'lon'], inplace=True, axis=1)

print(pref_count.head())

m = folium.Map(location=[35, 135], zoom_start=5)

folium.Choropleth(
    geo_data=geo,
    name='choropleth',
    data=pref_count,
    columns=['prefecture', 'rate'],
    key_on='feature.properties.nam_ja',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.7,
    legend_name='開催数'
).add_to(m)

m.save('data/python_workshop_choropleth.html')
