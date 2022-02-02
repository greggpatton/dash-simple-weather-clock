import random
from time import strftime

import dash
from dash import dcc, html, Input, Output, callback

import dash_bootstrap_components as dbc

from api_visualcrossing import ApiVisualCrossing

import pages.settings as settings

dash.register_page(__name__, path="/")

# https://github.com/plotly/dash-recipes/blob/707c225a15f6903bb0079b986e3df0516504d38e/dash_requests.py#L6
# https://stackoverflow.com/questions/47945841/how-to-access-a-cookie-from-callback-function-in-dash-by-plotly
# https://community.plotly.com/t/access-cookie-in-serve-layout-function/37351/3
# https://community.plotly.com/t/display-correct-time-in-browsers-timezone/49789/2

weather_api = ApiVisualCrossing()
# weather_api_key = ''
# with open('weather_api_key.txt', 'r') as file:
#     weather_api_key = file.read().replace('\n', '')

layout = dbc.Container(
    [
        html.Div(id="vshift", className="text-center"),
        dcc.Interval(
            id="interval-update-vshift",
            interval=10 * 1000,
            n_intervals=0,  # in milliseconds
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            id="time",
                            style={
                                "font-size": "25em", 
                                "line-height": ".4em",
                                "padding-top": ".1em",
                                },
                        ),
                    ],
                    width={"size": 12, "offset": 0},
                    class_name="text-center",
                    # style={"font-size": "1.9em", "padding-bottom": "1.5em"},
                ),
            ],
            justify="center",
            align="start",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            id="date",
                            style={
                                "font-size": "12em", 
                                "line-height": ".3em",
                                },
                            ),
                    ],
                    width={
                        "size": 10,
                        "offset": 0,
                    },
                    class_name="text-center",
                    # xs=12, sm=8, md=5, lg=6, xl=5
                    # style={
                    #     "font-size": "1em",
                    #     "line-height": ".3em",
                    # },
                ),
            ],
            justify="center",
            align="start",
            # align="baseline",
            # class_name="g-0",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(id="weather", className="text-center"),
                        dcc.Interval(
                            id="interval-update-weather",
                            interval=600 * 1000,
                            n_intervals=0,  # in milliseconds
                        ),
                    ],
                    width={
                        "size": 12,
                    },
                ),
            ],
            justify="center",
            align="start",
        ),
    ],
    # className="vh-100 d-flex align-items-center justify-content-center",
    # className="vh-100 d-flex justify-content-center",
    fluid=False,
    # style={"line-height": "7.5em"},
    # style={"font-size": "1.4vmin"},
    # style={"font-size": "1.75vmin", "line-height": "4.5em"},
)


@callback(Output("vshift", "children"), Input("interval-update-vshift", "n_intervals"))
def update_vshift(n):
    vshift = round(random.uniform(2, 14), 1)
    style = {"height": f"{vshift}em"}
    return [
        html.Div(style=style),
    ]


@callback(
    Output("weather", "children"), Input("interval-update-weather", "n_intervals")
)
def update_weather(n):
    location = settings.get_location()
    weather_api_key = settings.get_weather_api_key()

    if location and weather_api_key:
        weather_api.refresh(location, weather_api_key)
        return [
            html.Span(
                f"{weather_api.get_resolved_address()}",
                style={
                    "fontSize": "2em",
                    # "line-height": ".3em",
                    # "padding-top": "5em",
                    "padding-bottom": "10em",
                },
            ),
            html.Br(),
            html.Span(
                f"Temp : {weather_api.get_temperature()}",
                style={
                    "fontSize": "10em",
                    "line-height": ".7em",
                },
                # className="text-nowrap",
            ),
            html.Span(
                f"Feels : {weather_api.get_feels_like_temperature()}",
                style={
                    "fontSize": "6em",
                    # "line-height": ".4em",
                    "margin-left": ".5em",
                },
            ),
            html.Br(),
            html.Span(
                f"High :  {weather_api.get_high_temperature()}",
                style={
                    "fontSize": "6em",
                    "line-height": ".75em",
                },
            ),
            html.Span(
                f"Low : {weather_api.get_low_temperature()}",
                style={
                    "fontSize": "6em",
                    "line-height": ".75em",
                    "margin-left": "1em",
                },
            ),
            html.Br(),
            html.Span(
                f"Wind: {weather_api.get_wind_speed()}",
                style={
                    "fontSize": "7em",
                    # "line-height": ".5em",
                },
            ),
            html.Span(
                f"Gusting: {weather_api.get_wind_gust()}",
                style={
                    "fontSize": "7em",
                    # "line-height": ".5em",
                    "margin-left": ".5em",
                },
            ),
            html.Span(
                f"{weather_api.get_wind_direction()}",
                style={
                    "fontSize": "5em",
                    # "line-height": ".5em",
                    "margin-left": ".5em",
                },
            ),
        ]
    else:
        return dcc.Location(pathname="/Settings", id="location-settings")
