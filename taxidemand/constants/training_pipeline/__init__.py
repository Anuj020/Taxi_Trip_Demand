import os
import sys
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


"""
defining common constant variable for training pipeline
"""
TRAIN_FILE_PATH: str = "/Users/anuj/Desktop/MLOPS/TaxiDemand/Taxi_data/train.csv"
TEST_FILE_PATH: str = "/Users/anuj/Desktop/MLOPS/TaxiDemand/Taxi_data/test.csv"
TARGET_COLUMN = "trip_duration"
PIPELINE_NAME: str = "taxidemand"
ARTIFACT_DIR: str = "Artifacts"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
VALIDATION_FILE_NAME: str = "validation.csv"

RAW_TRAIN_DATA_PATH: str = 'raw_train.csv'
RAW_TEST_DATA_PATH: str = 'raw_test.csv'


SAVED_MODEL_DIR =  os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"
KMEAN_CLUSTER = "kmean"

"""
    Defining constants for data ingestion
"""
DATA_INGESTION_DATABASE_NAME: str = os.getenv("DBNAME")
DATA_INGESTION_TRAIN_TABLE_NAME: str = os.getenv("TRAIN_DATA_TABLE")
DATA_INGESTION_TEST_TABLE_NAME: str = os.getenv("TEST_DATA_TABLE")
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
VALIDATION_DIR: str = "validation"
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_RAW_DIR: str = 'raw_data'
DATA_INGEATION_TRAIN_TEST_SPLIT_RATION: float = 0.2
RANDOM_STATE: int = 42


"""
    Data Validation constants
"""

DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'report.yaml'
DRIFT_THRESHOLD: float = 0.05


"""
    Data Transformation constants
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR_NAME: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT: str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pickel"