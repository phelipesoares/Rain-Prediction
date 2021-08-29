#!/usr/bin/env python
# coding: utf-8

# In[134]:

### Take the data from API

import requests
import time
from datetime import datetime

f = open("project_info.txt", "r")
info_list = eval(f.read())

for x in info_list[1]:
    table_id = x
    
for x in info_list[2]:
    path = x
    
for x in info_list[3]:
    url = x
    
headers = info_list[0]

cities = list(("Sao Paulo", "Carapicuiba", "New York", "Paris", "London", "Rome", "Moscow", "Ottawa", "Hong Kong", "Beijing"))
listdict = list(())
for i in cities:
    querystring = {"q":"{}".format(i)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    var = response.json()
    dic = var['current']
    dic['condition'] = dic['condition']['text']
    dic['city'] = "{}".format(i)
    listdict.append(dic)
    time.sleep(1)
    
from google.cloud import bigquery
from google.oauth2 import service_account

project_id = 'weather-project-305419'
client = bigquery.Client(project=project_id)
print(f'list:{listdict}')

input = []
for x in listdict:
    for i in x.values():
        input.append(i)
        if len(input) < 24:
            pass
        else:
            rows_to_insert = [
            {
            u"last_updated_epoch": u"{}".format(input[0]), 
            u"last_updated": u"{}".format(input[1]),
            u"temp_c": u"{}".format(input[2]),
            u"temp_f": u"{}".format(input[3]),
            u"is_day": u"{}".format(input[4]),
            u"condition": u"{}".format(input[5]),
            u"wind_mph": u"{}".format(input[6]),
            u"wind_kph": u"{}".format(input[7]),
            u"wind_degree": u"{}".format(input[8]),
            u"wind_dir": u"{}".format(input[9]),
            u"pressure_mb": u"{}".format(input[10]),
            u"pressure_in": u"{}".format(input[11]),
            u"precip_mm": u"{}".format(input[12]),
            u"precip_in": u"{}".format(input[13]),
            u"humidity": u"{}".format(input[14]),
            u"cloud": u"{}".format(input[15]),
            u"feelslike_c": u"{}".format(input[16]),
            u"feelslike_f": u"{}".format(input[17]),
            u"vis_km": u"{}".format(input[18]),
            u"vis_miles": u"{}".format(input[19]),
            u"uv": u"{}".format(input[20]),
            u"gust_mph": u"{}".format(input[21]),
            u"gust_kph": u"{}".format(input[22]),
            u"city": u"{}".format(input[23]),
            u"extraction_date": u"{}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            },
            ]
            errors = client.insert_rows_json(table_id, rows_to_insert)
            input = []
time.sleep(480)
