import numpy as np
import peakutils as pu


class ExitService:
    def __init__(self, df):
        self.df = df
        self.exit_df = self.df.iloc[self.get_exit():].reset_index(drop=True)

    def get_exit_elevation(self):
        peaks = pu.indexes(self.df.elevation, thres=0.9, min_dist=1)
        offset = peaks[-1] - 30
        jmp_df = self.df.iloc[offset:].reset_index()
        return {'plane_on_altitude': jmp_df, 'peaks': peaks}

    def get_exit_horz_speed(self):
        jmp_df = self.get_exit_elevation()['plane_on_altitude']
        horz_speed_peaks = pu.indexes(jmp_df.horz_speed_mph, thres=0.8, min_dist=2)
        horz_speed_lows = pu.indexes(-jmp_df.horz_speed_mph, thres=0.4, min_dist=2)
        peak = [p for p in horz_speed_peaks if p < horz_speed_lows[0]]
        return {'exit': peak[-1], 'peaks': horz_speed_peaks, 'lows': horz_speed_lows}

    def get_exit_vert_speed(self):
        jmp_df = self.get_exit_elevation()['plane_on_altitude']
        vert_speed_peaks = pu.indexes(jmp_df.vert_speed_mph, thres=0.4, min_dist=2)
        vert_speed_lows = pu.indexes(-jmp_df.vert_speed_mph, thres=0.8, min_dist=2)
        drop = [l for l in vert_speed_lows if l < vert_speed_peaks[0]]
        return {'exit': drop[-1], 'peaks': vert_speed_peaks, 'lows': vert_speed_lows}
    
    @staticmethod
    def closest_value(input_list, input_value):
        difference = lambda x: abs(x - input_value)
        res = min(input_list, key=difference)
        return res

    def get_exit(self):
        jmp_df = self.get_exit_elevation()['plane_on_altitude']
        mean = np.mean([jmp_df.time_sec[self.get_exit_vert_speed()['exit']], 
                        jmp_df.time_sec[self.get_exit_horz_speed()['exit']]])
        return self.df.index[self.df['time_sec'] == self.closest_value(self.df.time_sec, mean)][0]
    
    def get_exit_df(self):
        return self.exit_df
