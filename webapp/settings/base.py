class BaseConfig(object):

    DEBUG = False
    
    INFLUX_HOST = "http://influxdb"
    INFLUX_PORT = "8086"
    INFLUX_DATABASE_URI = "http://influxdb:8086"
    
    API_BASE_URL = None
    
    ENABLE_TOKEN_AUTH = True

    # Cloud credentials
    API_KEY = None
    API_HOST = "https://api.mbedcloud.com"
    
    MODULES = [
        "webapp",
    ]
