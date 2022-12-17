import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


# Url for database connection
SQLALCHEMY_DATABASE_URL = (
    "postgresql://"
    f"{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

# Engine conneciton
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Create session for conneciton
SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)
# Declarative connections
Base = declarative_base()
# Create a database seccion for query
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()