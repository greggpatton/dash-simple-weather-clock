import datetime

import dash

from dash import html, dcc, Input, Output, callback

import dash_bootstrap_components as dbc

import flask

import base64_utils as b64

dash.register_page(__name__, path="/settings", order=2)

API_COOKIE_KEY = "dash_simple_weather_clock_weather_api_cookie_key"
LOCATION_COOKIE_KEY = "dash_simple_weather_clock_location"
DATA_UNITS_COOKIE_KEY = "dash_simple_weather_clock_data_units"

DATA_UNITS_DICT = {'metric': 'Metric (°C, km)', 'us': 'US (°F, mi)', 'uk': 'UK (°C, mi)'}

# https://www.youtube.com/watch?v=VZ6IdRMc0RI&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=8
# https://dash.plotly.com/dash-core-components/input
# https://stackoverflow.com/questions/26613435/python-flask-not-creating-cookie-when-setting-expiration
# https://tedboy.github.io/flask/generated/generated/flask.Response.set_cookie.html

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                            #### Get your free API key from Visual Crossing.
                            """,
                            style={"padding-top": "1em"},
                        ),
                        dcc.Link(
                            "Visual Crossing Global Weather API",
                            href="https://www.visualcrossing.com/weather-api",
                            target="_blank",
                            style={"font-size": "2em"},
                        ),
                    ],
                    width={"size": 12, "offset": 0},
                ),
            ],
            justify="center",
            style={"font-size": "2em", "line-height": "2em"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "API Key: ",
                            style={"line-height": "2em"},
                        ),
                        dbc.Input(
                            id="input-weather-api-key",
                            type="password",
                            placeholder="Enter weather API key",
                            debounce=True,
                            autoComplete="on",
                            size="50",
                            class_name="input-lg",
                        ),
                    ],
                    width={"size": 4, "offset": 0},
                ),
            ],
            id="weather-api-key",
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "Location: ",
                            style={"line-height": "2em"},
                        ),
                        dbc.Input(
                            id="input-location",
                            placeholder="Enter location",
                            debounce=True,
                            autoComplete="on",
                            size="50",
                            class_name="input-lg",
                        ),
                    ],
                    width={"size": 4, "offset": 0},
                ),
            ],
            id="location",
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "Data Units: ",
                            style={"line-height": "2em"},
                        ),
                        dbc.Select(
                            id="input-data-units",
                            options=[
                                {"label": DATA_UNITS_DICT["metric"], "value": "metric"},
                                {"label": DATA_UNITS_DICT["us"], "value": "us"},
                                {"label": DATA_UNITS_DICT["uk"], "value": "uk"},
                            ],
                            class_name="input-lg",
                        ),
                    ],
                    width={"size": 4, "offset": 0},
                ),
            ],
            id="data-units",
            justify="center",
        ),
    ],
    class_name="text-center",
)

@callback(
    Output("input-weather-api-key", "value"),
    Input("input-weather-api-key", "value"),
)
def update_weather_api_key(value):
    if value is not None:
        dash.callback_context.response.set_cookie(
            API_COOKIE_KEY,
            b64.encode(value),
            expires=datetime.datetime.now() + datetime.timedelta(days=200000),
        )
    else:
        value = get_weather_api_key()
    return value

@callback(
    Output("input-location", "value"),
    Input("input-location", "value"),
)
def update_location(value):
    if value is not None:
        dash.callback_context.response.set_cookie(
            LOCATION_COOKIE_KEY,
            b64.encode(value),
            expires=datetime.datetime.now() + datetime.timedelta(days=200000),
        )
    else:
        value = get_location()
    return value


@callback(
    Output("input-data-units", "value"),
    Input("input-data-units", "value"),
)
def update_data_units(value):
    if value is not None:
        dash.callback_context.response.set_cookie(
            DATA_UNITS_COOKIE_KEY,
            b64.encode(value),
            expires=datetime.datetime.now() + datetime.timedelta(days=200000),
        )
    else:
        value = get_data_units()
    return value


def get_weather_api_key():
    allcookies = dict(flask.request.cookies)
    if API_COOKIE_KEY in allcookies:
        return b64.decode(allcookies[API_COOKIE_KEY])
    else:
        return ""


def get_location():
    allcookies = dict(flask.request.cookies)
    if LOCATION_COOKIE_KEY in allcookies:
        return b64.decode(allcookies[LOCATION_COOKIE_KEY])
    else:
        return ""

def get_data_units():
    allcookies = dict(flask.request.cookies)
    if DATA_UNITS_COOKIE_KEY in allcookies:
        return b64.decode(allcookies[DATA_UNITS_COOKIE_KEY])
    else:
        return "metric"

def get_data_units_label():
    return DATA_UNITS_DICT[get_data_units()]
