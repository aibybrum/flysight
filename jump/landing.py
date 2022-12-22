import numpy as np
import peakutils as pu
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class Landing:
    def __init__(self, df):
        self.df = df

    def get_landing(self):
        elevation_lows = pu.indexes(-self.df.elevation, thres=0.5, min_dist=1)
        # get last low point above 250 feet
        return [elevation_lows[i] for i in range(0, len(elevation_lows)) 
                if self.df.elevation[elevation_lows[i]] > 250][-1]