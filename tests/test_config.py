import os
from app.config import Config

def test_config():
    original_url = os.environ.get('DATABASE_URL')
    os.environ['DATABASE_URL'] = 'test_url'
    assert Config.get_database_url() == 'test_url'
    if original_url:
        os.environ['DATABASE_URL'] = original_url
    else:
        del os.environ['DATABASE_URL']