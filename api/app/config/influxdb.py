import os
from influxdb_client import InfluxDBClient

from dotenv import load_dotenv

load_dotenv()

#url = "http://localhost:8086/"
url = "http://influxdb:8086"
token = os.getenv('DOCKER_INFLUXDB_INIT_ADMIN_TOKEN')
org = os.getenv('DOCKER_INFLUXDB_INIT_ORG')
bucket = os.getenv('DOCKER_INFLUXDB_INIT_BUCKET')

client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)
