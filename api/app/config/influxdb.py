import os
from influxdb_client import InfluxDBClient

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('./../env/.env')
load_dotenv(dotenv_path=dotenv_path)

environment = os.getenv('ENVIRONMENT')
url = ''
if environment == 'dev':
    url = "http://localhost:8086/"
elif environment == 'docker':
    url = "http://influxdb:8086"
    
token = os.getenv('DOCKER_INFLUXDB_INIT_ADMIN_TOKEN')
org = os.getenv('DOCKER_INFLUXDB_INIT_ORG')
bucket = os.getenv('DOCKER_INFLUXDB_INIT_BUCKET')

client = InfluxDBClient(
    url=url,
    token=token,
    org=org,
    enable_gzip=True,  
    buffer_capacity=10000,  
    batch_size=5000, 
    retries=3,  
    max_retry_delay=5000
)
