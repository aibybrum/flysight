from uuid import UUID, uuid4
import pandas as pd
from datetime import datetime

from fastapi import UploadFile
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.util.date_utils import get_date_helper

from app.schemas.jump import Jump, JumpCreate
from app.services.dataset.dataset import DatasetService
from app.services.main import InfluxdbCRUD, PostgresService
from app.services.user import UserService
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult


class JumpService():
    def get_jumps_by_user(self, user_id: UUID) -> ServiceResult:
        # user_result = UserService(self.db).get_user(user_id)
        # if not user_result.success:
        #     return user_result

        db_jumps = JumpCRUD().get_jumps_by_user(user_id)
        return ServiceResult(db_jumps)

    def create_jump(self, user_id: UUID, file: UploadFile) -> ServiceResult:
        # user_result = UserService.get_user(user_id)
        # if not user_result.success:
        #     return user_result

        db_jump = JumpCRUD().create_jump(user_id, file)
        if not db_jump:
            return ServiceResult(AppException.CreateJump())
        return ServiceResult(db_jump)

    def delete_jump(self, jump_id: UUID) -> ServiceResult:
        db_jump = JumpCRUD().get_jump(jump_id)
        if db_jump is None:
            return ServiceResult(AppException.JumpNotFound())
        try:
            JumpCRUD().delete_jump(jump_id)
        except (Exception ,):
            return ServiceResult(AppException.JumpNotModified())
        return ServiceResult({"message": "Jump deleted successfully"})


class JumpCRUD(InfluxdbCRUD):
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
            return []
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
        dataset = DatasetService(file.file, file.filename, user_id)
        df = dataset.create_jump_data()
        db_jump = JumpCreate(id=uuid4(), name=dataset.get_name(), user_id=user_id, data=df.to_json(default_handler=str, orient='records'))
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self.bucket, record=df, data_frame_measurement_name=db_jump.id, data_frame_tag_columns=['name', 'user_id'])
        write_api.__del__()
        return db_jump

    def delete_jump(self, jump_id: UUID):
        start = get_date_helper().to_utc(datetime(1970, 1, 1, 0, 0, 0, 0))
        stop = get_date_helper().to_utc(datetime(2200, 1, 1, 0, 0, 0, 0))
        self.client.delete_api().delete(start, stop, f'_measurement="{jump_id}"', bucket=f'{self.bucket}')
