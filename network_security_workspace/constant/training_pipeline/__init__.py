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

SCHEMA_FILE_PATH : str = os.path.join("data_schema", "schema.yaml")


"""
Data Ingestion rlated constant start DATA_INGESTION variables name
    
"""

DATA_INGESTION_COLLECTION_NAME : str = "Network_Security"
DATA_INGESTION_DATABASE_NAME : str = "hareeshkumarh29"
DATA_INGESTION_DIR_NAME : str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION : float = 0.2


"""
Data validation ralated constant start DATA_VALIDATION variables name
"""

DATA_VALIDATION_DIR_NAME : str = "data_validation"
DATA_VALIDATION_VALID_DIR : str = "validated"
DATA_VALODATION_INVALID_DIR : str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIDATION_DRIFT_RREPORT_FILE_NAME : str = "report.yaml"