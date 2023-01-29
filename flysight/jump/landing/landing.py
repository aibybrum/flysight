import os
import peakutils as pu
import plotly.graph_objects as go
from dotenv import load_dotenv
from flysight.jump.exit.exit import Exit
import flysight.jump.helpers as helpers

load_dotenv()
token = os.getenv("TOKEN")


class Landing:
    def __init__(self, df):
        self.df = df
        self.exit_df = Exit(df).get_exit_df()
        self.landing_df = self.exit_df.iloc[self.get_landing():].reset_index(drop=True)
        
    def get_landing(self):
        elevation_lows = pu.indexes(-self.exit_df.elevation, thres=0.5, min_dist=1)
        # get last low point above 250 feet
        return [elevation_lows[i] for i in range(0, len(elevation_lows)) 
                if self.exit_df.elevation[elevation_lows[i]] > 250][-1]

    def get_top_of_turn(self):
        return pu.indexes(self.landing_df.elevation, thres=0.01, min_dist=1)[0]

    def get_stop(self):
        offset = 1.5
        horz_speed_peaks = pu.indexes(self.landing_df.horz_speed_mph, thres=0.1, min_dist=1)
        horz_speed_lows = pu.indexes(-self.landing_df.horz_speed_mph, thres=0.5, min_dist=1)
        return [l for l in horz_speed_lows if l > horz_speed_peaks[-1] and self.landing_df.horz_speed_mph[l] < offset][0]

    def get_max_horz_speed(self):
        return self.landing_df.idxmax().horz_speed_mph

    def get_landing_df(self):
        return self.landing_df

    def set_landing_df(self, df):
        self.landing_df = df

    def save_landing(self, name):
        self.landing_df.to_csv(f'././data/landing/{name}.csv', index=False)

    def plt_overview(self, selected, speed_metric, distance_metric):
        if len(selected) != 0:
            x_axis = helpers.get_x_axis_settings(self.landing_df, distance_metric=distance_metric)
            y_axis = helpers.get_y_axis_settings(self.landing_df, speed_metric=speed_metric)

            plotly_data = []
            layout_kwargs = {'xaxis': {'domain': [0.06 * (len(selected) - 1), 1],
                                       'title': 'Horizontal distance (' + distance_metric + ')'}}

            for i, s in enumerate(selected):
                axis_name = 'yaxis' + str(i + 1) * (i > 0)
                yaxis = 'y' + str(i + 1) * (i > 0)
                plotly_data.append(go.Scatter(
                    x=x_axis['Horizontal Distance']['col'],
                    y=y_axis[s]['col'],
                    name=s,
                    mode='lines',
                    line=dict(color=y_axis[s]['color'], width=1.2),
                    showlegend=False,
                    hovertemplate=y_axis[s]['hovertemplate'],
                ),
                )
                layout_kwargs[axis_name] = {
                    'position': i * 0.06, 'side': 'left', 'title': s + ' (' + y_axis[s]['metric'] + ')',
                    'titlefont': {'size': 10, 'color': y_axis[s]['color']}, 'title_standoff': 0,
                    'anchor': 'free', 'tickfont': {'size': 10, 'color': y_axis[s]['color']}, 'showgrid': False,
                }

                plotly_data[i]['yaxis'] = yaxis
                if i > 0:
                    layout_kwargs[axis_name]['overlaying'] = 'y'

            fig = go.Figure(data=plotly_data, layout=go.Layout(**layout_kwargs))
            fig.update_layout(
                hovermode="x unified"
            )
            return fig
        else:
            return helpers.empty_layout("Please select Y-axis")

    def plt_overhead(self, distance_metric):
        x_axis = helpers.get_x_axis_settings(self.landing_df, distance_metric=distance_metric)
        y_axis = helpers.get_y_axis_settings(self.landing_df, distance_metric=distance_metric)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis['Distance']['col'],
            y=y_axis['Distance']['col'],
            line=dict(color=y_axis['Distance']['color'], width=1.2),
            hovertemplate=y_axis['Distance']['hovertemplate'],
            showlegend=False,
            
        ))
        fig.update_layout(hovermode='x unified', title='Overhead view of flight path',
                          legend=dict(yanchor="top", y=1, xanchor="right", x=1))
        fig.update_xaxes(title=f"X-axis distance ({x_axis['Distance']['metric']})")
        fig.update_yaxes(title=f"Y-axis distance ({y_axis['Distance']['metric']})")
        return fig

    def plt_side_view(self, distance_metric):
        x_axis = helpers.get_x_axis_settings(self.landing_df, distance_metric=distance_metric)
        y_axis = helpers.get_y_axis_settings(self.landing_df)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis['Horizontal Distance']['col'].iloc[:self.get_stop()+1],
            y=y_axis['Elevation']['col'].iloc[:self.get_stop()+1],
            name='Elevation',
            line=dict(color=y_axis['Elevation']['color'], width=1.2),
            hovertemplate=y_axis['Elevation']['hovertemplate'],
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[x_axis['Horizontal Distance']['col'][self.get_top_of_turn()]],
            y=[y_axis['Elevation']['col'][self.get_top_of_turn()]],
            name='Top of turn',
            text=['Top of turn'],
            textposition='top right',
            hovertemplate='Top of turn: %{y:.2f}' + y_axis['Elevation']['metric'] + ' <extra></extra>',
            mode='markers+text',
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[x_axis['Horizontal Distance']['col'][self.get_stop()]],
            y=[y_axis['Elevation']['col'][self.get_stop()]],
            name='Stop',
            text=['stop'],
            textposition='top left',
            hovertemplate='Stop: %{y:.2f}' + x_axis['Distance']['metric'] + ' <extra></extra>',
            mode='markers+text',
            showlegend=False
        ))
        fig.update_layout(hovermode='x unified', title='Side view of flight path',
                          legend=dict(yanchor="top", y=1, xanchor="right", x=1))
        fig.update_xaxes(title=f"Horizontal distance ({x_axis['Horizontal Distance']['metric']})")
        fig.update_yaxes(title=f"Elevation ({y_axis['Elevation']['metric']})")

        return fig

    def plt_speed(self, speed_metric, distance_metric):
        x_axis = helpers.get_x_axis_settings(self.landing_df, distance_metric=distance_metric)
        y_axis = helpers.get_y_axis_settings(self.landing_df, speed_metric=speed_metric)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis['Horizontal Distance']['col'].iloc[self.get_max_horz_speed():self.get_stop() + 1],
            y=y_axis['Horizontal speed']['col'].iloc[self.get_max_horz_speed():self.get_stop() + 1],
            line=dict(color=y_axis['Horizontal speed']['color'], width=1.2),
            hovertemplate=y_axis['Horizontal speed']['hovertemplate'],
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[x_axis['Horizontal Distance']['col'].iloc[self.get_max_horz_speed()]],
            y=[y_axis['Horizontal speed']['col'][self.get_max_horz_speed()]],
            name=f"max horz speed ({round(y_axis['Horizontal speed']['col'][self.get_max_horz_speed()], 2)} {y_axis['Horizontal speed']['metric']})",
            text=["Max Horz Speed"],
            textposition="top right",
            hovertemplate='max horz speed: %{y:.2f}' + y_axis['Horizontal speed']['metric'] + ' <extra></extra>',
            mode='markers+text'
        ))
        fig.add_trace(go.Scatter(
            x=[x_axis['Horizontal Distance']['col'].iloc[self.get_stop()]],
            y=[y_axis['Horizontal speed']['col'][self.get_stop()]],
            text=['stop'],
            textposition='top left',
            hovertemplate='Stop: %{y:.2f}' + x_axis['Horizontal Distance']['metric'] + ' <extra></extra>',
            mode='markers+text',
            showlegend=False
        ))

        fig.update_layout(hovermode='x unified', title='Speed during swoop',
                          legend=dict(yanchor="top", y=1, xanchor="right", x=1))
        fig.update_xaxes(title=f"Horizontal distance ({x_axis['Horizontal Distance']['metric']})")
        fig.update_yaxes(title=f"Horizontal speed ({y_axis['Horizontal speed']['metric']})")
        return fig

    def plt_map(self):
        df = self.landing_df.iloc[:self.get_stop() + 1].reset_index(drop=True)
        y_axis = helpers.get_y_axis_settings(df)

        fig = go.Figure()

        fig.add_trace(go.Scattermapbox(
            lat=df.lat,
            lon=df.lon,
            mode='lines',
            line=dict(color=y_axis['Elevation']['color']),
            showlegend=False,
        ))

        fig.add_trace(go.Scattermapbox(
            lat=[df.lat[self.get_top_of_turn()]],
            lon=[df.lon[self.get_top_of_turn()]],
            name='Top of turn',
            textposition='top right',
            mode='markers',
        ))

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(yanchor="top", y=1, xanchor="right", x=1),
            mapbox=dict(
                accesstoken=token,
                style="satellite-streets",
                center=go.layout.mapbox.Center(
                    lat=df.lat[round(len(df) / 2)],
                    lon=df.lon[round(len(df) / 2)]
                ),
                pitch=0,
                zoom=15.5
            )
        )
        return fig

    def debug(self, yaxis, speed_metric='km/u', distance_metric='m'):
        x_axis = helpers.get_x_axis_settings(self.landing_df, distance_metric=distance_metric)
        y_axis = helpers.get_y_axis_settings(self.landing_df, speed_metric=speed_metric)

        vert_speed_peaks = pu.indexes(y_axis[yaxis]['col'], thres=0.5, min_dist=1)
        vert_speed_lows = pu.indexes(-y_axis[yaxis]['col'], thres=0.5, min_dist=1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis['Distance']['col'],
            y=y_axis[yaxis]['col'],
            name=yaxis,
            line=dict(color=y_axis[yaxis]['color'], width=1.2),
            hovertemplate=y_axis[yaxis]['hovertemplate'],
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=x_axis['Distance']['col'][vert_speed_peaks],
            y=y_axis[yaxis]['col'][vert_speed_peaks],
            mode='markers',
            marker=dict(color='Green', size=8),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=x_axis['Distance']['col'][vert_speed_lows],
            y=y_axis[yaxis]['col'][vert_speed_lows],
            mode='markers',
            marker=dict(color='Red', size=8),
            showlegend=False
        ))
        fig.update_layout(hovermode="x unified", legend=dict(yanchor="top", y=1, xanchor="right", x=1))
        fig.update_xaxes(title=f"Horizontal distance ({x_axis['Distance']['metric']})")
        fig.update_yaxes(title=f"{yaxis} ({y_axis[yaxis]['metric']})")
        return fig
