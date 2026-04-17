import yaml
from taxidemand.logging.logger import logging
from taxidemand.exception.exception import TaxiDemandException
import os,sys
import math
import pickle
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
# read yaml file
def read_yaml(file_path:str) -> dict:
    try:
        with open(file_path,'rb') as yaml_files:
            return yaml.safe_load(yaml_files)
    except Exception as e:
        raise TaxiDemandException(e,sys)
    
# write yaml file
def write_yaml_file(file_path:str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
            logging.info("content has been dumped.")
    except Exception as e:
        raise TaxiDemandException(e,sys)

# save numpy array in specific file path
def save_numpy_array_data(file_path: str,array: np.array):
    """
    file_path: str location of file to save
    array: array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise TaxiDemandException(e,sys)

# load numpy data
def load_numpy_array_data(file_path: str) -> np.array:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file:{file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            np.load(file_path)
            logging.info("numpy array is loaded")
    except Exception as e:
        raise TaxiDemandException(e,sys)
    
# saving objects -- model, preprocesser
def save_object(file_path:str, obj: object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
            logging.info("object has been saved")
    except Exception as e:
        raise TaxiDemandException(e,sys)

# loading objects
def load_object(file_path:str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file:{file_path} is not exists")
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise TaxiDemandException(e,sys)


#Haversine Model
def haversine(lat1,lat2,lon1,lon2, radius_of_earth = 6371):
    delta_lat = np.radians(lat2 - lat1)
    delta_lon = np.radians(lon2 - lon1) 
    half_part = (pow(np.sin(delta_lat/2),2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * pow(np.sin(delta_lon/2),2))
    haversine_distance = 2 * radius_of_earth * np.arcsin(np.sqrt(half_part))
    return haversine_distance

# Manhattan Distance 
def manhattan_distance(lat1,lat2,lon1,lon2):
    return abs(lat2-lat1) + abs(lon2-lon1)
    
# Bearing 
def bearing(lat1,lat2,lon1,lon2):
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)
    lon1 = np.radians(lon1)
    lon2 = np.radians(lon2)
    delta_lon = lon2-lon1

    x = np.sin(delta_lon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1)*np.cos(lat2) * np.cos(delta_lon)
    theta = np.atan2(x,y)
    bearing_formula = (theta *(180/np.pi) + 360) % 360
    return bearing_formula


def filter_passanger_count(df):
    df = df.copy()
    return df[(df["passenger_count"] > 0) & (df["passenger_count"] <=6 )]


def encode_vendor(df):
    df = df.copy()
    df = pd.get_dummies(df, columns=["vendor_id"], prefix="vendor", drop_first=True)

    if "vendor_2" not in df.columns:
        df["vendor_2"] = 0

    df["vendor_2"] = df["vendor_2"].astype(int)
    return df


def map_store_and_fwd(df):
    df = df.copy()
    df["store_and_fwd_flag"] = df["store_and_fwd_flag"].map({"Y": 1, "N": 0})
    return df


def add_datetime_features(df):
    df = df.copy()

    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])

    if "dropoff_datetime" in df.columns:
        df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])

    df["pickup_hour"] = df["pickup_datetime"].dt.hour
    df["pickup_day"] = df["pickup_datetime"].dt.day
    df["pickup_weekday"] = df["pickup_datetime"].dt.weekday
    df["pickup_month"] = df["pickup_datetime"].dt.month
    df["is_weekend"] = df["pickup_weekday"].isin([5, 6]).astype(int)
    df["rush_hour"] = df["pickup_hour"].isin([6, 7, 8, 9, 16, 17, 18, 19, 20]).astype(int)

    return df

def remove_coordinate_outliers(df):
    df = df.copy()

    return df[
        df.pickup_latitude.between(
            df.pickup_latitude.quantile(0.01),
            df.pickup_latitude.quantile(0.99)
        ) &
        df.dropoff_latitude.between(
            df.dropoff_latitude.quantile(0.01),
            df.dropoff_latitude.quantile(0.99)
        ) &
        df.pickup_longitude.between(
            df.pickup_longitude.quantile(0.01),
            df.pickup_longitude.quantile(0.99)
        ) &
        df.dropoff_longitude.between(
            df.dropoff_longitude.quantile(0.01),
            df.dropoff_longitude.quantile(0.99)
        )
    ]

def log_transform_target(df, target_col="trip_duration"):
    df = df.copy()

    if target_col in df.columns:
        df[target_col] = np.log1p(df[target_col])

    return df
