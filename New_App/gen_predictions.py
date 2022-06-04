from Functions.GCP_Functions import *
from Functions.data_transformation import *
from datetime import datetime

def predictions(request=None):

    df = read_storage_files(bucket_name='data_injection_bucket', file_path=find_last_bucket_file(bucket_name='data_injection_bucket'))

    df = cities_filter(df, cidades = ['Paris', 'Sao Paulo', 'Carapicuiba', 'New York', 'Otawwa', 'London', 'Rome', 'Moscow'
                    , 'Hong Kong', 'Beijing'])

    df = tag_target(df, raining_list = ['Light rain', 'Light rain shower', 'Light drizzle', 'Heavy rain', 'Moderate rain'
            , 'Patchy light rain with thunder', 'Moderate or heavy rain shower', 'Patchy light rain', 'Torrential rain shower'
            , 'Moderate rain at times', 'Moderate or heavy rain with thunder'])

    df = df[['city', 'temp_c', 'is_day', 'condition', 'wind_kph', 'wind_degree'
                    , 'pressure_mb', 'precip_mm', 'humidity', 'cloud', 'feelslike_c', 'vis_km', 'uv'
                    , 'gust_kph', 'target']]

    model_pipe = read_storage_files('weather-ml-bucket', 'model/v1/Rain_Model_Object')

    df[['rain_prob', 'not_rain_prob']] = model_pipe.predict_proba(df)

    send_file_to_gcs('weather_prediction_files',
                    obj=df,
                    destination_blob_name=f'predictions/{datetime.now().strftime("%Y_%m_%d")}/weather_prediction_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.parquet')

if __name__ == '__main__':
    predictions()