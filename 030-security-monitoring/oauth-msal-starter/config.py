import os
from dotenv import load_dotenv

load_dotenv(".env_config")
load_dotenv(f".env.{os.getenv("ENV")}")

class Config(object):
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
    # AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

    # TODO: Enter your application client ID here
    APPLICATION_CLIENT_ID = os.environ.get('APPLICATION_CLIENT_ID')
    REDIRECT_PATH = "/getAToken"

    # You can find the proper permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    SCOPE = ["User.Read"]

    SESSION_TYPE = "filesystem"  # So token cache will be stored in server-side session
