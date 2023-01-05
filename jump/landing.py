import numpy as np
import peakutils as pu
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import plotly.express as px
import os
from exit import Exit
from dotenv import load_dotenv
import helpers

load_dotenv()

token = os.getenv("TOKEN")

class Landing():
    def __init__(self, df):
        self.df = df
        self.exit_df = Exit(df).get_exit_df()
        self.landing_df = self.exit_df.iloc[self.get_landing():].reset_index(drop=True)
        
    def get_landing(self):
        elevation_lows = pu.indexes(-self.exit_df.elevation, thres=0.5, min_dist=1)
        # get last low point above 250 feet
        return [elevation_lows[i] for i in range(0, len(elevation_lows)) 
                if self.exit_df.elevation[elevation_lows[i]] > 250][-1]

    def plt_landing_point(self):
        # Test for gettting the landing
        gs = gridspec.GridSpec(2, 2)
        pl.figure(figsize=(15,10))

        # Elevation
        ax = pl.subplot(gs[0, :]) # row 1, span all columns
        elevation_peaks = pu.indexes(self.exit_df.elevation, thres=0.01, min_dist=1)
        elevation_lows = pu.indexes(-self.exit_df.elevation, thres=0.5, min_dist=1)

        pl.plot(self.exit_df.time, self.exit_df.elevation)
        pl.axvline(x = self.exit_df.time[self.get_landing()], color='grey', linestyle ="--")
        pl.plot(self.exit_df.time[elevation_peaks], self.exit_df.elevation[elevation_peaks], marker="8", color='g', ls="")
        pl.plot(self.exit_df.time[elevation_lows], self.exit_df.elevation[elevation_lows], marker="8", color='r', ls="")  
        pl.title("Landing - Elevation")
        pl.xlabel("Time (s)")
        pl.ylabel("Elevation (feet)")
            
        # Horizontal Speed
        ax = pl.subplot(gs[1, 0]) # row 0, col 0
        horz_speed_mph_peaks = pu.indexes(self.exit_df.horz_speed_mph, thres=0.5, min_dist=2)
        horz_speed_mph_lows = pu.indexes(-self.exit_df.horz_speed_mph, thres=0.5, min_dist=2)

        horz_lim_peaks = horz_speed_mph_peaks[-3:]
        horz_lim_lows = [l for l in horz_speed_mph_lows if l > horz_lim_peaks[0] and l < horz_lim_peaks[-1]]

        pl.plot(self.exit_df.time, self.exit_df.horz_speed_mph)
        pl.plot(self.exit_df.time[horz_lim_peaks], self.exit_df.horz_speed_mph[horz_lim_peaks], marker="8", color='g', ls="")
        pl.plot(self.exit_df.time[horz_lim_lows], self.exit_df.horz_speed_mph[horz_lim_lows], marker="8", color='r', ls="")
        pl.axvline(x = self.exit_df.time[self.get_landing()], color='grey', linestyle ="--")
        pl.title("Landing - Horizontal speed")
        pl.xlabel("Time (s)")
        pl.ylabel("Horizontal speed (mph)")

        # Vertical Speed
        ax = pl.subplot(gs[1, 1]) # row 0, col 1
        vert_speed_mph_peaks = pu.indexes(self.exit_df.vert_speed_mph, thres=0.2, min_dist=2)
        vert_speed_mph_lows = pu.indexes(-self.exit_df.vert_speed_mph, thres=0.5, min_dist=2)

        vert_lim_peaks = vert_speed_mph_peaks[-3:]
        vert_lim_lows = [l for l in vert_speed_mph_lows if l > vert_lim_peaks[0] and l < vert_lim_peaks[-1]]

        pl.plot(self.exit_df.time, self.exit_df.vert_speed_mph)
        pl.plot(self.exit_df.time[vert_lim_peaks], self.exit_df.vert_speed_mph[vert_lim_peaks], marker="8", color='g', ls="")
        pl.plot(self.exit_df.time[vert_lim_lows], self.exit_df.vert_speed_mph[vert_lim_lows], marker="8", color='r', ls="")
        pl.axvline(x = self.exit_df.time[self.get_landing()], color='grey', linestyle ="--")
        pl.title("Landing - Vertical speed")
        pl.xlabel("Time (s)")
        pl.ylabel("Vertical speed (mph)")

        pl.show()


    def save_landing(self, name):
        self.landing_df.to_csv(f'././data/landing/{name}.csv', index=False) 