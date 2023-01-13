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
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
token = os.getenv("TOKEN")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Sw00pGenerator3000'

app.layout = html.Div([
    html.Div(children=[
        html.Div(children=[
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                },
            ),

            html.Label('Y-axis:', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                ['Elevation', 'Horizontal speed', 'Vertical speed', 'Dive angle'],
                ['Elevation', 'Horizontal speed', 'Vertical speed'],
                multi=True,
                id='y_drop',
            ),

            html.Label('Metrics:', style={'paddingTop': '2rem'}),
            html.Label('Speed:', style={'paddingTop': '1rem'}),
            dcc.Dropdown(['km/u', 'mph'], 'km/u', id='speed_metric'),

            html.Label('Distance:', style={'paddingTop': '1rem'}),
            dcc.Dropdown(['m', 'ft'], 'm', id='distance_metric'),
        ], style={
            'padding': '2rem',
            'margin': '1rem',
            'border-radius': '10px',
            'marginTop': '2rem',
            'width': '20%',
            'backgroundColor': 'white'
        }),
        html.Div(children=[
            dcc.Graph(
                id='first_graph',
            ),
        ], style={
            'border-radius': '10px',
            'width': '100%',
        }),
    ], style={
        'display': 'flex',
    }),
], style={
    'backgroundColor': 'white',
    'padding': '0',
    'margin': '0'
})


def parse_data(contents, filename):
    global df
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' or 'CSV' in filename:
            csv_file = pd.read_csv(io.StringIO(decoded.decode('utf-8')), skiprows=[1])
            df = Jump("test", csv_file)
    except Exception as e:
        logging.error(f"{e}")
        return html.Div([
            'There was an error processing this file.'
        ])
    return df


@app.callback(
    Output('first_graph', 'figure'),
    [
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename'),
        Input('y_drop', 'value'),
        Input('speed_metric', 'value'),
        Input('distance_metric', 'value')
    ])
def update_graph(contents, filename, selected, speed_metric, distance_metric):
    fig = {
        'layout': go.Layout(
            xaxis={"visible": True},
            yaxis={"visible": True},
            annotations=[
                {
                    "text": "Please upload file",
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

    if contents:
        jump = parse_data(contents, filename)
        landing_df = jump.get_landing_df()
        if len(selected) != 0:
            dic = jump.get_dic(speed_metric)
            d_metric = landing_df['horz_distance_m'] if distance_metric == "m" else landing_df['horz_distance_ft']

            plotly_data = []
            layout_kwargs = {'xaxis': {'domain': [0.06 * (len(selected) - 1), 1],
                                       'title': 'Horizontal distance (' + distance_metric + ')'}}

            for i, s in enumerate(selected):
                axis_name = 'yaxis' + str(i + 1) * (i > 0)
                yaxis = 'y' + str(i + 1) * (i > 0)
                plotly_data.append(go.Scatter(go.Scatter(
                    x=d_metric,
                    y=dic[s]['col'],
                    name=s,
                    mode='lines',
                    line=dict(color=dic[s]['color'], width=1.2),
                    showlegend=False,
                    hovertemplate=dic[s]['hovertemplate'],
                ),
                ))
                layout_kwargs[axis_name] = {
                    'position': i * 0.06, 'side': 'left', 'title': s + ' (' + dic[s]['metric'] + ')',
                    'titlefont': {'size': 10, 'color': dic[s]['color']}, 'title_standoff': 0,
                    'anchor': 'free', 'tickfont': {'size': 10, 'color': dic[s]['color']}, 'showgrid': False,
                }

                plotly_data[i]['yaxis'] = yaxis
                if i > 0:
                    layout_kwargs[axis_name]['overlaying'] = 'y'

            fig = go.Figure(data=plotly_data, layout=go.Layout(**layout_kwargs))
            fig.update_layout(hovermode="x unified")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

