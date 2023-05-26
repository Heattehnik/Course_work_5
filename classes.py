from dotenv import load_dotenv
import os
from abc import ABC
import psycopg2

load_dotenv()


class DatabaseConnector:
    __db_address = os.getenv('DATABASE_ADDRESS')
    __db_name = os.getenv('DATABASE_NAME')
    __db_user = os.getenv('DATABASE_USER')
    __db_password = os.getenv('DATABASE_PASSWORD')

    def __init__(self):
        self.connect = psycopg2.connect(host=self.__db_address,
                                        database=self.__db_name,
                                        user=self.__db_user,
                                        password=self.__db_password)
        self.cursor = self.connect.cursor()