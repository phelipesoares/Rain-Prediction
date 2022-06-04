#!/usr/bin/env python
# coding: utf-8

# In[1]:

from Functions.GCP_Functions import *
from Functions.data_transformation import *
from Functions.model_training import *

# In[2]:

def train_pipeline(request=None):

    df = get_table(query_string = """
      SELECT *
      FROM (SELECT *
                  , ROW_NUMBER() OVER(PARTITION BY last_updated, city ORDER BY last_updated, city) AS row_num
                  FROM `weather-project-305419.Daily_Weather.Weather-Info`) as row_weather
      WHERE row_num = 1
      """)

    df = cities_filter(df, cidades = ['Paris', 'Sao Paulo', 'Carapicuiba', 'New York', 'Otawwa', 'London', 'Rome', 'Moscow'
              , 'Hong Kong', 'Beijing'])

    df = tag_target(df, raining_list = ['Light rain', 'Light rain shower', 'Light drizzle', 'Heavy rain', 'Moderate rain'
      , 'Patchy light rain with thunder', 'Moderate or heavy rain shower', 'Patchy light rain', 'Torrential rain shower'
      , 'Moderate rain at times', 'Moderate or heavy rain with thunder'])

    df = to_float(df)

    df = date_diff_calc(df)

    df = rain_next1(df)

    # Choose Variables
    df = df[['city', 'temp_c', 'is_day', 'condition', 'wind_kph', 'wind_degree'
              , 'pressure_mb', 'precip_mm', 'humidity', 'cloud', 'feelslike_c', 'vis_km', 'uv'
              , 'gust_kph', 'target', 'target_1']]

    x, y = split_x_y(df)

    model_pipe = training_pipe(x, y)

    send_file_to_gcs(bucket_name='weather-ml-bucket',
                     obj=pickle.dumps(model_pipe),
                     destination_blob_name=f'model/v1/{datetime.now().strftime("%Y_%m")}/Rain_Model_Object_{datetime.now().strftime("%Y_%m_%d")}')

    return print("Done!")

if __name__ == '__main__':
    train_pipeline()
# %%