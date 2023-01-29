import os
import io
import dash
import base64
import pandas as pd
import glob
import dash_bootstrap_components as dbc
import plotly.io as pio
from flysight.jump.jump import Jump
from flysight.dataset.dataset import Dataset
import flysight.jump.helpers as helpers

from dash import dcc, html
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

themes = ["plotly_white", "plotly_dark", "ggplot2", "simple_white"]
pio.templates.default = themes[0]

load_dotenv()
path = os.getenv("DES_PATH")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Sw00pGenerator3000'

swoops = [os.path.split(file)[1].split('.')[0] for file in glob.glob(path + '*.csv')]

app.layout = html.Div(className="center", children=[
    html.Div(className="left", children=[
        html.Div(className="logo", children=[
            html.Div("SW00P", className="swoop"),
            html.Div("GENERATOR 3000", className="generator3000"),
        ]),
        dcc.Upload(id='upload', className='upload', children=html.Div([
            html.Div(className="upload-data", children=[
                'Drop your file here, or ',
                html.A('browse'),
                html.Div('Support: .csv', className="support")
            ]),
            html.Div(id="hidden-div"),
        ])),
        html.Div(className="swoops", children=[
            html.H2("Sw00ps"),
            html.Div(className="window", children=[
                dcc.RadioItems(
                    swoops,
                    id="swoops",
                    inline=False, className="swoop", inputClassName="input_swoop", labelClassName="label_swoop"
                ),
                dcc.Store(id='storage')
                # html.Div(id="storage"),
            ]),
        ]),
        html.Div(className="yaxis", children=[
            html.H2("Y-axis"),
            dcc.Checklist(
                ['Elevation', 'Horizontal speed', 'Vertical speed', 'Dive angle'],
                ['Elevation', 'Horizontal speed', 'Vertical speed'],
                className="y_check", inputClassName="input_y_check", labelClassName="label_y_check", id="y_axis"
            )
        ]),
        html.Div(className="units", children=[
            html.H2("Units"),
            dcc.RadioItems(['km/u', 'mph'], 'km/u', className="units_radio", inputClassName="input_units_radio",
                           labelClassName="label_units_radio", id="speed_metric"),
            dcc.RadioItems(['m', 'ft'], 'm', inputClassName="input_units_radio", labelClassName="label_units_radio",
                           id="distance_metric"),
        ]),
        html.Div(className="save", children=[
            html.Button('Save graphs', id='save-val', n_clicks=0),
        ]),
    ]),
    html.Div(className="right", children=[
        html.Div(className="title", children=[
            html.H1(id="dashboard_title"),
            html.Div(className="line")
        ]),
        html.Div(className="metrics", children=[
            html.Div(className="metric elevation", children=[
                html.Div(className="first_title", id='elevation'),
                html.Div('Elevation', className="second_title"),
            ]),
            html.Div(className="metric horz_speed", children=[
                html.Div(className="first_title", id='horz_speed'),
                html.Div('Horizontal speed', className="second_title"),
            ]),
            html.Div(className="metric vert_speed", children=[
                html.Div(className="first_title", id='vert_speed'),
                html.Div('Vertical speed', className="second_title"),
            ]),
            html.Div(className="metric dive_angle", children=[
                html.Div(className="first_title", id='dive_angle'),
                html.Div('Dive angle', className="second_title"),
            ]),
        ]),
        html.Div(className="graphs", children=[
            dbc.Row(dbc.Col(
                html.Div(className="graph overview", children=[
                    dcc.Graph(id='overview')
                ]),
            )),
            dbc.Row([
                dbc.Col(
                    html.Div(className="graph overhead", children=[
                        dcc.Graph(id='overhead')
                    ]),
                    width=5
                ),
                dbc.Col(
                    html.Div(className="graph map", children=[
                        dcc.Graph(id='map')
                    ]),
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(className="graph side_view_of_flight_path", children=[
                        dcc.Graph(id='side_view_of_flight_path'),
                    ]),
                    width=5
                ),
                dbc.Col(
                    html.Div(className="graph speed_during_swoop", children=[
                        dcc.Graph(id='speed_during_swoop'),
                    ]),
                ),
            ]),
            dbc.Collapse(
                dbc.Row([
                    dbc.Col(
                        html.Div(className="graph debug_elevation", children=[
                            dcc.Graph(id='debug_elevation'),
                        ]),
                    ),
                    dbc.Col(
                        html.Div(className="graph debug_horz_speed", children=[
                            dcc.Graph(id='debug_horz_speed'),
                        ]),
                    ),
                    dbc.Col(
                        html.Div(className="graph debug_vert_speed", children=[
                            dcc.Graph(id='debug_vert_speed'),
                        ]),
                    ),
                ]),
            ),
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
        Output('debug_elevation', 'figure'),
        Output('debug_horz_speed', 'figure'),
        Output('debug_vert_speed', 'figure')
    ],
    [
        Input('storage', 'data'),
        Input('y_axis', 'value'),
        Input('speed_metric', 'value'),
        Input('distance_metric', 'value')
    ]
)
def plt_graphs(df, y_axis, speed_metric, distance_metric):
    empty = helpers.empty_layout("Please select Sw00p")
    if df is not None:
        jump = Jump(df[0], pd.read_json(df[1], orient="split"))

        jump.set_landing_df(helpers.set_start_point(jump.get_landing_df(), jump.get_top_of_turn()))

        return [jump.plt_overview(y_axis, speed_metric, distance_metric),
                jump.plt_overhead(distance_metric),
                jump.plt_side_view(distance_metric),
                jump.plt_speed(speed_metric, distance_metric),
                jump.plt_map(),
                jump.debug('Elevation', speed_metric, distance_metric),
                jump.debug('Horizontal speed', speed_metric, distance_metric),
                jump.debug('Vertical speed', speed_metric, distance_metric)]
    return [empty] * 8


@app.callback(
    [
        Output("elevation", "children"),
        Output("horz_speed", "children"),
        Output("vert_speed", "children"),
        Output("dive_angle", "children"),
    ],
    [
        Input('storage', 'data'),
        Input("overview", "hoverData"),
        Input('speed_metric', 'value')
    ]
)
def hover_overview(df, hover_data, speed_metric):
    if df is not None and hover_data is not None:
        jump = Jump(df[0], pd.read_json(df[1], orient="split"))
        hover_id = hover_data["points"][0]['pointIndex']
        metrics = helpers.get_metrics(jump.get_landing_df(), hover_id, speed_metric)

        return [f"{ round(metrics['y_axis']['values'][0], 2) } { metrics['y_axis']['metric'][0] }",
                f"{ round(metrics['y_axis']['values'][1], 2) } { metrics['y_axis']['metric'][1] }",
                f"{ round(metrics['y_axis']['values'][2], 2) } { metrics['y_axis']['metric'][2] }",
                f"{ round(metrics['y_axis']['values'][3], 2) } { metrics['y_axis']['metric'][3] }"]
    return ['---,--'] * 4


@app.callback(
    Output('swoops', 'options'),
    Input('upload', 'contents'),
    State('upload', 'filename'))
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
                    dataset.save()
                    swoops.insert(0, dataset.get_name())
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
    return [{'label': s, 'value': s} for s in swoops[::-1]]


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
