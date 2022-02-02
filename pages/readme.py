import requests

import dash
from dash import dcc

import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/readme")

response = requests.get(
    "https://raw.githubusercontent.com/greggpatton/dash-simple-weather-clock/main/README.md"
)
readme = response.text

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(readme),
                    ],
                    width={"size": 12, "offset": 0},
                ),
            ],
            justify="center",
            style={"font-size": "2em", "line-height": "2em"},
        ),
    ],
    class_name="text-center",
)
