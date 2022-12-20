import helpers
import numpy as np
import peakutils as pu
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec

def get_skydive_elevation(dataframe):
    peaks = pu.indexes(dataframe.elevation, thres=0.9, min_dist=1)
    offset = peaks[-1] - 20 ## offset because the exit point can be to late to measure horz, vert speed
    jmp_df = dataframe.iloc[offset:].reset_index()
    return {'plane_on_altitude': jmp_df, 'peaks': peaks}
    
def get_skydive_horz_speed(dataframe):
    jmp_df = get_skydive_elevation(dataframe)['plane_on_altitude']
    # Get horz speed before exit / plane on attitude
    horz_speed_peaks = pu.indexes(jmp_df.horz_speed_mph, thres=0.5, min_dist=1)
    horz_speed_lows = pu.indexes(-jmp_df.horz_speed_mph, thres=0.5, min_dist=1)
    peak = [p for p in horz_speed_peaks if p < horz_speed_lows[0]]
    return {'plane_on_altitude': jmp_df, 'exit': peak[-1], 'peaks': horz_speed_peaks, 'lows': horz_speed_lows}

def get_skydive_vert_speed(dataframe):
    jmp_df = get_skydive_elevation(dataframe)['plane_on_altitude']
    # Get horz speed before exit / plane on attitude
    vert_speed_peaks = pu.indexes(jmp_df.vert_speed_mph, thres=0.5, min_dist=1)
    vert_speed_lows = pu.indexes(-jmp_df.vert_speed_mph, thres=0.5, min_dist=1)
    drop = [l for l in vert_speed_lows if l < vert_speed_peaks[0]]
    return {'plane_on_altitude': jmp_df, 'exit': drop[-1], 'peaks': vert_speed_peaks, 'lows': vert_speed_lows}

def get_exit(dataframe):
    jmp_df = get_skydive_elevation(dataframe)['plane_on_altitude']
    mean = np.mean([jmp_df.time[get_skydive_vert_speed(dataframe)['exit']], jmp_df.time[get_skydive_horz_speed(self.df)['exit']]])
    return dataframe.index[dataframe['time'] == helpers.closest_value(dataframe.time, mean)][0]

def plt_exit_point(dataframe):
    jmp_df = get_skydive_elevation(dataframe)['plane_on_altitude']
    
    gs = gridspec.GridSpec(2, 2)
    pl.figure(figsize=(15,10))
    
    ax = pl.subplot(gs[1, 0]) # row 0, col 0
    horz_speed = get_skydive_horz_speed(dataframe)
    
    pl.plot(jmp_df.time, jmp_df.horz_speed_mph)
    pl.axvline(x = jmp_df.time[horz_speed['exit']], color='grey', linestyle ="--")
    pl.plot(jmp_df.time[horz_speed['peaks']], jmp_df.horz_speed_mph[horz_speed['peaks']], marker="8", color='g', ls="")
    pl.plot(jmp_df.time[horz_speed['lows'][0]], jmp_df.horz_speed_mph[horz_speed['lows'][0]], marker="8", color='r', ls="")
    pl.title("Exit - Horizontal speed")
    pl.xlabel("Time (s)")
    pl.ylabel("Horizontal speed (mph)")

    ax = pl.subplot(gs[1, 1]) # row 0, col 1
    vert_speed = get_skydive_vert_speed(dataframe)
    
    pl.plot(jmp_df.time, jmp_df.vert_speed_mph)
    pl.axvline(x = jmp_df.time[vert_speed['exit']], color='grey', linestyle ="--")
    pl.plot(jmp_df.time[vert_speed['peaks'][0]], jmp_df.vert_speed_mph[vert_speed['peaks'][0]], marker="8", color='g', ls="")
    pl.plot(jmp_df.time[vert_speed['lows']], jmp_df.vert_speed_mph[vert_speed['lows']], marker="8", color='r', ls="")
    pl.title("Exit - Vertical speed")
    pl.xlabel("Time (s)")
    pl.ylabel("Vertical speed (mph)")

    ax = pl.subplot(gs[0, :]) # row 1, span all columns
    peaks = get_skydive_elevation(dataframe)['peaks']
    
    pl.plot(dataframe.time, dataframe.elevation)
    pl.axvline(x = dataframe.time[peaks[-1]], color='grey', linestyle ="--")
    pl.plot(dataframe.time[peaks], dataframe.elevation[peaks], marker="8", color='g', ls="")
    pl.title("Plane on altitude - Elevation")
    pl.xlabel("Time (s)")
    pl.ylabel("Elevation (feet)")