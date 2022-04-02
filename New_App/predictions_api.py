#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Functions.GCP_Functions import *
from Functions.data_transformation import *
from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
import json


# In[ ]:


app = Flask(__name__)
api = Api(app)

class Weather_Prediction(Resource):
    def get(self):
        
        client, project_id, credentials = gcp_credentials(path = r"C:\Users\Phelipe\Documents\GitHub\Rain-Prediction\App\Credentials\Weather Project-6fa8e059f642.json")

        model_pipe = read_storage_files('weather-ml-bucket', 'model/Rain_Model_Object', project_id)

        last_batch = read_storage_files('weather-ml-bucket', 'data_files/api_last_batch', project_id)

        df = pd.DataFrame(last_batch)

        df = cities_filter(df, cidades = ['Paris', 'Sao Paulo', 'Carapicuiba', 'New York', 'Otawwa', 'London', 'Rome', 'Moscow'
                  , 'Hong Kong', 'Beijing'])

        df = tag_target(df, raining_list = ['Light rain', 'Light rain shower', 'Light drizzle', 'Heavy rain', 'Moderate rain'
          , 'Patchy light rain with thunder', 'Moderate or heavy rain shower', 'Patchy light rain', 'Torrential rain shower'
          , 'Moderate rain at times', 'Moderate or heavy rain with thunder'])

        df = df[['city', 'temp_c', 'is_day', 'condition', 'wind_kph', 'wind_degree'
                  , 'pressure_mb', 'precip_mm', 'humidity', 'cloud', 'feelslike_c', 'vis_km', 'uv'
                  , 'gust_kph', 'target']]

        df[['rain_prob', 'not_rain_prob']] = model_pipe.predict(df)
        
        predictions = json.dumps(df.values.tolist())
              # return our data and 200 OK HTTP code
        return {'predictions': predictions}, 200

api.add_resource(Weather_Prediction, '/predictions')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

