from dataclasses import dataclass

import logging
import numpy as np
import pandas as pd
import peakutils as pu
import plotly.graph_objects as go

# Helper functions for setting start point

def cumulative_sum(df: pd.Series, phase: str = '1', offset: float = 0.0) -> list:
    """Computes the cumulative sum of differences in a pandas Series."""
    lis, diff = [0.0], 0.0
    if phase == '2':
        lis[0] = round(offset, 6)
        diff = lis[0]
    for i in range(len(df) - 1):
        diff += df[i + 1] - df[i]
        lis.append(round(diff, 6))
    return lis

def shift_column(dataframe: pd.DataFrame, key: int, column_name: str) -> np.ndarray:
    """Shifts a DataFrame column based on the given key, recalculating values relative to the key."""
    if key < 0 or key >= len(dataframe):
        raise ValueError("Key must be between 0 and the length of the DataFrame.")
        
    first_part = dataframe.iloc[:key + 1][column_name][::-1].reset_index(drop=True)
    second_part = dataframe.iloc[key + 1:][column_name].reset_index(drop=True)
    offset = second_part.iloc[0] - first_part.iloc[0]
    
    shifted_first = cumulative_sum(first_part, phase='1')[::-1]
    shifted_second = cumulative_sum(second_part, phase='2', offset=offset)
    
    return np.concatenate((shifted_first, shifted_second))

def set_start_point(df: pd.DataFrame, key: int) -> pd.DataFrame:
    """Adjusts multiple columns in the DataFrame to start from a specific key."""
    adjusted_df = df.copy()

    columns_to_shift = [
        'time_sec', 'horz_distance_m', 'horz_distance_ft',
        'x_axis_distance_m', 'x_axis_distance_ft',
        'y_axis_distance_m', 'y_axis_distance_ft'
    ]

    for col in columns_to_shift:
        adjusted_df[col] = shift_column(df, key, col)
    
    return adjusted_df


# Helper functions for logging exceptions

def log_exceptions(func):
    """Decorator to log exceptions for wrapped functions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper


# Helper functions for finding threshold peaks and lows

@dataclass
class Threshold:
    """A class to represent threshold settings for peak and low detection."""
    thres_peaks: float
    min_dist_peaks: float
    thres_lows: float
    min_dist_lows: float

    def find_peaks_lows(self, metric: np.ndarray):
        """Detects peaks and lows in the provided metric using predefined thresholds."""
        peaks = pu.indexes(metric, thres=self.thres_peaks, min_dist=self.min_dist_peaks)
        lows = pu.indexes(-metric, thres=self.thres_lows, min_dist=self.min_dist_lows)
        return peaks, lows


# Helper functions for visualizations

def validate_metric(speed_metric: str, distance_metric: str):
    """Validates if the provided metrics are in the correct format."""
    if speed_metric not in ['km/u', 'mph']:
        raise ValueError("Invalid speed metric. Expected 'km/u' or 'mph'.")
    if distance_metric not in ['m', 'ft']:
        raise ValueError("Invalid distance metric. Expected 'm' or 'ft'.")

def get_column_or_none(df: pd.DataFrame, prefix: str, metric: str) -> pd.Series:
    """Retrieves a column from the DataFrame based on a prefix and metric."""
    column_name = f'{prefix}_{metric}'
    return df[column_name] if column_name in df.columns else None

def create_setting(name: str, col: pd.Series, color: str, metric: str, hovertemplate: str) -> dict:
    """Creates a dictionary of plot settings for a specific metric."""
    return {
        'col': col,
        'color': color,
        'metric': metric,
        'hovertemplate': hovertemplate
    }

def get_y_axis_settings(df: pd.DataFrame, speed_metric: str = 'km/u', distance_metric: str = 'm') -> dict:
    """Retrieves Y-axis plot settings for various metrics in the DataFrame."""
    validate_metric(speed_metric, distance_metric)
    settings = {}

    if 'elevation' in df.columns:
        elevation_col = df['elevation']
        settings['Elevation'] = create_setting('elevation', elevation_col, '#636EFA', 'ft', 'Elevation: %{y:.2f} ft <extra></extra>')

    horz_speed_col = get_column_or_none(df, 'horz_speed', speed_metric)
    if horz_speed_col is not None:
        settings['Horizontal speed'] = create_setting('horz_speed', horz_speed_col, '#FF0B0B', speed_metric, f'Horz speed: %{{y:.2f}} {speed_metric} <extra></extra>')

    distance_col = get_column_or_none(df, 'y_axis_distance', distance_metric)
    if distance_col is not None:
        settings['Distance'] = create_setting('y_axis_distance', distance_col, '#636EFA', distance_metric, f'y-axis distance: %{{y:.2f}} {distance_metric} <extra></extra>')

    if 'dive_angle' in df.columns:
        dive_angle_col = df['dive_angle']
        settings['Dive angle'] = create_setting('dive_angle', dive_angle_col, '#AB63FA', 'deg', 'Dive angle: %{y:.2f}° <extra></extra>')

    vert_speed_col = get_column_or_none(df, 'vert_speed', speed_metric)
    if vert_speed_col is not None:
        settings['Vertical speed'] = create_setting('vert_speed', vert_speed_col, '#00CC96', speed_metric, f'Vert speed: %{{y:.2f}} {speed_metric} <extra></extra>')

    return settings

def get_x_axis_settings(df: pd.DataFrame, speed_metric: str = 'km/u', distance_metric: str = 'm') -> dict:
    """Retrieves X-axis plot settings for various metrics in the DataFrame."""
    validate_metric(speed_metric, distance_metric)
    settings = {}

    if 'time_sec' in df.columns:
        time_col = df['time_sec']
        settings['Time'] = create_setting('time_sec', time_col, '#00CC96', 's', 'Time: %{y:.2f} s <extra></extra>')

    horz_distance_col = get_column_or_none(df, 'horz_distance', distance_metric)
    if horz_distance_col is not None:
        settings['Horizontal Distance'] = create_setting('horz_distance', horz_distance_col, '#636EFA', distance_metric, 'Horizontal Distance: %{y:.2f} ' + distance_metric + '<extra></extra>')

    x_axis_distance_col = get_column_or_none(df, 'x_axis_distance', distance_metric)
    if x_axis_distance_col is not None:
        settings['Distance'] = create_setting('x_axis_distance', x_axis_distance_col, '#AB63FA', distance_metric, 'x-axis distance: %{y:.2f} ' + distance_metric + '<extra></extra>')

    return settings

def get_metrics(df: pd.DataFrame, key: int, speed_metric: str) -> dict:
    """Retrieves metric values for a specific row in the DataFrame."""
    y_axis = get_y_axis_settings(df, speed_metric)
    return {
        'y_axis': {
            'values': [y_axis[col]['col'].loc[y_axis[col]['col'].index == key].values[0] for col in y_axis.keys()], 
            'metric': [y_axis[col]['metric'] for col in y_axis.keys()],
        },
    }

def empty_layout(text: str) -> dict:
    """Returns a layout with a centered annotation text."""
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
