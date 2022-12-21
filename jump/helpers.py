import numpy as np

def shift_df(dataframe, key, col):
    k = dataframe.iloc[:key][::-1][col].reset_index()
    k.iloc[:-1] *= -1
    j = [round(s + k[col][0], 4) for s in dataframe.iloc[key:][col]]
    return np.concatenate((k[col], j))