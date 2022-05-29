#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Functions.GCP_Functions import *
from Functions.data_transformation import *
from Functions.model_training import *


# In[2]:

def main():

    df = get_table(query_string = """
      SELECT *
      FROM (SELECT *
                  , ROW_NUMBER() OVER(PARTITION BY last_updated, city ORDER BY last_updated, city) AS row_num
                  FROM `weather-project-305419.Daily_Weather.Weather-Info`) as row_weather
      WHERE row_num = 1
      """, bq_client=bq_client)

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

    model_pipe, preprocessor = training_pipe(x, y)

    save_object(model_pipe, 'Rain_Model_Object')

    upload_blob(bucket_name='weather-ml-bucket',
                source_file_name='Rain_Model_Object',
                destination_blob_name='model/Rain_Model_Object')

if __name__ == '__main__':
    main()