import numpy as np
import requests
import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO,StringIO
import io
import uuid
import json
import boto3
import pandas as pd
import pyarrow.parquet as pq
import botocore
import toml
from NimbusStorage import NimbusCloudStorage

data = open('NimbusSetting.json').read()
Nimbus_settings = json.loads(data)
NIMBUS_BASE_SETTINGS = Nimbus_settings["Base"]
STORAGE_PROVIDER = NIMBUS_BASE_SETTINGS['STORAGE_PROVIDER']

store = NimbusCloudStorage(provider =STORAGE_PROVIDER)

with open('.streamlit/config.toml', 'r') as f:
    config = toml.load(f)
 
bucket_name = config['aws']['bucket_name']
directory = config['aws']['directory']
file_key = config['aws']['file_key']
 
s3 = boto3.client('s3')

def download_file_from_s3(bucket_name, file_key):
    try:
        response = store.read_object(container_name=bucket_name, key=file_key)
        return response
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"The object '{file_key}' does not exist in the bucket '{bucket_name}'.")
        else:
            raise
file_contents = download_file_from_s3(bucket_name, file_key)


def fetch_data_from_parquet(bucket_name, file_key):
    try:
        response = store.read_object(container_name=bucket_name, key=file_key)
        table = pq.read_table(BytesIO(response))
        df = table.to_pandas()
        return df
    except Exception as e:
        print("Error:", e)
        return None


def fetch_data_from_parquet_files(bucket_name, directory):
    try:
        tables_data = {}
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=directory)
        if 'Contents' in response:
            for obj in response['Contents']:
                file_key = obj['Key']
                if file_key.endswith('.parquet'):
                    table_name = file_key.split('/')[-1].replace('.parquet', '')
                    table_data = fetch_data_from_parquet(bucket_name, file_key)
                    if table_data is not None:
                        tables_data[table_name] = table_data
        else:
            print("No Parquet files found in the specified directory.")
        return tables_data
    except Exception as e:
        print("Error:", e)
        return None
    

tables = fetch_data_from_parquet_files(bucket_name, directory)