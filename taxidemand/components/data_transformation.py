from taxidemand.logging.logger import logging
from taxidemand.exception.exception import TaxiDemandException
from taxidemand.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from taxidemand.entity.config_entity import DataTransformationConfig
from taxidemand.constants.training_pipeline import TARGET_COLUMN
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from taxidemand.utils import utils
from sklearn.pipeline import Pipeline
import os
import sys
import numpy as np
import pandas as pd

class DataTransformation():
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                data_transformation_config: DataTransformationConfig):
        try:
            
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            
        except Exception as e:
            raise TaxiDemandException(e,sys)

    def transformed_train_data(self):
        try:

            kmean = KMeans(n_clusters=50, random_state=42)

            train_df = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            train_df = utils.filter_passanger_count(train_df)
            train_df = utils.encode_vendor(train_df)
            train_df = train_df.drop("id",axis=1)
            train_df = utils.add_datetime_features(train_df)
            train_df = utils.remove_coordinate_outliers(train_df)
            train_df['total_distance_km'] = utils.haversine(train_df['pickup_latitude'],train_df['dropoff_latitude'],train_df['pickup_longitude'],train_df['dropoff_longitude'])
            train_df['manhattan_distance'] = utils.manhattan_distance(train_df['pickup_latitude'],train_df['dropoff_latitude'],train_df['pickup_longitude'],train_df['dropoff_longitude'])
            train_df['bearing_direction'] = utils.bearing(train_df['pickup_latitude'],train_df['dropoff_latitude'],train_df['pickup_longitude'],train_df['dropoff_longitude'])
            coords_pickup = train_df[['pickup_latitude', 'pickup_longitude']]
            coords_dropoff = train_df[['dropoff_latitude', 'dropoff_longitude']]
            train_df['pickup_cluster'] = kmean.fit_predict(coords_pickup)
            train_df['dropoff_cluster'] = kmean.fit_predict(coords_dropoff)
            train_df['trip_duration'] = np.log1p(train_df['trip_duration'])
            train_df['rush_hour'] = train_df['pickup_hour'].isin([6,7,8,9,16,17,18,19,20]).astype(int)
            train_df['store_and_fwd_flag'] = train_df['store_and_fwd_flag'].map({'Y':1, 'N':0})
            train_df_preprocessed = train_df.drop(columns=[
                        'pickup_datetime', 'dropoff_datetime',
                        'pickup_latitude', 'pickup_longitude',
                        'dropoff_latitude', 'dropoff_longitude',],errors='ignore')
            utils.save_object(self.data_transformation_config.data_transformation_keman_path, kmean)
            return train_df_preprocessed
        except Exception as e:
            raise TaxiDemandException(e,sys)

    def transformed_test_data(self):
        try:

            kmean = utils.load_object(self.data_transformation_config.data_transformation_keman_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            test_df = utils.filter_passanger_count(test_df)
            test_df = utils.encode_vendor(test_df)
            test_df = test_df.drop("id",axis=1)
            test_df = utils.add_datetime_features(test_df)
            test_df = utils.remove_coordinate_outliers(test_df)
            test_df['total_distance_km'] = utils.haversine(test_df['pickup_latitude'],test_df['dropoff_latitude'],test_df['pickup_longitude'],test_df['dropoff_longitude'])
            test_df['manhattan_distance'] = utils.manhattan_distance(test_df['pickup_latitude'],test_df['dropoff_latitude'],test_df['pickup_longitude'],test_df['dropoff_longitude'])
            test_df['bearing_direction'] = utils.bearing(test_df['pickup_latitude'],test_df['dropoff_latitude'],test_df['pickup_longitude'],test_df['dropoff_longitude'])
            coords_pickup = test_df[['pickup_latitude', 'pickup_longitude']]
            coords_dropoff = test_df[['dropoff_latitude', 'dropoff_longitude']]
            test_df['pickup_cluster'] = kmean.fit_predict(coords_pickup)
            test_df['dropoff_cluster'] = kmean.fit_predict(coords_dropoff)
            test_df['rush_hour'] = test_df['pickup_hour'].isin([6,7,8,9,16,17,18,19,20]).astype(int)
            test_df['store_and_fwd_flag'] = test_df['store_and_fwd_flag'].map({'Y':1, 'N':0})
            test_df_preprocessed = test_df.drop(columns=[
                        'pickup_datetime', 'dropoff_datetime',
                        'pickup_latitude', 'pickup_longitude',
                        'dropoff_latitude', 'dropoff_longitude',],errors='ignore')
            return test_df_preprocessed
        except Exception as e:
            raise TaxiDemandException(e,sys)
    
    def get_data_transformer_object(self, dataframe):
        num_cols = dataframe.select_dtypes(include=['int64', 'float64']).columns.tolist()

        preprocesser = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), num_cols)
            ]
        )
        return preprocesser

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Initiated Data Transformation Method")
        try:
            logging.info("Starting data trnasformation")
            
            ## Training Dataframe

            train_df = self.transformed_train_data()
            input_train_df = train_df.drop(columns=[TARGET_COLUMN], axis = 1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            ## Testing Dataframe
            test_df = self.transformed_test_data()

            preprocessor = self.get_data_transformer_object(input_train_df)
            preprocessor_obj = preprocessor.fit(input_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(test_df)

            # convert into array from dataframes
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = transformed_input_test_feature

            # save numpy array data
            utils.save_numpy_array_data(self.data_transformation_config.data_transformation_train_file_path,array=train_arr)
            utils.save_numpy_array_data(self.data_transformation_config.data_transformation_test_file_path,array=test_arr)
            utils.save_object(self.data_transformation_config.data_transformation_object_file_path,preprocessor_obj)

            # preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformd_object_file_path= self.data_transformation_config.data_transformation_object_file_path,
                transformd_train_file_path= self.data_transformation_config.data_transformation_train_file_path,
                transformd_test_file_path= self.data_transformation_config.data_transformation_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise TaxiDemandException(e,sys)