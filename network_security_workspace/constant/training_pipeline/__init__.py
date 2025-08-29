import os
import sys
import pandas as pd
import numpy as np


"""
Defining common var name for tarining pipeline

"""

TRAGET_COLUMN : str = "Result"
PIPELINE_NAME : str = "network_security_workspace"
ARTIFACT_DIR : str = "Artifacta"
FILE_NAME : str = "Dataset_Phising_Website.csv"

TRAIN_FILE_NAME : str = "train.csv"
TEST_FILE_NAME : str = "test.csv"


"""
Data Ingestion rlated constant start DATA_INGESTION varianles name
    
"""

DATA_INGESTION_COLLECTION_NAME : str = "Network_Security"
DATA_INGESTION_DATABASE_NAME : str = "hareeshkumarh29"
DATA_INGESTION_DIR_NAME : str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION : float = 0.2