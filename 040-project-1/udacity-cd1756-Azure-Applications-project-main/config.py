import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))
load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('USER_SECRET_KEY')

    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT')
    BLOB_CONNECTION_STRING = os.environ.get('BLOB_CONNECTION_STRING')
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER')
    
    SQL_SERVER = os.environ.get('SQL_SERVER')
    SQL_DATABASE = os.environ.get('SQL_DATABASE')
    SQL_USERNAME = os.environ.get('SQL_USERNAME')
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{SQL_USERNAME}:{quote_plus(SQL_PASSWORD)}@{SQL_SERVER}:1433/{SQL_DATABASE}?"
        f"driver=ODBC+Driver+17+for+SQL+Server&"
        f"TrustServerCertificate=yes&"
        f"connection_timeout=30&"
        f"encrypt=yes"
    )
    
    # SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://' + SQL_USERNAME + '@' + SQL_SERVER + ':' + SQL_PASSWORD + '@' + SQL_SERVER + ':1433/' + SQL_DATABASE  + '?driver=ODBC+Driver+17+for+SQL+Server'
    # SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://' + SQL_USERNAME + ':' + SQL_PASSWORD + '@' + SQL_SERVER + ':1433/' + SQL_DATABASE  + '?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### Info for MS Authentication ###
    CLIENT_SECRET = os.environ.get("USER_CLIENT_SECRET")
    if not CLIENT_SECRET:
        raise ValueError("Need to define CLIENT_SECRET environment variable")

    AUTHORITY = os.environ.get('AUTHORITY', "https://login.microsoftonline.com/common")
    APP_CLIENT_ID = os.environ.get('APP_CLIENT_ID')
    REDIRECT_PATH = os.environ.get('REDIRECT_PATH', "/getAToken")
    SCOPE = ["User.Read"]
    SESSION_TYPE = "filesystem"