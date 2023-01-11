import os
import io
import dash
import base64
import logging
import pandas as pd
import plotly.graph_objects as go
from flysight.jump.jump import Jump

from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
app.title = 'Sw00pGenerator3000'

app.layout = html.Div(className="center", children=[
    html.Div(className="left", children=[
        html.Div(className="logo", children=[
            html.Div("SW00P", className="swoop"),
            html.Div("GENERATOR 3000", className="generator3000"),
        ]),  
        dcc.Upload(className='upload', children=html.Div([
            html.Div(className="upload-data", children=[
                    'Drop your file here, or ',
                    html.A('browse'),
                    html.Div('Support: .csv', className="support")
                ]),
            ]),
        ),
        html.Div(className="swoops", children=[
            #html.H2("Swoops"),
            html.Div(className="window", children=[
                dcc.RadioItems(
                    ['09-01-2023', '10-01-2023', '11-01-2023', '12-01-2023'], '09-01-2023',
                    inline=False, className="swoop", inputClassName="input_swoop", labelClassName="label_swoop"
                ),
            ]),
        ]),
        html.Div(className="yaxis", children=[
            html.H2("Y-axis"),
            dcc.Checklist(
                ['Elevation', 'Horizontal speed', 'Vertical speed', 'Dive angle'],
                ['Elevation', 'Horizontal speed', 'Vertical speed'], 
                className="y_check", inputClassName="input_y_check", labelClassName="label_y_check"
            )
        ]),
        html.Div(className="units", children=[
            html.H2("Units"),
            dcc.RadioItems(['km/u', 'mph'], 'km/u', className="units_radio", inputClassName="input_units_radio", labelClassName="label_units_radio"),
            dcc.RadioItems(['m', 'ft'], 'm', inputClassName="input_units_radio", labelClassName="label_units_radio"),
        ]),
        html.Div(className="save", children=[
            html.Button('Save graphs', id='save-val', n_clicks=0),
        ]),
    ]),
    html.Div(className="right", children=[
        html.Div(className="title", children=[
            html.H1("F@#k Ye4h!"),
            html.Div(className="line")
        ]),
        html.Div(className="metrics", children=[
            html.Div(className="metric elevation", children=[
                html.H3('493,58 feet', id='elevation'),
                html.Label('Elevation'),
            ]),
            html.Div(className="metric horz_speed", children=[
                html.H3('87,47 km/u', id='horz_speed'),
                html.Label('Horizontal speed'),
            ]),
            html.Div(className="metric vert_speed", children=[
                html.H3('112,66 km/u', id='vert_speed'),
                html.Label('Vertical speed'),
            ]),
            html.Div(className="metric dive_angle", children=[
                html.H3('40,10 °', id='dive_angle'),
                html.Label('Dive angle'),
            ]),
        ]),
        html.Div(className="graphs", children=[

        ]),
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True)

