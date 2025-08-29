from network_security_workspace.components.data_ingestion import DataIngestion
from network_security_workspace.logging.logger import logging
from network_security_workspace.exception.exception import NetworkSecurityException
from network_security_workspace.entity.config_entity import DataIngestionConfig
from network_security_workspace.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == "__main__":
    
    try:
        tainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(tainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("initiate the data ingestion")
        dataingestionartifacts = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifacts)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)