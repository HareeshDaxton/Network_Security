import sys
import os
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from network_security_workspace.constant.training_pipeline import TRAGET_COLUMN
from sklearn.pipeline import Pipeline

from network_security_workspace.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security_workspace.entity.artifact_entity import (DataValidationArtifact, DataTransformationArtifact)
from network_security_workspace.entity.config_entity import DataTransformationConfig
from network_security_workspace.exception.exception import NetworkSecurityException
from network_security_workspace.logging.logger import logging
from network_security_workspace.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact : DataValidationArtifact, data_transformation_config : DataTransformationConfig):
        try:
            self.data_validation_artifact  : DataValidationArtifact = data_validation_artifact
            self.data_transformation_config : DataTransformationConfig = data_transformation_config
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        logging.info("Entered the get_data_transformer_object method of Data_Transformation class")
        try:
            imputer : KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor : Pipeline = Pipeline(steps=[("imputer", imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:     
            raise NetworkSecurityException(e, sys)  
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation")
        try:
            logging.info("stating data transformation")
            
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            input_feature_train_df = train_df.drop(columns=[TRAGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TRAGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            
            input_feature_test_df = test_df.drop(columns=[TRAGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TRAGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)
            
            preprocessor = self.get_data_transformer_object() 
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object,)
            
            # data_transform_artifact = DataTransformationArtifact(
            #     transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
            #     transformed_train_file_pat = self.data_transformation_config.transformed_train_file_path,
            #     transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            # )
            data_transform_artifact = DataTransformationArtifact(
            transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
            transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transform_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)            
