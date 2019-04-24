import os

import folium
import pandas as pd

geo = os.path.join('data', 'japan.geojson')

py_workshop = os.path.join('data', 'python_workshop_list.csv')

base_df = pd.read_csv(py_workshop)
base_df.dropna(subset=['prefecture'], inplace=True)
grouped  = base_df.groupby('prefecture')

pref_count = grouped.count().reset_index()

tokyo_idx = pref_count[pref_count['prefecture'] == '東京都'].index[0]
pref_count.drop([tokyo_idx], inplace=True)

all = pref_count['month'].sum()

pref_count['tmp'] = pref_count['month'].astype('int64')
pref_count['rate'] = pref_count['tmp'].apply(lambda x: (x/all)*100)
pref_count.drop(['month', 'title', 'address', 'lat', 'lon', 'tmp'], inplace=True, axis=1)


bins = list(pref_count['rate'].quantile([0, 0.25, 0.5, 0.75, 1]))
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
    bins=bins,
    legend_name='開催数(%)'
).add_to(m)

m.save('docs/python_workshop_choropleth.html')
