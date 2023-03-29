import os
import numpy as np
import pandas as pd
import app.utils.dataset.helpers as helpers


class Dataset:
    def __init__(self, filename, df, user_id=None):
        self.filename = filename
        self.df = df
        self.user_id = user_id

    def get_total_seconds(self):
        datetimes = [pd.to_datetime(d) for d in self.df.time]
        l = []
        for i, d in enumerate(datetimes):
            duration = datetimes[i] - datetimes[0]
            l.append(duration.total_seconds())
        return l

    def get_fixed_elevation(self, elevation):
        ground_elevation = helpers.meters_to_feet(self.df.hMSL.iloc[-1])
        return [helpers.meters_to_feet(self.df.hMSL[i]) - ground_elevation - elevation for i in
                range(0, len(self.df.hMSL))]
        # return [helpers.meters_to_feet(self.df.hMSL[i]) - elevation for i in range(0, len(self.df.hMSL))]

    def get_vertical_speed(self, metric):
        if metric == 'mph':
            return [helpers.meter_per_second_to_miles_per_hour(meter) for meter in self.df.velD]
        elif metric == 'km/u':
            return [helpers.meter_per_second_to_kilometers_per_hour(meter) for meter in self.df.velD]
        else:
            raise ValueError('Invalid metric')

    def get_horizontal_speed(self, metric):
        speed = [helpers.calc_horizontal_speed(self.df.velN[i], self.df.velE[i]) for i in range(0, len(self.df))]
        if metric == 'mph':
            return [helpers.meter_per_second_to_miles_per_hour(s) for s in speed]
        elif metric == 'km/u':
            return [helpers.meter_per_second_to_kilometers_per_hour(s) for s in speed]
        else:
            raise ValueError('Invalid metric')

    def get_dive_angle(self, v_speed, h_speed):
        return [helpers.calc_dive_angle(v_speed[i], h_speed[i]) for i in range(0, len(self.df))]

    def get_horizontal_distance(self, metric):
        lis, dis = [0], 0.0
        for i in range(0, len(self.df) - 1):
            dis += helpers.calc_distance_geo(metric, self.df.lat[i], self.df.lat[i + 1], self.df.lon[i],
                                             self.df.lon[i + 1])
            lis.append(dis)
        return lis

    def get_axis_distance(self, metric, axis):
        x, y = helpers.calc_axis_distance(metric, self.df.lat, self.df.lon)
        axis_value = x if axis == 'x' else y
        lis, dis = [0], 0.0
        for i in range(0, len(axis_value) - 1):
            dis += axis_value[i + 1] - axis_value[i]
            lis.append(dis)
        return lis

    def create(self):
        df = pd.DataFrame({
            'timestamp': pd.to_datetime(self.df.time),
            'time_sec': np.array(self.get_total_seconds()),
            'lat': self.df.lat,
            'lon': self.df.lon,
            'elevation': self.get_fixed_elevation(0),
            'horz_distance_ft': self.get_horizontal_distance('ft'),
            'horz_distance_m': self.get_horizontal_distance('m'),
            'x_axis_distance_ft': self.get_axis_distance('ft', 'x'),
            'x_axis_distance_m': self.get_axis_distance('m', 'x'),
            'y_axis_distance_ft': self.get_axis_distance('ft', 'y'),
            'y_axis_distance_m': self.get_axis_distance('m', 'y'),
            'vert_speed_mph': self.get_vertical_speed('mph'),
            'horz_speed_mph': self.get_horizontal_speed('mph'),
            'vert_speed_km/u': self.get_vertical_speed('km/u'),
            'horz_speed_km/u': self.get_horizontal_speed('km/u'),
            'heading': self.df.heading,
            'dive_angle': self.get_dive_angle(self.get_vertical_speed('mph'), self.get_horizontal_speed('mph')),
            'name': self.get_name(),
            'user_id': self.user_id})
        df.set_index('timestamp', inplace=True)
        return df

    def get_name(self):
        return pd.to_datetime(self.df.time[0]).strftime("D%m-%d-%YT%H%M") + self.filename

    def save(self, path):
        dataframe = self.create()
        dataframe.to_csv(os.path.join(path, self.get_name() + '.csv'), index=False)

    def __str__(self):
        return f'{self.get_name()}'
