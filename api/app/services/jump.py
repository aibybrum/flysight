from uuid import UUID, uuid4
import pandas as pd

from fastapi import UploadFile
from influxdb_client.client.write_api import SYNCHRONOUS

from api.app.utils.dataset.dataset import Dataset
from api.app.schemas.jump import Jump, JumpCreate
from api.app.services.main import InfluxdbService

from datetime import datetime
from influxdb_client.client.util.date_utils import get_date_helper


class JumpCRUD(InfluxdbService):
    def get_measurements(self):
        query = f'import "influxdata/influxdb/schema"\n\nschema.measurements(bucket: "{self.bucket}")'
        tables = self.client.query_api().query(query=query)
        measurements = [row["_value"] for table in tables for row in table]
        return measurements

    def get_tag_values(self, jump_id, tag):
        query = f'import "influxdata/influxdb/schema"\n\nschema.measurementTagValues(bucket: "{self.bucket}", ' \
                f'start: 0, tag: "{tag}", measurement: "{jump_id}")'
        tables = self.client.query_api().query(query=query)
        tag_values = [row["_value"] for table in tables for row in table]
        return tag_values[0] if tag_values else None

    def get_jumps_by_user(self, user_id: UUID):
        result = {}
        for measurement in self.get_measurements():
            uid = self.get_tag_values(measurement, 'user_id')
            name = self.get_tag_values(measurement, 'name')
            if uid is not None and name is not None:
                result.setdefault(uid, []).append({'id': measurement, 'name': name})
        if str(user_id) not in result:
            return None
        return [Jump(id=jump['id'], name=jump['name']) for jump in result.get(str(user_id), [])]

    def get_jump(self, jump_id: UUID):
        query = f'from(bucket: "{self.bucket}") |> range(start: 0) ' \
                f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") ' \
                f'|> filter(fn: (r) => r._measurement == "{jump_id}")'
        db_jump = self.client.query_api().query_data_frame(query=query)
        if not db_jump.empty:
            return Jump(id=db_jump['_measurement'][0], name=db_jump['name'][0])
        return None

    def create_jump(self, user_id: UUID, file: UploadFile):
        dataset = Dataset(file.filename, pd.read_csv(file.file, skiprows=[1]), user_id)
        df = dataset.create()
        db_jump = JumpCreate(id=uuid4(), name=dataset.get_name(), user_id=user_id,
                             data=df.to_json(default_handler=str, orient='records'))
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self.bucket, record=df, data_frame_measurement_name=db_jump.id,
                        data_frame_tag_columns=['name', 'user_id'])
        write_api.__del__()
        return db_jump

    def delete_jump(self, jump_id: UUID):
        start = get_date_helper().to_utc(datetime(1970, 1, 1, 0, 0, 0, 0))
        stop = get_date_helper().to_utc(datetime(2200, 1, 1, 0, 0, 0, 0))
        self.client.delete_api().delete(start, stop, f'_measurement="{jump_id}"', bucket=f'{self.bucket}')


class JumpService(JumpCRUD):
    pass
