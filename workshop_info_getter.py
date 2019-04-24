import csv
import json
import pickle
import re

from collections import defaultdict

import requests

from tqdm import tqdm
from shapely.geometry import shape, Point

URL = 'https://connpass.com/api/v1/event/'

MONTHS = [month for month in range(201801, 201813, 1)]

PREF_P = re.compile(r'\w{2,3}[都道府県]')


def exec_api(month, start=1):
    params = {
        'keyword': 'Python',
        'count': 100,
        'ym': str(month),
        'start': start
    }
    res = requests.get(URL, params=params)
    return res.json()


def get_workshop_info():
    workshop_info = {}
    for month in tqdm(MONTHS):
        res = exec_api(month)
        workshop_info[month] = res['events']
        results_available =  res['results_available']
        if results_available > 100:
            starts = [count for count in range(101, results_available, 100)]
            for start in starts:
                res = exec_api(month, start)
                workshop_info[month].extend(res['events'])
    return workshop_info


def parse_pref(lat, lon, address, geo_json):
    # refs. https://qiita.com/jagio/items/bdccc28d1b3c56233931
    if lat and lon:
        point = Point(float(lon), float(lat))
        for feature in geo_json['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return feature['properties']['nam_ja'] # 市区町村名へアクセス
    if address:
        m = PREF_P.search(address)
        if m:
            return m[0]
    return None


def main():
    with open('data/japan.geojson') as f:
        # 出典元: 地球地図日本 (http://www.gsi.go.jp/kankyochiri/gm_jpn.html)
        geo_json = json.load(f)
    workshop_info = get_workshop_info()
    with open('data/python_workshop_list.csv', 'w') as csvfile:
        dictwriter = csv.DictWriter(csvfile, fieldnames=['month', 'title', 'prefecture', 'address', 'lat', 'lon'])
        dictwriter.writeheader()
        for k, v in workshop_info.items():
            for event in v:
                row = {
                    'month': k,
                    'title': event['title'],
                    'prefecture': parse_pref(event['lat'], event['lon'], event['address'], geo_json),
                    'address': event['address'],
                    'lat': event['lat'],
                    'lon': event['lon']
                }
                dictwriter.writerow(row)


if __name__ == '__main__':
    main()
