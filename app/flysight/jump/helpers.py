import numpy as np
import plotly.graph_objects as go


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
    df2['time'] = shift_df(df2, key, 'time')
    df2['horz_distance_m'] = shift_df(df2, key, 'horz_distance_m')
    df2['horz_distance_ft'] = shift_df(df2, key, 'horz_distance_ft')
    df2['x_axis_distance_m'] = shift_df(df2, key, 'x_axis_distance_m')
    df2['x_axis_distance_ft'] = shift_df(df2, key, 'x_axis_distance_ft')
    df2['y_axis_distance_m'] = shift_df(df2, key, 'y_axis_distance_m')
    df2['y_axis_distance_ft'] = shift_df(df2, key, 'y_axis_distance_ft')
    return df2


'''
Graphs settings
'''


def validate_metric(speed_metric, distance_metric):
    if speed_metric not in ['km/u', 'mph']:
        raise ValueError("Wrong speed metric")
    elif distance_metric not in ['m', 'ft']:
        raise ValueError("Wrong distance metric")


def get_metrics(df, hover_id, speed_metric):
    y_axis = get_y_axis_settings(df, speed_metric)
    return {
        'y_axis':
        {
            'values': [y_axis[col]['col'].loc[y_axis[col]['col'].index == hover_id].values[0] for col in y_axis.keys()],
            'metric': [y_axis[col]['metric'] for col in y_axis.keys()],
        },

    }


def get_y_axis_settings(df, speed_metric='km/u', distance_metric='m'):
    validate_metric(speed_metric, distance_metric)
    return {
        'Elevation':
        {
            'col': df.elevation,
            'color': '#057DE5',
            'metric': "ft",
            'hovertemplate': 'Elevation: %{y:.2f} ft <extra></extra>'
        },
        'Horizontal speed':
        {
            'col': df['horz_speed_km/u'] if speed_metric == 'km/u' else df['horz_speed_mph'],
            'color': '#FC6481',
            'metric': speed_metric,
            'hovertemplate': 'Horz speed: %{y:.2f} ' + speed_metric + '<extra></extra>'
        },
        'Vertical speed':
        {
            'col': df['vert_speed_km/u'] if speed_metric == 'km/u' else df['vert_speed_mph'],
            'color': '#38D996',
            'metric': speed_metric,
            'hovertemplate': 'Vert speed: %{y:.2f} ' + speed_metric + '<extra></extra>'
        },
        'Dive angle':
        {
            'col': df.dive_angle,
            'color': '#D36EC6',
            'metric': 'deg',
            'hovertemplate': 'Dive angle: %{y:.2f}° <extra></extra>'
        },
        'Distance':
        {
            'col': df['y_axis_distance_m'] if distance_metric == "m" else df['y_axis_distance_ft'],
            'color': '#057DE5',
            'metric': distance_metric,
            'hovertemplate': 'yaxis distance: %{y:.2f} ' + distance_metric + '<extra></extra>'
        },
    }


def get_x_axis_settings(df, speed_metric='km/u', distance_metric='m'):
    validate_metric(speed_metric, distance_metric)
    return {
        'Time':
        {
            'col': df.time,
            'metric': 's'
        },
        'Horizontal Distance':
        {
            'col': df['horz_distance_m'] if distance_metric == "m" else df['horz_distance_ft'],
            'metric': distance_metric
        },
        'Distance':
        {
            'col': df['x_axis_distance_m'] if distance_metric == "m" else df['x_axis_distance_ft'],
            'metric': distance_metric
        }
    }


def empty_layout(text):
    return {
        'layout': go.Layout(
            xaxis={"visible": True},
            yaxis={"visible": True},
            annotations=[
                {
                    "text": text,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
    }