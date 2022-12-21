import pandas as pd
import numpy as np
import exit.exit as exit
import dataset.dataset as dataset
import landing.landing as landing
import matplotlib.pyplot as plt
import helpers

class Jump:
    def __init__(self, name, df):
        self.name = name
        self.df = dataset.Dataset(df).create()
        self.exit = exit.Exit(self.df)
        self.landing = landing.Landing(self.df)

    def set_start_point(self, key):
        df2 = self.df.copy()
        df2.time = helpers.shift_df(df2, key, 'time')
        df2.horz_distance = helpers.shift_df(df2, key, 'horz_distance')
        return df2

    def get_df(self):
        return self.df

    def set_name(self, name):
        self.name = name

    def __str__ (self):
        return f'{self.name}'

def main():
    data = pd.read_csv('././data/J1.csv', skiprows=[1])
    df = Jump("v1", data)

    #df.landing.set_df(df.set_start_point(df.landing.get_landing()))
    df.landing.debug_plt()
    df.landing.plt()
    
    
if __name__ == "__main__":
    main()