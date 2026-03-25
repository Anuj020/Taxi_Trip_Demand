from taxidemand.logging.logger import logging
from taxidemand.exception.exception import TaxiDemandException
from taxidemand.components.data_ingestion import DataIngestion
from taxidemand.components.data_validation import DataValidation
from taxidemand.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig, DataValidationConfig
import sys

if __name__ == "__main__":
    try:
        #data ingestion
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiate the data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")

        # data validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initiate Data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(" Data validation completed")
        print(data_validation_artifact)

    except Exception as e:
        raise TaxiDemandException(e,sys)
    
    