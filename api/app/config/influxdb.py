import os
from influxdb_client import InfluxDBClient

from dotenv import load_dotenv

load_dotenv()

url = "http://localhost:8086/"
token = os.getenv('INFLUXDB_TOKEN')
org = os.getenv('INFLUXDB_ORG')
bucket = os.getenv('INFLUXDB_BUCKET')

client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)
