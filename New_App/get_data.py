#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Functions.GCP_Functions import *
from Functions.weather_api import *

# In[2]:

def main():
    table_id, url, headers = read_api_credentials(path="Credentials/project_info.txt")
    listdict = get_api_data(url, headers)
    df = create_metadata(listdict)
    save_api_file(df)
    upload_blob(bucket_name="data_injection_bucket", source_file_name=f"Files/{dt_file}_weather_api.parquet", destination_blob_name=f"weather_api_files/{dt_file}_weather_api")
    bq_send_data_f_listdict(listdict, table_id)

    #upload_blob(bucket_name='weather-ml-bucket',
     #           source_file_name='api_last_batch',
      #          destination_blob_name='data_files/api_last_batch')

if __name__ == '__main__':
    main()