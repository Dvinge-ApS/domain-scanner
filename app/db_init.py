from sqlalchemy import create_engine, exc
from app.config import Config
import time
import logging

logger = logging.getLogger(__name__)

def wait_for_db(max_attempts=60):
    engine = create_engine(Config.get_database_url())
    attempt = 0
    while attempt < max_attempts:
        try:
            engine.connect()
            logger.info("Database connection successful")
            return engine
        except exc.OperationalError as e:
            logger.warning(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            attempt += 1
            time.sleep(1)
    raise Exception("Could not connect to the database")

def init_db():
    engine = wait_for_db()
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")