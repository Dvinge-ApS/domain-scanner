# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @staticmethod
    def get_database_url():
        return os.getenv('DATABASE_URL', 'sqlite:///./test.db')

    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '5'))
    QUERY_DELAY = int(os.getenv('QUERY_DELAY', '2'))
    HOURLY_LIMIT = int(os.getenv('HOURLY_LIMIT', '1000'))