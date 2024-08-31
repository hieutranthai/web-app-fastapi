""" Application Settings Module
"""
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy.engine import create_engine, URL
import urllib.parse

load_dotenv()

def get_connection_object(asyncMode: bool = False) -> object:
    engine = os.environ.get("DB_ENGINE") if not asyncMode else os.environ.get("ASYNC_DB_ENGINE")
    dbhost = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = quote_plus(os.environ.get("DB_PASSWORD"))
    dbname = os.environ.get("DB_NAME")
    return URL.create(engine, username, password, dbhost, "5432", dbname)

def get_connection_string(asyncMode: bool = False) -> str:
    """Get the connection string for the database

    Returns:
        string: The connection string
    """
    engine = os.environ.get("DB_ENGINE") if not asyncMode else os.environ.get("ASYNC_DB_ENGINE")
    dbhost = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    #password = quote_plus(os.environ.get("DB_PASSWORD"))#.replace("%", "%%")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")
    return f"{engine}://{username}:{password}@{dbhost}/{dbname}"

# Database Setting
SQLALCHEMY_DATABASE_URL = get_connection_string()
SQLALCHEMY_DATABASE_URL_ASYNC = get_connection_string(asyncMode=True)

SQLALCHEMY_DATABASE_OBJECT = get_connection_object()
SQLALCHEMY_DATABASE_OBJECT_ASYNC = get_connection_object(asyncMode=True)

ADMIN_DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")

# JWT Setting
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))