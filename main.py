from network_security_workspace.components.data_ingestion import DataIngestion
from network_security_workspace.logging.logger import logging
from network_security_workspace.exception.exception import NetworkSecurityException
from network_security_workspace.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from network_security_workspace.entity.config_entity import TrainingPipelineConfig

from network_security_workspace.components.data_validation import DataValidation
from network_security_workspace.components.data_transformation import DataTransformation
from network_security_workspace.components.model_trainer import ModelTrainer
from network_security_workspace.components.model_trainer import *
import sys

if __name__ == "__main__":
    
    try:
        training_pipeline_config = TrainingPipelineConfig()   # fixed typo
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        
        logging.info("Initiating Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Completed Data Ingestion")
        print(data_ingestion_artifact)
        
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        
        logging.info("Initiating Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Completed Data Validation")
        print(data_validation_artifact)
        
        logging.info("Starting Data Transformation")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Completed Data Transformation")
        
        logging.info("model training started")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config) 
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        
        logging.info("model training completed")
       
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)