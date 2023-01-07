import numpy as np


def set_start_point(df, key):
    df2 = df.copy()
    df2.time = shift_df(df2, key, 'time')
    df2.horz_distance = shift_df(df2, key, 'horz_distance')
    return df2


def shift_df(dataframe, key, col):
    k = dataframe.iloc[:key][::-1][col].reset_index()
    k.iloc[:-1] *= -1
    j = [round(s + k[col][0], 4) for s in dataframe.iloc[key:][col]]
    return np.concatenate((k[col], j))