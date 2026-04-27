from taxidemand.logging.logger import logging
from taxidemand.exception.exception import TaxiDemandException
from taxidemand.components.data_ingestion import DataIngestion
from taxidemand.components.data_validation import DataValidation
from taxidemand.components.data_transformation import DataTransformation
from taxidemand.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from taxidemand.components.model_trainer import ModelTrainer
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
        #print(data_validation_artifact)

        # data transformation
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        logging.info("Data Transformation Started")
        data_transformation = DataTransformation(data_ingestion_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        #print(data_transformation_artifact)
        logging.info("Data Transformation Completed")

        # Model trainer
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        logging.info("Model Training Started")
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)
        logging.info("Model Trainer Completed")
    except Exception as e:
        raise TaxiDemandException(e,sys)
    
    