from taxidemand.logging.logger import logging
from taxidemand.exception.exception import TaxiDemandException
from taxidemand.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from taxidemand.entity.config_entity import DataTransformationConfig,ModelTrainerConfig
from taxidemand.constants import training_pipeline
from taxidemand.utils.model.estimators import TaxiDemandModel
from taxidemand.utils import utils
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
import os
import sys

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise TaxiDemandException(e,sys)
    
    # MLflow function

    #Train model
    def train_model(self,X_train,y_train,X_test,y_test):
        model = {
            "XGBoost Regressor": XGBRegressor()}

        params = {"XGBoost Regressor": {
            'n_estimators': training_pipeline.N_ESTIMATORS,
            'learning_rate': training_pipeline.LEARNING_RATE,
            'max_depth': training_pipeline.MAX_DEPTH,
            'min_child_weight': training_pipeline.MIN_CHILD_WEIGHTS
        }}

        model_report: list = utils.evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                                  models = model,param=params)

        # Get best model
        best_model_name = max(model_report, key=lambda x: model_report[x]["test_score"])
        best_model = model_report[best_model_name]["model"]

        train_score = model_report[best_model_name]["train_score"]
        test_score = model_report[best_model_name]["test_score"]
        preprocessor = utils.load_object(file_path=self.data_transformation_artifact.transformd_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        taxidemand_model = TaxiDemandModel(preprocessor = preprocessor, model=best_model)
        utils.save_object(self.model_trainer_config.trained_model_file_path,obj=taxidemand_model)

        #model trainer artifact
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_name=self.model_trainer_config.trained_model_file_path,
                                                      train_matric_artifact=train_score,
                                                      test_matric_artifact=test_score)
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact
    
    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformd_train_file_path
            validation_file_path = self.data_transformation_artifact.transformd_validation_file_path
            train_arr = utils.load_numpy_array_data(train_file_path)
            test_arr = utils.load_numpy_array_data(validation_file_path)
            X_train,y_train,X_test,y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1], 
                test_arr[:, -1]
            )

            model = self.train_model(X_train,y_train,X_test,y_test)
        
        except Exception as e:
            raise TaxiDemandException(e,sys)