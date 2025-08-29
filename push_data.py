import os
import sys
import json
import certifi

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

print(MONGO_DB_URL)
ca = certifi.where()

import pandas as pd
import pymongo
import numpy as np
from network_security_workspace.logging.logger import logging
from network_security_workspace.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records            
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_mongodb_data(self, records, database, collections):
        try:
            self.records = records
            self.database = database
            self.collections = collections
            
            # self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            
            self.collections = self.database[self.collections]
            self.collections.insert_many(self.records)
            return(len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
if __name__ == "__main__":
    FILE_PATH=r"Network_Data\Dataset_Phising_Website.csv"
    DATABASE="hareeshkumarh29"
    collection="Network_Security"
    networkj=NetworkDataExtract()
    records=networkj.csv_to_json(file_path=FILE_PATH)
    print(records)
    no_of_records=networkj.insert_mongodb_data(records, DATABASE, collection)
    print(len(no_of_records))



