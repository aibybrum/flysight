import numpy as np

'''
Set starting point of dataframe
'''


def cumulative_sum(df, fase='1', between=0.0):
    lis, diff = [0.0], 0.0
    if fase == '2':
        lis[0] = round(between, 6)
        diff = lis[0]
    for i in range(len(df) - 1):
        diff += df[i+1] - df[i]
        lis.append(round(diff, 6))
    return lis


def shift_df(dataframe, key, col):
    if key < 0:
        raise ValueError("key must be positive")
    if key >= len(dataframe):
        raise ValueError("key must be less than the length of dataframe")
    first = dataframe.iloc[:key+1][col][::-1].reset_index(drop=True)
    second = dataframe.iloc[key+1:][col].reset_index(drop=True)
    between = second.iloc[0] - first.iloc[0]
    return np.concatenate((cumulative_sum(first, fase='1')[::-1], cumulative_sum(second, fase='2', between=between)))


def set_start_point(df, key):
    df2 = df.copy()
    df2['time_sec'] = shift_df(df2, key, 'time_sec')
    df2['horz_distance_m'] = shift_df(df2, key, 'horz_distance_m')
    df2['horz_distance_ft'] = shift_df(df2, key, 'horz_distance_ft')
    df2['x_axis_distance_m'] = shift_df(df2, key, 'x_axis_distance_m')
    df2['x_axis_distance_ft'] = shift_df(df2, key, 'x_axis_distance_ft')
    df2['y_axis_distance_m'] = shift_df(df2, key, 'y_axis_distance_m')
    df2['y_axis_distance_ft'] = shift_df(df2, key, 'y_axis_distance_ft')
    return df2


'''
Find peaks and lows
'''


def find_peaks_lows(metric, thres_peaks, min_dist_peaks, thres_lows, min_dist_lows):
    peaks = pu.indexes(metric, thres=thres_peaks, min_dist=min_dist_peaks)
    lows = pu.indexes(-metric, thres=thres_lows, min_dist=min_dist_lows)
    return {'peaks': peaks, 'lows': lows}