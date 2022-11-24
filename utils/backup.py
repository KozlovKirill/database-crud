import os
import logging
import requests
import gzip
import delegator

# from utils import load_dotenv, Path

# load_dotenv(Path('.') / '.env')

def backup():
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

    with gzip.open('backup.gz', 'wb') as backup_file:
        c = delegator.run(f'pg_dump -h {POSTGRES_SERVER} -U {POSTGRES_USER} {POSTGRES_DB}') #block=False, out=backup_file
        backup_file.write(c.out.encode('utf-8'))
    logging.debug('Backup created')

def send_backup():
    with open('backup.gz', 'rb') as backup_file:
        url = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_BOT_TOKEN")}/sendDocument?chat_id={os.getenv("TELEGRAM_CHAT_ID")}'
        r = requests.post(url, files={'backup.gz': backup_file})
    logging.debug('Backup sent')

# def restore():