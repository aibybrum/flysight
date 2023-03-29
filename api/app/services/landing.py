from uuid import UUID
from api.app.services.main import InfluxdbService
from api.app.utils.jump.jump import Jump
from api.app.schemas.landing import Landing, Data, LandingParams, Location, Distance, Speed


class LandingCRUD(InfluxdbService):
    def get_df(self, jump_id: UUID):
        query = f'from(bucket: "{self.bucket}") |> range(start: 0) ' \
                f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") ' \
                f'|> filter(fn: (r) => r._measurement == "{jump_id}")'
        df = self.client.query_api().query_data_frame(query=query)
        if not df.empty:
            jump = Jump(df.drop(['result', 'table', '_start', '_stop', '_time', '_measurement', 'name', 'user_id'], axis=1))
            return df['name'][0], jump
        return None


class LandingService(LandingCRUD):
    def get_landing(self, jump_id: UUID):
        name, jump = self.get_df(jump_id)
        landing_df = jump.get_landing_df()
        if landing_df.empty:
            return None

        return Landing(
            name=name,
            data=Data(
                params=LandingParams(
                    top_of_turn=jump.get_top_of_turn(),
                    max_horz_speed=jump.get_max_horz_speed(),
                    stop=jump.get_max_horz_speed(),
                ),
                time=landing_df['time_sec'].values.tolist(),
                location=Location(lat=landing_df['lat'].values.tolist(), lon=landing_df['lon'].values.tolist()),
                elevation=landing_df['elevation'].values.tolist(),
                distance=Distance(
                    horizontal={'ft': landing_df['horz_distance_ft'].values.tolist(),
                                'm': landing_df['horz_distance_m'].values.tolist()},
                    x_axis={'ft': landing_df['x_axis_distance_ft'].values.tolist(),
                            'm': landing_df['x_axis_distance_m'].values.tolist()},
                    y_axis={'ft': landing_df['y_axis_distance_ft'].values.tolist(),
                            'm': landing_df['y_axis_distance_m'].values.tolist()}
                ),
                speed=Speed(
                    horizontal={'km/u': landing_df['horz_speed_km/u'].values.tolist(),
                                'mph': landing_df['horz_speed_mph'].values.tolist()},
                    vertical={'km/u': landing_df['vert_speed_km/u'].values.tolist(),
                              'mph': landing_df['vert_speed_mph'].values.tolist()}
                ),
                dive_angle=landing_df['dive_angle'].values.tolist(),
                heading=landing_df['heading'].values.tolist(),
            ),
        )

