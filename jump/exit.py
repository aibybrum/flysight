import numpy as np
import peakutils as pu
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import helpers 

class Exit():
    def __init__(self, df):
        self.df = df
        self.exit_df = self.df.iloc[self.get_exit():].reset_index(drop=True)
        # self.exit_df = helpers.set_start_point(self.df, self.get_exit()).iloc[self.get_exit():].reset_index()
        
    def get_exit_df(self):
        return self.exit_df

    # Get exit point
    def get_skydive_elevation(self):
        peaks = pu.indexes(self.df.elevation, thres=0.9, min_dist=1)
        # offset because the exit point can be to late to measure horz, vert speed
        offset = peaks[-1] - 20
        jmp_df = self.df.iloc[offset:].reset_index()
        return {'plane_on_altitude': jmp_df, 'peaks': peaks}
        
    def get_skydive_horz_speed(self):
        jmp_df = self.get_skydive_elevation()['plane_on_altitude']
        # Get horz speed before exit / plane on attitude
        horz_speed_peaks = pu.indexes(jmp_df.horz_speed_mph, thres=0.5, min_dist=1)
        horz_speed_lows = pu.indexes(-jmp_df.horz_speed_mph, thres=0.5, min_dist=1)
        peak = [p for p in horz_speed_peaks if p < horz_speed_lows[0]]
        return {'plane_on_altitude': jmp_df, 'exit': peak[-1], 'peaks': horz_speed_peaks, 'lows': horz_speed_lows}

    def get_skydive_vert_speed(self):
        jmp_df = self.get_skydive_elevation()['plane_on_altitude']
        # Get horz speed before exit / plane on attitude
        vert_speed_peaks = pu.indexes(jmp_df.vert_speed_mph, thres=0.5, min_dist=1)
        vert_speed_lows = pu.indexes(-jmp_df.vert_speed_mph, thres=0.5, min_dist=1)
        drop = [l for l in vert_speed_lows if l < vert_speed_peaks[0]]
        return {'plane_on_altitude': jmp_df, 'exit': drop[-1], 'peaks': vert_speed_peaks, 'lows': vert_speed_lows}

    def get_exit(self):
        jmp_df = self.get_skydive_elevation()['plane_on_altitude']
        mean = np.mean([jmp_df.time[self.get_skydive_vert_speed()['exit']], jmp_df.time[self.get_skydive_horz_speed()['exit']]])
        return self.df.index[self.df['time'] == helpers.closest_value(self.df.time, mean)][0]

    # Visualistions
    def plt_exit_point(self):
        jmp_df = self.get_skydive_elevation()['plane_on_altitude']
        
        gs = gridspec.GridSpec(2, 2)
        pl.figure(figsize=(15,10))
        
        ax = pl.subplot(gs[1, 0]) # row 0, col 0
        horz_speed = self.get_skydive_horz_speed()
        
        pl.plot(jmp_df.time, jmp_df.horz_speed_mph)
        pl.axvline(x = jmp_df.time[horz_speed['exit']], color='grey', linestyle ="--")
        pl.plot(jmp_df.time[horz_speed['peaks']], jmp_df.horz_speed_mph[horz_speed['peaks']], marker="8", color='g', ls="")
        pl.plot(jmp_df.time[horz_speed['lows'][0]], jmp_df.horz_speed_mph[horz_speed['lows'][0]], marker="8", color='r', ls="")
        pl.title("Exit - Horizontal speed")
        pl.xlabel("Time (s)")
        pl.ylabel("Horizontal speed (mph)")

        ax = pl.subplot(gs[1, 1]) # row 0, col 1
        vert_speed = self.get_skydive_vert_speed()
        
        pl.plot(jmp_df.time, jmp_df.vert_speed_mph)
        pl.axvline(x = jmp_df.time[vert_speed['exit']], color='grey', linestyle ="--")
        pl.plot(jmp_df.time[vert_speed['peaks'][0]], jmp_df.vert_speed_mph[vert_speed['peaks'][0]], marker="8", color='g', ls="")
        pl.plot(jmp_df.time[vert_speed['lows']], jmp_df.vert_speed_mph[vert_speed['lows']], marker="8", color='r', ls="")
        pl.title("Exit - Vertical speed")
        pl.xlabel("Time (s)")
        pl.ylabel("Vertical speed (mph)")

        ax = pl.subplot(gs[0, :]) # row 1, span all columns
        peaks = self.get_skydive_elevation()['peaks']
        
        pl.plot(self.df.time, self.df.elevation)
        pl.axvline(x = self.df.time[peaks[-1]], color='grey', linestyle ="--")
        pl.plot(self.df.time[peaks], self.df.elevation[peaks], marker="8", color='g', ls="")
        pl.title("Plane on altitude - Elevation")
        pl.xlabel("Time (s)")
        pl.ylabel("Elevation (feet)")

        pl.show()

    def plt_exit(self):
        fig, ax = plt.subplots(figsize=(15,8))
        fig.subplots_adjust(right=0.75)

        twin1 = ax.twinx()
        twin2 = ax.twinx()

        twin2.spines.right.set_position(("axes", 1.08))

        p1, = ax.plot(self.exit_df.horz_distance_m, self.exit_df.elevation, "b", label="Elevation")
        p2, = twin1.plot(self.exit_df.horz_distance_m, self.exit_df.horz_speed_mph, "r", label="Horz speed")
        p3, = twin2.plot(self.exit_df.horz_distance_m, self.exit_df.vert_speed_mph, "g", label="Vert speed")

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

    def save_exit(self, name):
        self.exit_df.to_csv(f'././data/exit/{name}.csv', index=False) 