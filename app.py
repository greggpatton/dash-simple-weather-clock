from time import strftime

import flask

import dash
from dash import html, dcc, Input, Output

import dash_labs as dl

import dash_bootstrap_components as dbc

# Useful references:
# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Deploy_App_to_Web/PWA-Phone-App/res-seating/requirements.txt
# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/Complete_Guide/live_bootstrap.py
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
# https://hackerthemes.com/bootstrap-cheatsheet/
# https://dash.plotly.com/live-updates
# https://community.plotly.com/t/display-correct-time-in-browsers-timezone/49789/2

app = dash.Dash(
    __name__,
    plugins=[dl.plugins.pages],
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

server = app.server

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
        # size="lg",
        align_end=True,
        style={"font-size": "2em"},
    ),
    brand="Simple Weather Clock - Dash App",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True,
)

app.layout = dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
        # html.Span(id="get-local-date-time", hidden=True),
        dcc.Interval(id="interval-get-local-time", interval=1000),
        dcc.Interval(id="interval-get-local-date", interval=1000),
        # html.H1(id="local-date-time"),
        # dcc.Interval(id="interval-local-date-time", interval=1000),
    ],
    fluid=True,
    style={"font-size": "1vmin"},
)

app.clientside_callback(
    """
    function(n) {          
        const date = new Date();
        hour = date.toLocaleTimeString('en-US', { hour: 'numeric', hour12: true });
        ampm = hour.split(' ')[1];
        hour = String(hour.split(' ')[0]);
        minute = String(date.toLocaleTimeString('en-US', { minute: 'numeric' })).padStart(2, '0');
        second = String(date.toLocaleTimeString('en-US', { second: 'numeric' }).padStart(2, '0'));

        hm = '<span style="font-size: 15em;">' + hour + ':' + minute + '</span>';
        sm = '<span style="font-size: 10em;">:' + second + '</span>';
        ampm ='<span style="font-size: 4em; margin-left: .25em;">' + ampm + '</span>';

        document.getElementById("time").innerHTML = hm + sm + ampm;
    }
    """,
    Output("time", "children"),
    Input("interval-get-local-time", "n_intervals"),
)

app.clientside_callback(
    """
    function(n) {          
        const date = new Date();

        year = date.toLocaleString('en-US', { year: 'numeric' });

        month = date.toLocaleString('en-US', { month: 'short' });
        dayofweek = date.toLocaleString('en-US', { weekday: 'short' });
        day = String(date.toLocaleString('en-US', { day: 'numeric' }).padStart(1, '0'));

        dayofweek = '<span style="font-size: 10em;">' + dayofweek + '</span>';
        month = '<span style="font-size: 10em; margin-left: .25em;">' + month + '</span>';
        day = '<span style="font-size: 10em; margin-left: .25em;">' + day + '</span>';
        year = '<span style="font-size: 6em; margin-left: .5em;">' + year + '</span>';

        document.getElementById("date").innerHTML = dayofweek + month + day + year;
    }
    """,
    Output("date", "children"),
    Input("interval-get-local-date", "n_intervals"),
)


if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(
        debug=False,
        dev_tools_ui=False,
        dev_tools_silence_routes_logging=True,
    )
