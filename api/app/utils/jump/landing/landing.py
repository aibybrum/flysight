import peakutils as pu
import logging
from app.utils.jump.exit.exit import Exit

logging.basicConfig(level=logging.INFO)


class Landing:
    def __init__(self, df):
        self.df = df
        self.exit_df = Exit(df).get_exit_df()
        self.landing_df = self.exit_df.iloc[self.get_landing_index():].reset_index(drop=True)
    
    def get_landing_df(self):
        return self.landing_df
        
    # Get landing
    def get_landing_elevation(self):
        jmp_df = self.exit_df[self.exit_df.elevation <= 1200].reset_index()
        peaks = pu.indexes(jmp_df.elevation, thres=0.5, min_dist=0.1)
        lows = pu.indexes(-jmp_df.elevation, thres=0.1, min_dist=0.1)
        return {'start_landing': jmp_df, 'peaks': peaks, 'lows': lows}

    def get_landing_vert_speed(self):
        jmp_df = self.get_landing_elevation()['start_landing']
        peaks = pu.indexes(jmp_df.vert_speed_mph, thres=0.5, min_dist=0.1)
        lows = pu.indexes(-jmp_df.vert_speed_mph, thres=0.75, min_dist=5)
        
        lows_keys = [low for low in lows if low <= peaks[-1]]
        lows_values = [jmp_df.vert_speed_mph[low] for low in lows_keys]
        
        # landing_point is where the vertspeed is the lowest and start to increase
        return {'landing_point': lows_keys[lows_values.index(min(lows_values))], 'peaks': peaks, 'lows': lows}
    
    def get_landing(self):
        # change landing point if there is a dip in elevation
        elevation_low = self.get_landing_elevation()['lows'][0]
        vert_speed_low = self.get_landing_vert_speed()['landing_point']
        if elevation_low <= vert_speed_low:
            return elevation_low
        return vert_speed_low
    
    def get_landing_index(self):
        try:
            jmp_df = self.get_landing_elevation()['start_landing']
            return self.exit_df.index[self.exit_df['time'] == jmp_df.time[self.get_landing()]][0]
        except:
            logging.info(f'No high performance landing detected')
        
    # Get features of landing
    def get_stop(self):
        offset = 1.5
        horz_speed_peaks = pu.indexes(self.landing_df.horz_speed_mph, thres=0.1, min_dist=1)
        horz_speed_lows = pu.indexes(-self.landing_df.horz_speed_mph, thres=0.5, min_dist=1)
        return [l for l in horz_speed_lows if l > horz_speed_peaks[-1] and self.landing_df.horz_speed_mph[l] < offset][0]
    
    def get_top_of_turn(self):
        peaks = pu.indexes(self.landing_df.elevation, thres=0.01, min_dist=1)
        if len(peaks) == 0 or peaks[0] >= self.get_stop():
            return None
        return peaks[0]

    def get_max_horz_speed(self):
        return self.landing_df.idxmax().horz_speed_mph
