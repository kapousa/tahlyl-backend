import sqlite3
import threading
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# // DB
DATABASE_FILE = "tahlyl-local-dbe.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"  # SQLAlchemy URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_connection():
    """Gets a new connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        logger.info(f"Thread {threading.get_ident()}: Database connection established.")
        return conn
    except sqlite3.Error as e:
        logger.error(f" {threading.get_ident()}: Error connecting to database: {e}")
        raise

def get_db():
    """Gets a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info(f"Thread {threading.get_ident()}: SQLAlchemy session closed.")