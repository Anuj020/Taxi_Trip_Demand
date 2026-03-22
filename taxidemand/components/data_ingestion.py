from taxidemand.exception.exception import TaxiDemandException
from taxidemand.logging.logger import logging
from taxidemand.entity.artifact_entity import DataIngestionArtifact
from taxidemand.entity.config_entity import DataIngestionConfig
import os
import sys
from typing import List
import psycopg2
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise TaxiDemandException(e,sys)

    def export_postgres_data_into_dataframe(self):
        """
        Read data from PostgreSQL
        """
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(
                host = os.getenv("HOST"),
                dbname = os.getenv("DBNAME"),
                user = os.getenv("DB_USER"),
                password = os.getenv("PASSWORD")
            )

            cur = conn.cursor()
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_testing_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_training_file_path),exist_ok=True)
            train_data_query = f"""
                    COPY (
                    SELECT * from {os.getenv("TRAIN_DATA_TABLE")}
                    ) TO STDOUT WITH CSV HEADER
                    """
            with open(self.data_ingestion_config.raw_training_file_path,'w') as file:
                cur.copy_expert(train_data_query,file)

            test_data_query = f"""
                    COPY (
                    SELECT * from {os.getenv("TEST_DATA_TABLE")}
                    ) TO STDOUT WITH CSV HEADER
                    """
            with open(self.data_ingestion_config.raw_testing_file_path,'w') as file:
                cur.copy_expert(test_data_query,file)
            
            train_df = pd.read_csv(self.data_ingestion_config.raw_training_file_path)
            return train_df
        except Exception as e:
            raise TaxiDemandException(e,sys)

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()


    # def export_data_into_feature_store(self,dataframe:pd.DataFrame):
    #     feature_store_file_path = self.data_ingestion_config.feature_store_file_path

    #     dir_name = os.path.dirname(feature_store_file_path)
    #     os.makedirs(dir_name,exist_ok= True)
    #     dataframe.to_csv(feature_store_file_path,index=False,header=True)
    #     return dataframe

    def split_data_as_train_validation(self,dataframe:pd.DataFrame):
        try:
            train_set , validation_set = train_test_split(
                dataframe,test_size = self.data_ingestion_config.train_test_split_ratio, 
                random_state=self.data_ingestion_config.random_state
            )
            logging.info("Peforming train val split on dataframe")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting train and validation file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index = False,header = True
            )
            logging.info("train set is created.")
            validation_dir = os.path.dirname(self.data_ingestion_config.validation_data_dir)
            os.makedirs(validation_dir,exist_ok=True)
            validation_set.to_csv(
                self.data_ingestion_config.validation_data_dir,index = False,header = True
            )
            logging.info("validation set is created.")
        except Exception as e:
            raise TaxiDemandException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_postgres_data_into_dataframe()
            # dataframe = self.export_data_into_feature_store(dataframe)

            self.split_data_as_train_validation(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path= self.data_ingestion_config.training_file_path,
                test_file_path= self.data_ingestion_config.raw_testing_file_path,
                validation_file_path= self.data_ingestion_config.validation_data_dir
            )
            return data_ingestion_artifact
        except Exception as e:
            raise TaxiDemandException(e,sys)