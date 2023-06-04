from os import environ
from dotenv import load_dotenv

from pymongo import MongoClient


load_dotenv()
load_dotenv('.env.development')


def get_client():
    connection_string = environ.get('MONGO_DB_CONNECTION')
    if not connection_string:
        raise ValueError('Without connection string in environment variables')
    client = MongoClient(connection_string, serverSelectionTimeoutMS=1000)
    return client


def get_database():
    client = get_client()
    database_name = environ.get('MONGO_DATABASE_NAME', 'eng')

    return client[database_name]
