import dash
from dash import dcc

import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/readme", order=3)

layout = dbc.Container(
    [
        dcc.Interval(id="interval-send-to-readme", interval=1, max_intervals=1),
    ],
)
