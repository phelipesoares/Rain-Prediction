# GCP Libraries

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud import storage
from datetime import datetime
import os
import pickle

try:
    bq_client = bigquery.Client()
except:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\Phelipe\Downloads\Weather Project-6fa8e059f642.json"
    bq_client = bigquery.Client()

storage_client = storage.Client(project=bq_client.project)

def get_table(bq_client: object == bq_client, query_string: str) -> pd.DataFrame:
    df = (
        bq_client.query(query_string)
        .result()
        .to_dataframe()
    )
    return df

def bq_send_data_f_listdict(listdict, table_id, bq_client: object = bq_client):
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
                errors = bq_client.insert_rows_json(table_id, rows_to_insert)
                input = []
                print(f'{table_id}: {errors}')
    return errors

def find_last_bucket_file(bucket_name, storage_client = storage_client):
    bucket = storage_client.get_bucket(bucket_name)
    all_blobs = list(storage_client.list_blobs(bucket))
    last_file_name = all_blobs[-1].name
    return last_file_name

def read_storage_files(bucket_name, file_path, storage_client=storage_client):
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_path)
    obj = blob.download_as_string()
    return pickle.loads(obj)

def upload_blob(bucket_name, source_file_name, destination_blob_name, storage_client=storage_client):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )