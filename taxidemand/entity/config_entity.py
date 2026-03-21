import os
import sys
import numpy as np
import pandas as pd

"""
defining common constant variable for training pipeline
"""
TARGET_COLUMN = "trip_duration"
PIPELINE_NAME: str = "Taxi-demand"
ARTIFACT_DIR: str = "Artifacts"
TRAIN_FILE_NAME: str = "/Users/anuj/Desktop/MLOPS/TaxiDemand/Taxi_data/train.csv"
TEST_FILE_NAME: str = "/Users/anuj/Desktop/MLOPS/TaxiDemand/Taxi_data/test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")

SAVED_MODEL_DIR =  os.path.join("Saved_models")
MODEL_FILE_NAME = "model.pkl"