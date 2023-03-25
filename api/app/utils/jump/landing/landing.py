import peakutils as pu

from api.app.services.jump import helpers
from api.app.services.jump.exit.exit import ExitService


class LandingService:

    def __init__(self, df):
        self.df = df
        self.exit_df = ExitService(df).get_exit_df()
        self.landing_df = self.exit_df.iloc[self.get_landing_index():].reset_index(drop=True)

    def get_landing_index(self):
        elevation_lows = pu.indexes(-self.exit_df.elevation, thres=0.5, min_dist=1)
        # get last low point above 250 feet
        return [elevation_lows[i] for i in range(0, len(elevation_lows))
                if self.exit_df.elevation[elevation_lows[i]] > 250][-1]

    def get_top_of_turn(self):
        return pu.indexes(self.landing_df.elevation, thres=0.01, min_dist=1)[0]

    def get_stop(self):
        offset = 1.5
        horz_speed_peaks = pu.indexes(self.landing_df.horz_speed_mph, thres=0.1, min_dist=1)
        horz_speed_lows = pu.indexes(-self.landing_df.horz_speed_mph, thres=0.5, min_dist=1)
        return [l for l in horz_speed_lows if l > horz_speed_peaks[-1] and self.landing_df.horz_speed_mph[l] < offset][
            0]

    def get_max_horz_speed(self):
        return self.landing_df.idxmax().horz_speed_mph

    def set_startpoint(self, startpoint):
        if startpoint == 'Start':
            self.landing_df = helpers.set_start_point(self.landing_df, 0)
        elif startpoint == 'Top of turn':
            self.landing_df = helpers.set_start_point(self.landing_df, self.get_top_of_turn())