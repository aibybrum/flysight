import numpy as np
import pandas as pd
import datetime as dt
import requests
import itertools
import dataset.helpers as helpers

class Dataset:
    def __init__(self, name, df, metrics={'height': 'ft', 'vel': 'km/u'}):
        self.name = name
        self.old_df = df 
        self.df = None
        self.metrics = self.set_metrics(metrics)
        
    def get_total_seconds(self):
        datetimes = [pd.to_datetime(d) for d in self.old_df.time]
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
        divided_dataset = list(helpers.divide_dataset(self.old_df, 150))
        l = [self.request_earth_elevation(divided_dataset[i]).values for i in range(0, len(divided_dataset))]
        if metric == 'ft':
            return [helpers.meters_to_feet(e) for e in list(itertools.chain(*l))]
        elif metric == 'm':
            return list(itertools.chain(*l))

    def get_dynamic_elevation(self, metric):
        ground_elevation = helpers.meters_to_feet(self.old_df.hMSL.iloc[-1]) if metric == 'ft' else self.old_df.hMSL.iloc[-1]
        earth_elevation = self.get_earth_elevation(metric)
        if metric == 'ft':
            return [helpers.meters_to_feet(self.old_df.hMSL[i]) - ground_elevation - earth_elevation[i] for i in range(0, len(self.old_df.hMSL))]
        elif metric == 'm':
            return [self.old_df.hMSL[i] - ground_elevation - earth_elevation[i] for i in range(0, len(self.old_df.hMSL))]
        else:
            raise ValueError('Invalid metric')

    def get_fixed_elevation(self, elevation, metric):
        ground_elevation = helpers.meters_to_feet(self.old_df.hMSL.iloc[-1]) if metric == 'ft' else self.old_df.hMSL.iloc[-1]
        if metric == 'ft':
            return [helpers.meters_to_feet(self.old_df.hMSL[i]) - ground_elevation - elevation for i in range(0, len(self.old_df.hMSL))]
        elif metric == 'm':
            return [self.old_df.hMSL[i] - ground_elevation - elevation for i in range(0, len(self.old_df.hMSL))]
        else:
            raise ValueError('Invalid metric')

    def get_vertical_speed(self, metric='mph'):
        if metric == 'mph':
            return [helpers.meterpersecond_to_milesperhour(meter) for meter in self.old_df.velD]
        elif metric == 'km/u':
            return [helpers.meterpersecond_to_kilometersperhour(meter) for meter in self.old_df.velD]
        else:
            raise ValueError('Invalid metric')

    def get_horizontal_speed(self, metric='mph'):
        speed = [helpers.calc_horizontal_speed(self.old_df.velN[i], self.old_df.velE[i]) for i in range(0, len(self.old_df))]
        if metric == 'mph':
            return [helpers.meterpersecond_to_milesperhour(s) for s in speed]
        elif metric == 'km/u':
            return [helpers.meterpersecond_to_kilometersperhour(s) for s in speed]
        else:
            raise ValueError('Invalid metric')

    def get_dive_angle(self, v_speed, h_speed):
        return [helpers.calc_dive_angle(v_speed[i], h_speed[i]) for i in range(0, len(self.old_df))]

    def get_horizontal_distance(self, metric):
        l, f = [0], 0.0
        for i in range(0, len(self.old_df)-1):
            f += helpers.calc_distance(self.old_df.lat[i], self.old_df.lat[i+1], self.old_df.lon[i], self.old_df.lon[i+1], metric)
            l.append(f)
        return l

    def update_df(self):
        return pd.DataFrame({
            'time': np.array(self.get_total_seconds()),
            'lat': self.old_df.lat,
            'lon': self.old_df.lon,
            'dynamic_elevation': self.get_dynamic_elevation(self.metrics['height']),
            'fixed_elevation': self.get_fixed_elevation(0, self.metrics['height']),
            'horizontal_distance': self.get_horizontal_distance(self.metrics['height']),
            'vertical_speed': self.get_vertical_speed(self.metrics['vel']),
            'horizontal_speed': self.get_horizontal_speed(self.metrics['vel']),
            'dive_angle': self.get_dive_angle(self.get_vertical_speed(), self.get_horizontal_speed())})
    
    def copy(self):
        self.df.to_csv(f'.\\data\\test-v1-{self.name}')

    def get_metrics(self):
        return self.metrics

    def set_metrics(self, value):
        if value['height'] == 'm' or value['height'] == 'ft':
            if value['vel'] == 'km/u' or value['vel'] == 'mph':
                self.metrics = value
                self.df = self.update_df()
        else: 
            raise ValueError('Invalid metric')

    def get_df(self):
        return self.df

    def __str__ (self):
            return f'{self.name}'

    