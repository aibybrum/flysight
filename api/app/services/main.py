from sqlalchemy.orm import Session
import api.app.config.influxdb as influxdb


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class PostgresService(DBSessionContext):
    pass


class InfluxdbService:
    def __init__(self, bucket: influxdb.bucket, client: influxdb.client):
        self.bucket = bucket
        self.client = client
