# (c) @TheLx0980
# Year : 2023

import logging, re
from os import environ

id_pattern = re.compile(r'^.\d+$')



API_ID = environ.get('API_ID', '2992000')
API_HASH = environ.get('API_HASH', '235b12e862d71234ea222082052822fd')
SESSION = environ.get('SESSION', '')
ADMINS = [str(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
