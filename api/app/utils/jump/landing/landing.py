import peakutils as pu
import logging
from app.utils.jump.exit.exit import Exit
from app.utils.jump import helpers

logging.basicConfig(level=logging.DEBUG)


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
        landing_vert_speed = helpers.find_peaks_lows(self.start_elevation_df['vert_speed_km/u'], thres_peaks=0.5, min_dist_peaks=0.1, thres_lows=0.75, min_dist_lows=5)        
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
        landing_horz_speed = helpers.find_peaks_lows(self.landing_df['horz_speed_km/u'], thres_peaks=0.1, min_dist_peaks=1, thres_lows=0.5, min_dist_lows=1)
        return [l for l in landing_horz_speed['lows'] if l > landing_horz_speed['peaks'][-1] and self.landing_df['horz_speed_km/u'][l] < offset][0]

    def get_start_rollout_estimate(self):
        landing_vert_speed = helpers.find_peaks_lows(self.landing_df['vert_speed_km/u'], thres_peaks=0.5, min_dist_peaks=0.1, thres_lows=0.75, min_dist_lows=0.1)
        last_peak_index = landing_vert_speed['peaks'][-1]

        diff = np.insert(np.diff(np.diff(self.landing_df['horz_distance_m'])), 0, 0)
        landing_horz_dis = pu.indexes(diff, thres=0.2, min_dist=0.1)

        for index in landing_horz_dis:
            if index >= last_peak_index:
                return index
        return None
    
    def get_stop_rollout_estimate(self):
        landing_vert_speed = helpers.find_peaks_lows(self.landing_df['vert_speed_km/u'], thres_peaks=0.5, min_dist_peaks=0.1, thres_lows=0.75, min_dist_lows=0.1)
        peaks = landing_vert_speed['peaks']
        lows = landing_vert_speed['lows']

        if len(peaks) > 0:
            first_low_after_last_peak = next((low for low in lows if low > peaks[-1]), None)
            if first_low_after_last_peak is not None:
                return first_low_after_last_peak
        return None

    def get_time_to_execute_turn(self):
        return f"{round(self.landing_df.time[self.get_start_rollout_estimate()] - self.landing_df.time[0], 1)} sec"
    
    def get_time_during_rollout(self):
        return f"{round(self.landing_df.time[self.get_stop_rollout_estimate()] - self.landing_df.time[self.get_start_rollout_estimate()], 1)} sec"
    
    def get_time_aloft_during_swoop(self):
        return f"{round(self.landing_df.time[self.get_stop_estimate()] - self.landing_df.time[self.get_stop_rollout_estimate()], 1)} sec"
    
    def set_start_point(self):
        key = self.get_stop_rollout_estimate()
        if key < 0 or key >= len(self.landing_df):
            raise ValueError("Invalid key for setting the starting point")
        self.landing_df = helpers.set_start_point(self.landing_df, key)

    def get_landing_df(self):
        return self.landing_df if hasattr(self, 'landing_df') else None