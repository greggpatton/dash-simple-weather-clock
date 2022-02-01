import datetime

from dash import html, dcc, Input, Output, callback
import dash

import flask

import base64_utils as b64

dash.register_page(__name__, path="/Settings")

API_COOKIE_KEY = "dash_simple_weather_clock_weather_api_cookie_key"
LOCATION_COOKIE_KEY = "dash_simple_weather_clock_location"

# https://www.youtube.com/watch?v=VZ6IdRMc0RI&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=8
# https://dash.plotly.com/dash-core-components/input
# https://stackoverflow.com/questions/26613435/python-flask-not-creating-cookie-when-setting-expiration
# https://tedboy.github.io/flask/generated/generated/flask.Response.set_cookie.html

layout = html.Div(
    [
        html.Div(
            [
                dcc.Link(
                    "Visual Crossing Global Weather API",
                    href="https://www.visualcrossing.com/weather-api",
                    target="_blank",
                ),
            ],
            className="text-center",
            style={"font-size": "2em", "line-height": "2em"},
        ),
        html.Div(
            [
                html.H1(
                    "Weather API Key: ",
                    style={"line-height": "2em"},
                ),
                dcc.Input(
                    id="input-weather-api-key",
                    type="password",
                    placeholder="Enter weather API key",
                    debounce=True,
                    autoComplete="on",
                    size="50",
                ),
            ],
            id="weather-api-key",
            className="text-center",
        ),
        html.Br(
            style={"line-height": "2em"},
        ),
        html.Div(
            [
                html.H1(
                    "Location: ",
                    style={"line-height": "2em"},
                ),
                dcc.Input(
                    id="input-location",
                    placeholder="Enter location",
                    debounce=True,
                    autoComplete="on",
                    size="50",
                ),
            ],
            id="location",
            className="text-center",
        ),
    ],
)


@callback(
    Output("input-location", "value"),
    [Input("input-location", "value")],
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
    Output("input-weather-api-key", "value"),
    [Input("input-weather-api-key", "value")],
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
