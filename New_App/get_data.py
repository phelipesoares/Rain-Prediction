#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Functions.GCP_Functions import *
from Functions.weather_api import *

# In[2]:

def get_data(request=None):
    table_id, url, headers = read_api_credentials(path="Credentials/project_info.txt")  
    listdict = get_api_data(url, headers)
    df = create_metadata(listdict)
    send_file_to_gcs(bucket_name="data_injection_bucket", df=df, destination_blob_name=f"weather_api_files/{dt_file[:10]}/{dt_file}_weather_api.parquet")
    bq_send_data_f_listdict(listdict, table_id)
    return print('Done!')

if __name__ == '__main__':
    get_data()