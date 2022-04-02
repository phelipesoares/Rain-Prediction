import requests
import time

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
