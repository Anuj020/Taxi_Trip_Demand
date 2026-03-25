from taxidemand.exception.exception import TaxiDemandException
from taxidemand.logging.logger import logging
from taxidemand.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from taxidemand.entity.config_entity import DataIngestionConfig,DataValidationConfig
from taxidemand.constants.training_pipeline import TARGET_COLUMN,DRIFT_THRESHOLD
from taxidemand.utils.utils import read_yaml, write_yaml_file
import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

class DataValidation():
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise TaxiDemandException(e,sys)
    
    def detect_dataset_drift(self,train_file_path,test_file_path):
        try:
            status = True
            train_data = pd.read_csv(train_file_path)
            test_data = pd.read_csv(test_file_path)

            if TARGET_COLUMN in train_data.columns:
                    train_df = train_data.drop(columns=[TARGET_COLUMN])
            else:
                 train_df = train_data
            train_cols = set(train_df.columns)
            test_cols = set(test_data.columns)
            sample_dist = ks_2samp(train_cols,test_cols)
            if DRIFT_THRESHOLD <= sample_dist.pvalue:
                 is_found = False
            else:
                 is_found = True
            report = {
            "common_columns": sorted(list(train_cols & test_cols)),
            "missing_in_test": sorted(list(train_cols - test_cols)),
            "extra_in_test": sorted(list(test_cols - train_cols)),
            "schema_match": len(train_cols - test_cols) == 0,
            "p_value" : float(sample_dist.pvalue),
            "drift_status" : is_found
            }

            drift_report_file_path = self.data_validation_config.data_drift_config
            dir_path = os.path.dirname(drift_report_file_path)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return drift_report_file_path
        except Exception as e:
            raise TaxiDemandException(e,sys)
 
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
              train_file_path = self.data_ingestion_artifact.test_file_path
              test_file_path = self.data_ingestion_artifact.test_file_path

              data_drift = self.detect_dataset_drift(train_file_path,test_file_path)
              data_validation_drift = DataValidationArtifact(data_drift)
              return data_validation_drift
        except Exception as e:
             raise TaxiDemandException(e,sys) 

"""
Next steps:
    Add data validation part in main.py
    run main.py
"""