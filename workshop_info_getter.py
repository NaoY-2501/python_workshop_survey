import csv
import json
import pickle

from collections import defaultdict

import requests

from tqdm import tqdm

URL = 'https://connpass.com/api/v1/event/'

MONTHS = [month for month in range(201801, 201813, 1)]


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


def main():
    workshop_info = get_workshop_info()
    with open('python_wokrshop_list.csv', 'w') as csvfile:
        dictwriter = csv.DictWriter(csvfile, fieldnames=['month', 'title', 'address', 'lat', 'lon'])
        for k, v in workshop_info.items():
            for event in v:
                row = {
                    'month': k,
                    'title': event['title'],
                    'address': event['address'],
                    'lat': event['lat'],
                    'lon': event['lon']
                }
                dictwriter.writerow(row)


if __name__ == '__main__':
    main()
