from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ["headers"] 
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=72)

security = AuthX(config=config)

