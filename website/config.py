from dotenv import load_dotenv
from pathlib import Path 
import os

#set path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
  """ Set flask config vars from .env file """

  # load in env variables
  TESTING = os.getenv('TESTING')
  SECRET_KEY = os.getenv('SECRET_KEY')
  FLASK_ENV = os.getenv('FLASK_ENV')