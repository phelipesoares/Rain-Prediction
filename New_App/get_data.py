#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Functions.GCP_Functions import *
from Functions.weather_api import *
from Functions.model_training import save_model


# In[2]:


table_id, url, headers = read_api_credentials(path=r"C:\Users\Phelipe\Documents\GitHub\Rain-Prediction\App\Credentials\project_info.txt")
listdict = get_api_data(url, headers)
client, project_id, credentials = gcp_credentials(path=r"C:\Users\Phelipe\Documents\GitHub\Rain-Prediction\App\Credentials\Weather Project-6fa8e059f642.json")
errors = bq_send_data_f_listdict(listdict, table_id, client)

save_object(listdict, 'api_last_batch')

upload_blob(bucket_name='weather-ml-bucket',
            source_file_name='api_last_batch',
            destination_blob_name='data_files/api_last_batch')