from .base import BaseConfig

class Config(BaseConfig):
    DEBUG = True
    
    # Uncomment if not using docker
    #INFLUX_DATABASE_URI = "http://localhost:8086"
    
    ENABLE_TOKEN_AUTH = False
    
    API_BASE_URL = "http://app"
    PORT = 8080
    
    # Cloud credentials
    API_KEY = "CLOUD_ACCESS_KEY"
    API_HOST = "https://api.us-east-1.mbedcloud.com"

