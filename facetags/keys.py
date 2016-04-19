"""
    Accessor for private keys in the environment
"""

import os
import secretkeys

secretkeys.setkeys()

APP_SECRET = os.getenv('APP_SECRET')
APP_DEBUG = str(os.getenv('APP_DEBUG')).lower() == 'true'

DB_NAME = os.getenv('DB_NAME')
DB_SCHEMA = os.getenv('DB_SCHEMA')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

CLARIFAI_ID = os.environ["CLARIFAI_ID"]
CLARIFAI_SECRET = os.environ["CLARIFAI_SECRET"]

FACEBOOK_ID = os.environ["FACEBOOK_ID"]
FACEBOOK_SECRET = os.environ["FACEBOOK_SECRET"]