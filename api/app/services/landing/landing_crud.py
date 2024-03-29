import numpy as np
from uuid import UUID

from app.services.influxdb_service import InfluxDBService


class LandingCRUD(InfluxDBService):
    def get_dataset(self, jump_id: UUID):
        query = f'from(bucket: "{self.bucket}") |> range(start: 0) ' \
                f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") ' \
                f'|> filter(fn: (r) => r._measurement == "{jump_id}")'
        df = self.client.query_api().query_data_frame(query=query)
        if not df.empty:
            return df['name'][0], df.drop(['result', 'table', '_start', '_stop', '_time', '_measurement', 'name', 'user_id'], axis=1)
        return None
