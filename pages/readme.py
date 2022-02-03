import dash
from dash import dcc

import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/readme", name='Readme on GitHub', order=3)

layout = dbc.Container(
    [
        dcc.Interval(id="interval-send-to-github-readme", interval=1, max_intervals=1),
    ],
)
