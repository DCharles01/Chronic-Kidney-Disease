from dotenv import load_dotenv
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# get abs path of current script
load_dotenv(os.path.join(Path(os.path.abspath(__file__)).parent.parent, '.env'))

DB_USER = os.environ.get('USERNAME')
DB_PASSWORD = os.environ.get('PASSWORD')
DB_NAME = os.environ.get('DB')
DEV_DB_NAME = os.environ.get('DEV_DB')
TEST_DB_NAME = os.environ.get('TEST_DB')
DB_HOST = os.environ.get('HOST')
DB_PORT = os.environ.get('PORT')
