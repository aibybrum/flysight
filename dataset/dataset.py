import numpy as np
import pandas as pd
import datetime as dt
import requests
import itertools
import dataset.helpers as helpers

class Dataset:
    def __init__(self, name, df, metrics):
        self.name = name
        self.df = df 
        self.metrics = metrics
        self.df_con = self.convert()

    def get_total_seconds(self):
        datetimes = [pd.to_datetime(d) for d in self.df.time]
        l = []
        for i, d in enumerate(datetimes):
            duration = datetimes[i] - datetimes[0]
            l.append(duration.total_seconds())
        return l

    def request_earth_elevation(self, x):
        s = "https://api.open-elevation.com/api/v1/lookup?locations="
        for i in range(x.index.start, x.index.stop): 
            s += str(x.lat[i]) + "," + str(x.lon[i]) + "|"
        r = requests.get(s[:-1]).json()
        elevation = pd.json_normalize(r, 'results')['elevation']
        return elevation
        
    def get_earth_elevation(self, metric):
        l = []
        divided_dataset = list(helpers.divide_dataset(self.df, 150))
        for i in range(0, len(divided_dataset)):
            l.append(self.request_earth_elevation(divided_dataset[i]).values)
        if metric == 'ft':
            return [helpers.meters_to_feet(e) for e in list(itertools.chain(*l))]
        elif metric == 'm':
            return list(itertools.chain(*l))

    def get_dynamic_elevation(self, metric):
        ground_elevation = helpers.meters_to_feet(self.df.hMSL.iloc[-1]) if metric == 'ft' else self.df.hMSL.iloc[-1]
        earth_elevation = self.get_earth_elevation(metric)
        l = []
        for i in range(0, len(self.df.hMSL)):
            if metric == 'ft':
                l.append(helpers.meters_to_feet(self.df.hMSL[i]) - ground_elevation - earth_elevation[i])
            elif metric == 'm':
                l.append(self.df.hMSL[i] - ground_elevation - earth_elevation[i])
        return l

    def get_fixed_elevation(self, elevation, metric):
        ground_elevation = helpers.meters_to_feet(self.df.hMSL.iloc[-1]) if metric == 'ft' else self.df.hMSL.iloc[-1]
        l = []
        for i in range(0, len(self.df.hMSL)):
            if metric == 'ft':
                l.append(helpers.meters_to_feet(self.df.hMSL[i]) - ground_elevation - elevation)
            elif metric == 'm':
                l.append(self.df.hMSL[i] - ground_elevation - elevation)
        return l

    def get_vertical_speed(self, metric='mph'):
        if metric == 'mph':
            return [helpers.meterpersecond_to_milesperhour(meter) for meter in self.df.velD]
        elif metric == 'km/u':
            return [helpers.meterpersecond_to_kilometersperhour(meter) for meter in self.df.velD]

    def get_horizontal_speed(self, metric='mph'):
        l = []
        for i in range(0,len(self.df)):
            speed = helpers.calc_horizontal_speed(self.df.velN[i], self.df.velE[i])
            if metric == 'mph':
                l.append(helpers.meterpersecond_to_milesperhour(speed))
            elif metric == 'km/u':
                l.append(helpers.meterpersecond_to_kilometersperhour(speed))
        return l

    def get_dive_angle(self, v_speed, h_speed):
        l = []
        for i in range(0, len(self.df)):
            l.append(helpers.calc_dive_angle(v_speed[i], h_speed[i]))
        return l

    def get_horizontal_distance(self, metric):
        l, f = [0], 0.0
        for i in range(0, len(self.df)-1):
            f += helpers.calc_distance(self.df.lat[i], self.df.lat[i+1], self.df.lon[i], self.df.lon[i+1], metric)
            l.append(f)
        return l

    def convert(self):
        return pd.DataFrame({'time': np.array(self.get_total_seconds()),
                            'lat': self.df.lat,
                            'lon': self.df.lon,
                            'dynamic_elevation': self.get_dynamic_elevation(self.metrics['height']),
                            'fixed_elevation': self.get_fixed_elevation(0, self.metrics['height']),
                            'horizontal_distance': self.get_horizontal_distance(self.metrics['height']),
                            'vertical_speed': self.get_vertical_speed(self.metrics['vel']),
                            'horizontal_speed': self.get_horizontal_speed(self.metrics['vel']),
                            'dive_angle': self.get_dive_angle(self.get_vertical_speed(), self.get_horizontal_speed())})

    def copy(self):
        self.df_con.to_csv(f'.\\data\\test-v1-{self.name}')

    def __str__ (self):
            return f'{self.name}: {self.df_con}'

    