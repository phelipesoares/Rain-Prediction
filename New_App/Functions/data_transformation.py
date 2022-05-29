import pandas as pd
from dateutil import relativedelta
import numpy as np
import time
from datetime import date
from datetime import datetime
import pickle

def cities_filter(df, cidades):
    df = df.loc[df['city'].isin(cidades)]
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    return df

def drop_columns(df, columns):
    df = df.drop(columns)
    df = df.dropna()
    return df

def tag_target(df, raining_list):
    df['target'] = df['condition'].apply(lambda x: 1 if x in raining_list else 0)
    print(df['target'].unique())
    return df

# function to convert columns to float
def to_float(df):
    float_list = list()
    for column_name in df.drop(columns='target').columns:
        if str(df[f'{column_name}'][0]).replace(".", "").replace("-", "").isnumeric() == True:
            float_list.append(column_name)

    for column in df.columns:
        if column in float_list:
            df[f'{column}'] = df[f'{column}'].astype("float")
    return df

def algorithm_columns(df, columns):
    df = df[[columns]]
    return df

# Calculate the difference between the actual and previous register
def date_diff_calc(df):
    df = df.sort_values(by=['city', 'last_updated']).reset_index().drop(columns='index')
    i = 1
    date_diff_list = list()
    for cell in df['last_updated']:
        if i < len(df['last_updated']):
            date_diff_min = (df['last_updated'][i] - cell).total_seconds()/60
            date_diff_list.append(date_diff_min)
            i += 1
    df['date_diff'] = pd.DataFrame(date_diff_list)
    return df

# create a column that tells us weather is raining in the next hour
def rain_next1(df):
    i = 4
    rain_next1 = list()
    for cell in df['target']:
        if i < len(df['target']):
            rain_next1.append(df['target'][i])
            i += 1
    df['target_1'] = pd.DataFrame(rain_next1)
    return df

def save_object(obj, obj_name):
    f = open(obj_name, 'wb')
    pickle.dump(obj, f)
    f.close()