import json
from uuid import UUID, uuid4
from api.app.services.main import InfluxdbService
from api.app.utils.jump.jump import Jump
from api.app.schemas.landing import Landing, Data


class LandingCRUD(InfluxdbService):
    def get_df(self, jump_id: UUID):
        query = f'from(bucket: "{self.bucket}") |> range(start: 0) ' \
                f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") ' \
                f'|> filter(fn: (r) => r._measurement == "{jump_id}")'
        df = self.client.query_api().query_data_frame(query=query)
        if not df.empty:
            jump_df = df.drop(['result', 'table', '_start', '_stop', '_time', '_measurement', 'name', 'user_id'], axis=1)
            return df, jump_df
        return None


class LandingService(LandingCRUD):
    def get_landing(self, jump_id: UUID):
        df, jump_df = self.get_df(jump_id)

        if df.empty and jump_df.empty:
            return None

        jump = Jump(jump_df)

        json_str = jump.get_landing_df().to_json(orient="records")
        data = json.loads(json_str)

        return Landing(
            id=df['_measurement'][0],
            name=df['name'][0],
            user_id=df['user_id'][0],
            data=Data(
                top_of_turn=jump.get_top_of_turn(),
                max_horz_speed=jump.get_max_horz_speed(),
                stop=jump.get_stop(),
                dataframe=data
            )
        )

