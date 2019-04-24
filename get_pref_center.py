import pandas as pd

url = 'https://kariruno.com/center-todoufuken/'

dfs = pd.read_html(url)

df = dfs[0]

df.replace({
    '都道府県': 'prefecture',
    '経度': 'lat',
    '緯度': 'lon'
}, inplace=True)

df.to_csv('data/pref_center.csv', index=False, header=False)
