from datetime import datetime
import os
from taxidemand.logging.logger import logging
from taxidemand.exception.exception import TaxiDemandException
from taxidemand.constants import training_pipeline

logging.info(training_pipeline.PIPELINE_NAME)

class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp:str = timestamp

class DataIngestionConfig:
    # Creating some paths for data ingestion

    def __init__(self,training_pipeline_config: TrainingPipelineConfig):

        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.validation_data_dir: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.VALIDATION_DIR,training_pipeline.VALIDATION_FILE_NAME
        )

        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME
        )

        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_DIR_NAME,training_pipeline.TEST_FILE_NAME
        )

        self.raw_testing_file_path: str = os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_RAW_DIR,training_pipeline.RAW_TEST_DATA_PATH
        )

        self.raw_training_file_path: str = os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_RAW_DIR, training_pipeline.RAW_TRAIN_DATA_PATH
        )

        self.train_test_split_ratio: float = training_pipeline.DATA_INGEATION_TRAIN_TEST_SPLIT_RATION
        self.random_state: int = training_pipeline.RANDOM_STATE
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.train_table_name: str = training_pipeline.DATA_INGESTION_TRAIN_TABLE_NAME
        self.test_table_name: str = training_pipeline.DATA_INGESTION_TEST_TABLE_NAME    
        
