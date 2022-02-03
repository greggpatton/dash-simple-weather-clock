from time import strftime

import dash
from dash import dcc, html, Input, Output, callback

import dash_bootstrap_components as dbc

from api_visualcrossing import ApiVisualCrossing

import pages.settings as settings

dash.register_page(__name__, path="/", name="Weather Clock", order=1)

# https://github.com/plotly/dash-recipes/blob/707c225a15f6903bb0079b986e3df0516504d38e/dash_requests.py#L6
# https://stackoverflow.com/questions/47945841/how-to-access-a-cookie-from-callback-function-in-dash-by-plotly
# https://community.plotly.com/t/access-cookie-in-serve-layout-function/37351/3
# https://community.plotly.com/t/display-correct-time-in-browsers-timezone/49789/2

weather_api = ApiVisualCrossing()

layout = dbc.Container(
    [
        dcc.Interval(id="interval-get-local-time", interval=1000),
        dcc.Interval(id="interval-get-local-date", interval=1000),
        html.Div(id="vertical-shift", className="text-center"),
        dcc.Interval(
            id="interval-update-vshift",
            interval=10 * 1000,
            n_intervals=0,  # in milliseconds
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Span(
                            id="time-hours-minutes",
                            style={
                                "font-size": "25em",
                            },
                        ),
                        html.Span(
                            id="time-seconds",
                            style={
                                "font-size": "15em",
                            },
                        ),
                        html.Span(
                            id="time-ampm",
                            style={
                                "font-size": "5em",
                                "margin-left": ".25em",
                            },
                        ),
                    ],
                    class_name="text-center",
                ),
            ],
            justify="center",
            align="start",
            style={
                "line-height": "7.5em",
                "padding-top": "5em",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Span(
                            id="date-dayofweek-month-day",
                            style={
                                "font-size": "12em",
                            },
                        ),
                        html.Span(
                            id="date-year",
                            style={
                                "font-size": "5em",
                                "margin-left": ".5em",
                            },
                        ),
                    ],
                    class_name="text-center",
                ),
            ],
            justify="center",
            align="start",
            style={
                "line-height": "6em",
                "padding-top": ".75em",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(id="weather", className="text-center"),
                        dcc.Interval(
                            id="interval-update-weather",
                            interval=600 * 1000, # every 10 minutes
                            n_intervals=0,
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
    fluid=False,
)


@callback(
    Output("weather", "children"), Input("interval-update-weather", "n_intervals")
)
def update_weather(n):
    location = settings.get_location()
    weather_api_key = settings.get_weather_api_key()

    if location and weather_api_key:
        weather_api.refresh(location, weather_api_key, settings.get_data_units())
        return [
            html.Span(
                f"{weather_api.get_resolved_address()}",
                style={
                    "fontSize": "2em",
                    "line-height": "2em",
                },
            ),
            html.Span(
                f"{settings.get_data_units_label()}",
                style={
                    "fontSize": "2em",
                    "line-height": "2em",
                    "margin-left": ".75em",
                },
            ),
            html.Br(),
            html.Span(
                f"Temp : {weather_api.get_temperature()}",
                style={
                    "fontSize": "10em",
                    "line-height": ".7em",
                },
            ),
            html.Span(
                f"Feels : {weather_api.get_feels_like_temperature()}",
                style={
                    "fontSize": "6em",
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
                    "fontSize": "6em",
                },
            ),
            html.Span(
                f"Gusting: {weather_api.get_wind_gust()}",
                style={
                    "fontSize": "6em",
                    "margin-left": ".25em",
                },
            ),
            html.Span(
                f"from {weather_api.get_wind_direction()}",
                style={
                    "fontSize": "4vmin",
                    "margin-left": ".25em",
                },
            ),
        ]
    else:
        return dcc.Location(pathname="/Settings", id="location-settings")
