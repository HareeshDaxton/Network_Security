from network_security_workspace.components.data_ingestion import DataIngestion
from network_security_workspace.logging.logger import logging
from network_security_workspace.exception.exception import NetworkSecurityException
from network_security_workspace.entity.config_entity import DataIngestionConfig, DataValidationConfig
from network_security_workspace.entity.config_entity import TrainingPipelineConfig

from network_security_workspace.components.data_validation import DataValidation

import sys

if __name__ == "__main__":
    
    try:
        # tainingpipelineconfig = TrainingPipelineConfig()
        # dataingestionconfig = DataIngestionConfig(tainingpipelineconfig)
        # data_ingestion = DataIngestion(dataingestionconfig)
        # logging.info("initiate the data ingestion")
        # dataingestionartifacts = data_ingestion.initiate_data_ingestion()
        # logging.info("Completed the data ingestion")
        # print(dataingestionartifacts)
        # data_validation_config = DataValidationConfig(tainingpipelineconfig)
        # data_validation = DataValidation(dataingestionartifacts, data_validation_config)
        # logging.info("Initiate the data validation")
        # data_validation_artifact = data_validation.initiate_data_validation()
        # logging.info("Completed the data validation")
        # print(data_validation_artifact)
        
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
    except Exception as e:
        raise NetworkSecurityException(e, sys)