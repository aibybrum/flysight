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
        html.Div(className="yaxis", children=[
            html.H2("Y-axis"),
            dcc.Dropdown(
                ['Elevation', 'Horizontal speed', 'Vertical speed', 'Dive angle'],
                ['Elevation', 'Horizontal speed', 'Vertical speed'],
                multi=True, id='y_drop',
            ),
        ]),
        html.Div(className="units", children=[
            html.H2("Units"),
            dcc.Dropdown(['km/u', 'mph'], 'km/u', id='speed_metric'),
            dcc.Dropdown(['m', 'ft'], 'm', id='distance_metric'),
        ]),
        html.Div(className="swoops", children=[
            html.H2("Swoops"),
            html.Div(className="check", children=[
                dcc.RadioItems(
                    ['09-01-2023', '10-01-2023', '11-01-2023', '12-01-2023'], '09-01-2023',
                    inline=False, className="item", inputClassName="itemke"
                ),
            ]),
        ]),
        html.Div(className="save", children=[
            html.Button('Save graphs', id='save-val', n_clicks=0),
        ]),
    ]),
    html.Div(className="right", children=[
        html.Div(className="title", children=[
            html.H1("Dashboard"),
            html.Div(className="line")
        ]),
        
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True)
