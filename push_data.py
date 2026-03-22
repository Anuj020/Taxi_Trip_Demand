
from taxidemand.logging.logger import logging
from taxidemand.exception.exception import TaxiDemandException
from taxidemand.constants.training_pipeline import TRAIN_FILE_PATH,TEST_FILE_PATH
import psycopg
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
import certifi
import sys
import json
load_dotenv()



ca = certifi.where()
        

class PostgreSQL():
    def __init__(self):
        self.DB_CONFIG = {
            "host": os.getenv("HOST"),
            "port": os.getenv("PORT"),
            "dbname": os.getenv("DBNAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("PASSWORD")
        }
    def insert_to_postgresql(self,file_path,sql_query):
        try:
            with psycopg.connect(**self.DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    with cur.copy(sql_query) as copy:
                        with open(file_path, 'r',encoding="utf-8") as file:
                            for line in file:
                                copy.write(line)
                conn.commit()
                logging.info(f"{file_path} insreted successfully.")
        except Exception as e:
            raise TaxiDemandException(e,sys)
def main():
    db = PostgreSQL()
    files = [TRAIN_FILE_PATH,TEST_FILE_PATH]

    for file in files:
        file_name = os.path.basename(file)
        if "train" in file_name:
            sql_query = """
                    COPY train_data
                    FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
                        """
        else:
            sql_query = """
                    COPY test_data
                    FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
                        """
        logging.info(f"loading local file {file} into postgresSQL")
        db.insert_to_postgresql(file,sql_query)
if __name__ == "__main__":
    main()