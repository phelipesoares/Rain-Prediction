import requests
import time
from datetime import datetime
import pandas as pd

dt_metadata = datetime.now().replace(microsecond = 0)
dt_file = str(dt_metadata).replace(" ", "_").replace(":", "_").replace("-", "_")

def read_api_credentials(path):
    f = open(path, "r")
    info_list = eval(f.read())

    # Weather-info-table
    for x in info_list[1]:
        table_id = x

    # api url
    for x in info_list[3]:
        url = x

    # Headers api
    headers = info_list[0]
    return table_id, url, headers

def get_api_data(url, headers):
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
    return listdict

def create_metadata(listdict, dt = dt_metadata):
    df = pd.DataFrame(listdict)
    df['ingestion_date'] = pd.to_datetime(dt)
    return df

def save_api_file(df: pd.DataFrame, dt = dt_file):
    df.to_parquet(f"Files/{dt}_weather_api.parquet")