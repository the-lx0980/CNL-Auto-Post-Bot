# (c) @TheLx0980
# Year : 2023

import logging
from os import environ

API_ID = environ.get('API_ID', '')
API_HASH = environ.get('API_HASH', '')
ADMIN_ID = environ.get('ADMIN_ID', '')
SESSION = environ.get('SESSION', '')
ADMINS = environ.get('ADMINS', '').split(" ") 

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
