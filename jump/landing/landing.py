import numpy as np
import peakutils as pu
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class Landing:
    def __init__(self, df):
        self.df = df

    def set_df(self, df):
        self.df = df

    def get_landing(self):
        elevation_lows = pu.indexes(-self.df.elevation, thres=0.5, min_dist=1)
        # get last low point above 250 feet
        return [elevation_lows[i] for i in range(0, len(elevation_lows)) 
                if self.df.elevation[elevation_lows[i]] > 250][-1]

    def debug_plt(self): 
        df = self.df.copy()
        df = df.iloc[self.get_landing():]
        gs = gridspec.GridSpec(2, 2)
        pl.figure(figsize=(15,10))

        # Elevation
        ax = pl.subplot(gs[0, :]) # row 1, span all columns
        l_elevation_peaks = pu.indexes(df.elevation, thres=0.5, min_dist=1)
        l_elevation_lows = pu.indexes(-df.elevation, thres=0.5, min_dist=1)

        pl.plot(df.horz_distance, df.elevation)
        pl.plot(df.horz_distance[l_elevation_peaks], df.elevation[l_elevation_peaks], marker="8", color='g', ls="")
        pl.plot(df.horz_distance[l_elevation_lows], df.elevation[l_elevation_lows], marker="8", color='r', ls="")  
        pl.title("Landing - Elevation")

        # Horizontal Speed
        ax = pl.subplot(gs[1, 0]) # row 0, col 0
        l_horz_speed_mph_peaks = pu.indexes(df.horz_speed_mph, thres=0.5, min_dist=1)
        l_horz_speed_mph_lows = pu.indexes(-df.horz_speed_mph, thres=0.1, min_dist=1)

        l_horz_lim_lows = [l for l in l_horz_speed_mph_lows if l > l_horz_speed_mph_peaks[-1]]

        pl.plot(df.horz_distance, self.df.horz_speed_mph)
        pl.plot(df.horz_distance[l_horz_speed_mph_peaks], df.horz_speed_mph[l_horz_speed_mph_peaks], marker="8", color='g', ls="")
        pl.plot(df.horz_distance[l_horz_lim_lows[0]], df.horz_speed_mph[l_horz_lim_lows[0]], marker="8", color='r', ls="")
        pl.title("Landing - Horizontal speed")


        # Vertical Speed
        ax = pl.subplot(gs[1, 1]) # row 0, col 1
        l_vert_speed_mph_peaks = pu.indexes(df.vert_speed_mph, thres=0.5, min_dist=1)
        l_vert_speed_mph_lows = pu.indexes(-df.vert_speed_mph, thres=0.5, min_dist=1)

        l_vert_lim_lows = [l for l in l_vert_speed_mph_lows if l > l_vert_speed_mph_peaks[-1]]

        pl.plot(df.horz_distance, df.vert_speed_mph)
        pl.plot(df.horz_distance[l_vert_speed_mph_peaks], df.vert_speed_mph[l_vert_speed_mph_peaks], marker="8", color='g', ls="")
        pl.plot(df.horz_distance[l_vert_lim_lows[0]], df.vert_speed_mph[l_vert_lim_lows[0]], marker="8", color='r', ls="")
        pl.title("Landing - Vertical speed")

    def plt(self):
        df = self.df.copy()
        df = df.iloc[self.get_landing():]
        fig, ax = plt.subplots(figsize=(15,8))
        fig.subplots_adjust(right=0.75)

        twin1 = ax.twinx()
        twin2 = ax.twinx()

        twin2.spines.right.set_position(("axes", 1.08))

        p1, = ax.plot(df.horz_distance, df.elevation, "b", label="Elevation")
        p2, = twin1.plot(df.horz_distance, df.horz_speed_mph, "r", label="Horz speed")
        p3, = twin2.plot(df.horz_distance, df.vert_speed_mph, "g", label="Vert speed")

        ax.set_xlabel("Distance (feet)")
        ax.set_ylabel("Elevation (feet)")
        twin1.set_ylabel("Horizontal speed (mph)")
        twin2.set_ylabel("Vertical speed (mph)")

        ax.yaxis.label.set_color(p1.get_color())
        twin1.yaxis.label.set_color(p2.get_color())
        twin2.yaxis.label.set_color(p3.get_color())

        tkw = dict(size=4, width=1.5)
        ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
        twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
        twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
        ax.tick_params(axis='x', **tkw)

        ax.legend(handles=[p1, p2, p3])
        plt.show()