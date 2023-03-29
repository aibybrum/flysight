import numpy as np
import peakutils as pu

from app.utils.jump.exit import helpers


class Exit:
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
        mean = np.mean([jmp_df.time_sec[self.get_skydive_vert_speed()['exit']], jmp_df.time_sec[self.get_skydive_horz_speed()['exit']]])
        return self.df.index[self.df['time_sec'] == helpers.closest_value(self.df.time_sec, mean)][0]
