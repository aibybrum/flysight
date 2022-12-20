import numpy as np
import pandas as pd
import datetime as dt
import requests
import itertools
import dataset.helpers as helpers
import dataset.exit as exit

class Dataset:
    def __init__(self, name, df):
        self.name = name
        self.old_df = df 
        self.df = self.update_df()
        
    def get_total_seconds(self):
        datetimes = [pd.to_datetime(d) for d in self.old_df.time]
        l = []
        for i, d in enumerate(datetimes):
            duration = datetimes[i] - datetimes[0]
            l.append(duration.total_seconds())
        return l

    def get_fixed_elevation(self, elevation):
        ground_elevation = helpers.meters_to_feet(self.old_df.hMSL.iloc[-1])
        return [helpers.meters_to_feet(self.old_df.hMSL[i]) - ground_elevation - elevation for i in range(0, len(self.old_df.hMSL))]

    def get_vertical_speed(self):
        return [helpers.meterpersecond_to_milesperhour(meter) for meter in self.old_df.velD]

    def get_horizontal_speed(self):
        speed = [helpers.calc_horizontal_speed(self.old_df.velN[i], self.old_df.velE[i]) for i in range(0, len(self.old_df))]
        return [helpers.meterpersecond_to_milesperhour(s) for s in speed]

    def get_dive_angle(self, v_speed, h_speed):
        return [helpers.calc_dive_angle(v_speed[i], h_speed[i]) for i in range(0, len(self.old_df))]

    def get_horizontal_distance(self):
        l, f = [0], 0.0
        for i in range(0, len(self.old_df)-1):
            f += helpers.calc_distance(self.old_df.lat[i], self.old_df.lat[i+1], self.old_df.lon[i], self.old_df.lon[i+1])
            l.append(f)
        return l

    def update_df(self):
        return pd.DataFrame({
            'time': np.array(self.get_total_seconds()),
            'lat': self.old_df.lat,
            'lon': self.old_df.lon,
            'elevation': self.get_fixed_elevation(0),
            'horz_d': self.get_horizontal_distance(),
            'vert_s': self.get_vertical_speed(),
            'horz_s': self.get_horizontal_speed(),
            'dive_angle': self.get_dive_angle(self.get_vertical_speed(), self.get_horizontal_speed())})


    def get_exit(self):
        return exit.get_exit(self.df)
    
    def copy(self):
        self.df.to_csv(f'.\\data\\test-v1-{self.name}')

    def get_df(self):
        return self.df

    def __str__ (self):
            return f'{self.name}'

    