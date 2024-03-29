import app.config.influxdb as influxdb
import pandas as pd

class InfluxDBService:
    def __init__(self):
        self.client = influxdb.client
        self.bucket = influxdb.bucket
