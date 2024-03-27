from sqlalchemy.orm import Session
import app.config.influxdb as influxdb


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class PostgresService(DBSessionContext):
    pass


class PostgresCRUD(DBSessionContext):
    pass


class InfluxdbServiceContext(object):
    def __init__(self):
        self.bucket = influxdb.bucket
        self.client = influxdb.client

class InfluxdbCRUD(InfluxdbServiceContext):
    pass
