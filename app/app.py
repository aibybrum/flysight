import os
import io
import dash
import base64
import flask
import pandas as pd
import glob
import dash_bootstrap_components as dbc
import plotly.io as pio
from flysight.jump.jump import Jump
from flysight.dataset.dataset import Dataset
import flysight.jump.helpers as helpers

from dash import dcc, html
from dash.dependencies import Input, Output, State

themes = ["plotly_white", "plotly_dark", "ggplot2", "simple_white"]
pio.templates.default = themes[0]

path = "/data/"

server = flask.Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME], server=server)
app.title = 'Sw00pGenerator3000'

swoops = [os.path.split(file)[1].split('.')[0] for file in glob.glob(path + '*.csv')]

app.layout = html.Div(className="center", children=[
    html.Div(className="left", children=[
        html.Div(className="logo", children=[
            html.Div("SW", className="swoop"),
            html.Div("GEN3", className="generator3000"),
        ]),
        html.Div(className="menu", children=[

        ]),
    ]),
    html.Div(className="right", children=[
        html.Div(className="toolbar", children=[
            html.Div(className="title", children=[
                html.H1('F@ck Yea#!', id="dashboard_title"),
            ]),
            html.Div(className="searchbar", children=[
                dbc.Input(placeholder="Search..", type="text", id="searchbar"),
            ]),
            html.Div(className="save", children=[
                html.Button('Save graphs', id='save-val', n_clicks=0),
            ]),
        ]),
        html.Div(className="settings", children=[
            html.Div(className="setting swoops", children=[
                html.Div('Sw00ps', className="first_title"),
                dcc.Dropdown([{'label': s, 'value': s} for s in swoops[::-1]], className="dropdown", id='swoops',  placeholder="Jumps"),
                dcc.Upload(id='upload_swoops', className='upload', children=html.Div([
                    html.Div(className="upload-data", children=[
                        'Drop your file here, or ',
                        html.A('browse'),
                    ]),
                ])),
                dcc.Store(id='storage')
            ]),
            html.Div(className="setting ponds", children=[
                html.Div('Ponds', className="first_title"),
                dcc.Dropdown([], className="dropdown", id='ponds',  placeholder="Ponds"),
                dcc.Upload(id='upload_ponds', className='upload', children=html.Div([
                    html.Div(className="upload-data", children=[
                        'Drop your file here, or ',
                        html.A('browse'),
                    ]),
                ])),
            ]),
            html.Div(className="setting units", children=[
                html.Div('Units', className="first_title"),
                dcc.RadioItems(['km/u', 'mph'], 'km/u', className="units_radio", inputClassName="input_units_radio", labelClassName="label_units_radio", id="speed_metric"),
                dcc.RadioItems(['m', 'ft'], 'm', className="units_radio", inputClassName="input_units_radio", labelClassName="label_units_radio", id="distance_metric"),
            ]),
            html.Div(className="setting startpoint", children=[
                html.Div('Startpoint', className="first_title"),
                dcc.RadioItems(['Start', 'Top of turn', 'Roll out', 'Entry gate'], 'Start', className="startpoint_radio", inputClassName="input_startpoint_radio", labelClassName="label_startpoint_radio", id="startpoint"),
            ]),
        ]),
        html.Div(className="graphs", children=[
            dbc.Row(dbc.Col(
                html.Div(className="graph overview", children=[
                    html.Div(className="graph_title", children=[
                        html.Div(className="line"),
                        html.H2('Overview'),
                    ]),
                    html.Div(className="yaxis", children=[
                        dcc.Checklist(
                            ['Elevation', 'Horizontal speed', 'Vertical speed', 'Dive angle'],
                            ['Elevation', 'Horizontal speed', 'Vertical speed'],
                            className="y_check", inputClassName="input_y_check", labelClassName="label_y_check", id="y_axis"
                        ),
                    ]),
                    dcc.Graph(id='overview', config={'displayModeBar':False})
                ]),
            )),
            dbc.Row([
                dbc.Col(
                    html.Div(className="graph overhead", children=[
                        html.Div(className="graph_title", children=[
                            html.Div(className="line"),
                            html.H2('Overhead view of flight path'),
                        ]),
                        dcc.Graph(id='overhead')
                    ]),
                    width=5
                ),
                dbc.Col(
                    html.Div(className="graph map", children=[
                        dcc.Graph(id='map', config={'displayModeBar':False})
                    ]),
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(className="graph side_view_of_flight_path", children=[
                        html.Div(className="graph_title", children=[
                            html.Div(className="line"),
                            html.H2('Side view of flight path'),
                        ]),
                        dcc.Graph(id='side_view_of_flight_path'),
                    ]),
                    width=5
                ),
                dbc.Col(
                    html.Div(className="graph speed_during_swoop", children=[
                        html.Div(className="graph_title", children=[
                            html.Div(className="line"),
                            html.H2('Speed during swoop'),
                        ]),
                        dcc.Graph(id='speed_during_swoop'),
                    ]),
                ),
            ]),
        ]),
        html.Div(className="footer", children=[
            html.Div("© SWOOPGENERATOR3000 inc. 2023 - bram langmans", className="footer_text"),
        ]),
    ]),
])

@app.callback(
    [
        Output('dashboard_title', 'children'),
        Output('storage', 'data'),
    ],
    Input('swoops', 'value'),
)
def select_jump(value):
    title = 'F@ck Yea#!'
    if value is not None:
        df = pd.read_csv(os.path.join(path, str(value) + '.csv'))
        return [f'{title}, {value}', [value, df.to_json(orient="split")]]
    return [title, None]


@app.callback(
    [
        Output('overview', 'figure'),
        Output('overhead', 'figure'),
        Output('side_view_of_flight_path', 'figure'),
        Output('speed_during_swoop', 'figure'),
        Output('map', 'figure'),
    ],
    [
        Input('storage', 'data'),
        Input('y_axis', 'value'),
        Input('speed_metric', 'value'),
        Input('distance_metric', 'value'),
        Input('startpoint', 'value')
    ]
)
def plt_graphs(df, y_axis, speed_metric, distance_metric, startpoint):
    empty = helpers.empty_layout("Please select Sw00p")
    if df is not None:
        jump = Jump(df[0], pd.read_json(df[1], orient="split"))
        jump.set_startpoint(startpoint)
        return [jump.plt_overview(y_axis, speed_metric, distance_metric),
                jump.plt_overhead(distance_metric),
                jump.plt_side_view(distance_metric),
                jump.plt_speed(speed_metric, distance_metric),
                jump.plt_map()]
    return [empty] * 5


@app.callback(
    Output('swoops', 'options'),
    Input('upload_swoops', 'contents'),
    State('upload_swoops', 'filename'))
def upload_file(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if '.csv' or '.CSV' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), skiprows=[1])
                name = filename.rsplit('.', 1)[0]
                dataset = Dataset(name, df)
                if dataset.get_name() not in swoops:
                    dataset.save(path)
                    swoops.insert(0, dataset.get_name())
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
    return [{'label': s, 'value': s} for s in swoops[::-1]]


if __name__ == '__main__':
    app.run_server()
