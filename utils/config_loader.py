import os
import logging

def get_database_url() -> str:
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

    if POSTGRES_USER is None or POSTGRES_PASSWORD is None:
        logging.warning('%(asctime)s | %(name)s Database user information is undefined or defined partitialy, using default values \n Note: That may cause problems with database connection')
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = '12345'

    if POSTGRES_SERVER is None:
        logging.warning('Database server information is undefined, using localhost')
        POSTGRES_SERVER = 'localhost'

    if POSTGRES_PORT is None:
        logging.warning('Database port information is undefined, using 5432')
        POSTGRES_PORT = '5432'

    if POSTGRES_DB is None:
        logging.critical('Database name is undefined, exiting')
        #todo: create new database
        exit(1)


    return f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
