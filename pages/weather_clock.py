import random
from time import strftime

import dash
from dash import dcc, html, Input, Output, callback

from api_visualcrossing import ApiVisualCrossing

import pages.settings as settings

dash.register_page(__name__, path="/")

# https://github.com/plotly/dash-recipes/blob/707c225a15f6903bb0079b986e3df0516504d38e/dash_requests.py#L6
# https://stackoverflow.com/questions/47945841/how-to-access-a-cookie-from-callback-function-in-dash-by-plotly
# https://community.plotly.com/t/access-cookie-in-serve-layout-function/37351/3

weather_api = ApiVisualCrossing()
# weather_api_key = ''
# with open('weather_api_key.txt', 'r') as file:
#     weather_api_key = file.read().replace('\n', '')

layout = html.Div(
    [
        html.Div(id="vshift", className="text-center"),
        dcc.Interval(
            id="interval-update-vshift",
            interval=10 * 1000,
            n_intervals=0,  # in milliseconds
        ),
        html.Div(id="clock", className="text-center"),
        # dcc.Interval(
        #     id="interval-update-clock",
        #     interval=1 * 1000,
        #     n_intervals=0,  # in milliseconds
        # ),
        html.Div(id="weather", className="text-center"),
        dcc.Interval(
            id="interval-update-weather",
            interval=600 * 1000,
            n_intervals=0,  # in milliseconds
        ),
    ],
    # className="vh-100 d-flex align-items-center justify-content-center",
    # className="vh-100 d-flex justify-content-center",
    style={'font-size': '1.75vmin', "line-height": "4.5em"},
)

@callback(
    Output("vshift", "children"), Input("interval-update-vshift", "n_intervals")
)
def update_vshift(n):
    vshift = round(random.uniform(3, 8), 1)
    style = {'height': f'{vshift}em'}
    return [
        html.Div(style=style),
    ]

# @callback(
#     Output("clock", "children"), Input("interval-update-clock", "n_intervals")
# )
# def update_clock(n):        
#     return [
#         html.Span(f'{strftime("%I:%M").lstrip("0")}', style={"fontSize": "15em"}),
#         html.Span(f'{strftime(":%S")}', style={"fontSize": "10em"}),
#         html.Span(
#             f'{strftime("%p")}', style={"fontSize": "4em", "marginLeft": "0.25em"}
#         ),
#         html.Br(),
#         html.Span(f'{strftime("%a")}', style={"fontSize": "10em", "line-height": ".5em"}),
#         html.Span(
#             f'{strftime("%b")}', style={"fontSize": "10em", "marginLeft": "0.5em"}
#         ),
#         html.Span(
#             f'{strftime("%d")}', style={"fontSize": "10em", "marginLeft": "0.5em"}
#         ),
#         html.Span(
#             f'{strftime("%Y")}', style={"fontSize": "5em", "marginLeft": "0.5em"}
#         ),
#     ]

@callback(
    Output("weather", "children"), Input("interval-update-weather", "n_intervals")
)
def update_weather(n):
    location = settings.get_location()
    weather_api_key = settings.get_weather_api_key()

    if location and weather_api_key:
        weather_api.refresh(location, weather_api_key)
        return [
            html.Span(f'{weather_api.get_resolved_address()}', style={"fontSize": "1em"}),
            html.Br(),
            html.Span(f'Temp : {weather_api.get_temperature()}', style={"fontSize": "9em", 'line-height': '.4em'}),
            html.Span(f'Feels : {weather_api.get_feels_like_temperature()}', style={"fontSize": "4em", 'line-height': '.4em', 'margin-left': '.5em'}),
            html.Br(),
            html.Span(f'High :  {weather_api.get_high_temperature()}', style={"fontSize": "3.5em", 'line-height': '1em'}),
            html.Span(f'Low : {weather_api.get_low_temperature()}', style={"fontSize": "3.5em", 'line-height': '1em', 'margin-left': '1em'}),
            html.Br(),
            html.Span(f'Wind : {weather_api.get_wind_speed()}', style={"fontSize": "6em", 'line-height': '.5em'}),
            html.Span(f'{weather_api.get_wind_direction()}', style={"fontSize": "6em", 'line-height': '.5em', 'margin-left': '1em'}),
            html.Span(f'Gusting : {weather_api.get_wind_gust()}', style={"fontSize": "6em", 'line-height': '.5em', 'margin-left': '1em'}),
        ]
    else:
        return dcc.Location(pathname="/Settings", id="location-settings")
        
