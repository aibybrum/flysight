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
            html.H2("Sw00ps"),
            html.Div(className="window", children=[
                dcc.RadioItems(
                    ['09-01-2023', '10-01-2023', '11-01-2023', '12-01-2023', '13-01-2023', '14-01-2023'], '09-01-2023',
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
            html.H1("F@ck Yea#!"),
            html.Div(className="line")
        ]),
        html.Div(className="metrics", children=[
            html.Div(className="metric elevation", children=[
                html.Div('---,-- feet', className="first_title", id='elevation'),
                html.Div('Elevation', className="second_title"),
            ]),
            html.Div(className="metric horz_speed", children=[
                html.Div('---,-- km/u', className="first_title", id='horz_speed'),
                html.Div('Horizontal speed', className="second_title"),
            ]),
            html.Div(className="metric vert_speed", children=[
                html.Div('---,-- km/u', className="first_title", id='vert_speed'),
                html.Div('Vertical speed', className="second_title"),
            ]),
            html.Div(className="metric dive_angle", children=[
                html.Div('---,-- °', className="first_title", id='dive_angle'),
                html.Div('Dive angle', className="second_title"),
            ]),
        ]),
        html.Div(className="graphs", children=[
            html.Div(className="graph overview", children=[
                html.H2("Overview"),
                dcc.Graph(id='overview'),
            ]),
            html.Div(className="graph side_view_of_flight_path", children=[
                html.H2("Side view of flight path"),
                dcc.Graph(id='side_view_of_flight_path'),
            ]),
            html.Div(className="graph speed_during_swoop", children=[
                html.H2("Speed during swoop"),
                dcc.Graph(id='speed_during_swoop'),
            ]),
            html.Div(className="graph map", children=[
                html.H2("Map"),
                dcc.Graph(id='map'),
            ]),
        ]),
        html.Div(className="footer", children=[
            html.Div("© SWOOPGENERATOR3000 inc. 2023 - bram langmans", className="footer_text"),
        ]),
    ]),
])


@app.callback(Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def upload_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' or 'CSV' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            print(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


if __name__ == '__main__':
    app.run_server(debug=True)

