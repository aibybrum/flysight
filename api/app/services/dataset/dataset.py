import os
import numpy as np
import pandas as pd
import app.services.dataset.helpers as helpers


class DatasetService:
    def __init__(self, file, filename, user_id=None):
        self.file = file
        self.filename = filename
        self.user_id = user_id
        self.df = self.read_csv()

    def read_csv(self):
        try:
            df = pd.read_csv(self.file, skiprows=[1])
        except Exception as e:
            try:
                df = pd.read_csv(self.file, skiprows=7, header=None)
                df = df.drop(df.columns[0], axis=1)
                df.columns = ['time', 'lat', 'lon', 'hMSL', 'velN', 'velE', 'velD', 'hAcc', 'vAcc', 'sAcc', 'numSV']
            except Exception as e:
                df = None
        return df

    def get_total_seconds(self):
        datetimes = [pd.to_datetime(d) for d in self.df.time]
        l = []
        for i, d in enumerate(datetimes):
            duration = datetimes[i] - datetimes[0]
            l.append(duration.total_seconds())
        return l

    def get_dynamic_elevation(self):
        ground_elevation = helpers.meters_to_feet(self.df.hMSL.iloc[-1]) # last point in data is the ground estimation point
        return [helpers.meters_to_feet(self.df.hMSL[i]) - ground_elevation for i in range(0, len(self.df.hMSL))]

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
            dis += helpers.calc_distance_geo(metric, self.df.lat[i], self.df.lat[i + 1], self.df.lon[i], self.df.lon[i + 1])
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

    def create_jump_data(self):
        if self.df is not None: 
            df = pd.DataFrame({
                'timestamp': pd.to_datetime(self.df.time),
                'time_sec': np.array(self.get_total_seconds()),
                'lat': self.df.lat,
                'lon': self.df.lon,
                'elevation': self.get_dynamic_elevation(),
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
                'dive_angle': self.get_dive_angle(self.get_vertical_speed('mph'), self.get_horizontal_speed('mph')),
                'name': self.get_name(),
                'user_id': self.user_id})
            df.set_index('timestamp', inplace=True)
            return df
        else: 
            logging.error("dataframe is None type")
            raise Exception("dataframe is None type")

    def create_pond_data(self):
        if self.df is not None: 
            df = pd.DataFrame({
                'timestamp': pd.to_datetime(self.df.time),
                'time_sec': np.array(self.get_total_seconds()),
                'lat': self.df.lat,
                'lon': self.df.lon,
                'horz_speed_mph': self.get_horizontal_speed('mph'),
                'horz_speed_km/u': self.get_horizontal_speed('km/u')
            })
            df.set_index('timestamp', inplace=True)
            return df
        else: 
            logging.error("dataframe is None type")
            raise Exception("dataframe is None type")

    def get_name(self):
        return pd.to_datetime(self.df.time[0]).strftime("D%m-%d-%YT%H%M") + self.filename

    def __str__(self):
        return f'{self.get_name()}'