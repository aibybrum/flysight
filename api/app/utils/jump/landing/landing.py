import peakutils as pu
import logging
from app.utils.jump.exit.exit import Exit

logging.basicConfig(level=logging.INFO)


class Landing:
    def __init__(self, df):
        self.start_elevation = 2000
        self.exit_df = Exit(df).get_exit_df()
        self.start_elevation_df = self.exit_df[self.exit_df.elevation <= self.start_elevation].reset_index(drop=True)

        if self.is_init_turn_detected():
            self.landing_df = self.start_elevation_df.iloc[self.get_init_turn():].reset_index(drop=True)
        else:
            logging.info("No high performance landing detected")
            
    def is_init_turn_detected(self):
        return self.get_init_turn() is not None

    def get_init_turn(self):
        landing_vert_speed = self.find_peaks_lows(self.start_elevation_df['vert_speed_km/u'], thres_peaks=0.5, min_dist_peaks=0.1, thres_lows=0.75, min_dist_lows=5)        
        # The initiated turn is where the vertspeed is the lowest and starts to increase
        lows_keys = [low for low in landing_vert_speed['lows'] if low <= landing_vert_speed['peaks'][-1]]
        lows_values = [self.start_elevation_df['vert_speed_km/u'][low] for low in lows_keys]
        if lows_values:
            return lows_keys[lows_values.index(min(lows_values))]
        return None

    def get_max_horz_speed_id(self):
        return self.landing_df.horz_speed_mph.idxmax() if hasattr(self, 'landing_df') else None

    def get_max_vert_speed_id(self):
        return self.landing_df.vert_speed_mph.idxmax() if hasattr(self, 'landing_df') else None

    def get_stop_estimate(self):
        offset = 1.5
        landing_horz_speed = self.find_peaks_lows(self.landing_df['horz_speed_km/u'], thres_peaks=0.1, min_dist_peaks=1, thres_lows=0.5, min_dist_lows=1)
        return [l for l in landing_horz_speed['lows'] if l > landing_horz_speed['peaks'][-1] and self.landing_df['horz_speed_km/u'][l] < offset][0]

    def get_rollout_estimate(self):
        landing_vert_speed = self.find_peaks_lows(self.landing_df['vert_speed_km/u'], thres_peaks=0.5, min_dist_peaks=0.1, thres_lows=0.75, min_dist_lows=5)        
        return landing_vert_speed['peaks'][-1]
    
    def get_landing_df(self):
        return self.landing_df
        # return self.landing_df if hasattr(self, 'landing_df') else None
    
    def find_peaks_lows(self, metric, thres_peaks, min_dist_peaks, thres_lows, min_dist_lows):
        peaks = pu.indexes(metric, thres=thres_peaks, min_dist=min_dist_peaks)
        lows = pu.indexes(-metric, thres=thres_lows, min_dist=min_dist_lows)
        return {'peaks': peaks, 'lows': lows}