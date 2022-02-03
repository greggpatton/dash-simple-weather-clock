from time import strftime

import dash
from dash import dcc, Input, Output

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
            dbc.DropdownMenuItem(
                page["name"], href=page["path"], style={"font-size": "1.25rem"}
            )
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
        align_end=True,
        style={"font-size": "1.25rem"},
    ),
    brand="Simple Weather Clock",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True,
    brand_style={"font-size": "3.75vmin"},
)

app.layout = dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
        dcc.Location(id="redirect-to-location"),
    ],
    fluid=True,
    style={"font-size": "1vmin"},
)

app.clientside_callback(
    """
    function(n) {          
        const min = 2
        const max = 14
        
        const vshift = Math.random() * (max - min) + min;

        div = '<div style="height:' + vshift + 'em;"/>';

        document.getElementById("vertical-shift").innerHTML = div;
    }
    """,
    Output("vertical-shift", "children"),
    Input("interval-update-vshift", "n_intervals"),
)

app.clientside_callback(
    """
    function(n) {          
        window.open("https://github.com/greggpatton/dash-simple-weather-clock#simple-weather-clock");
        return "/";
    }
    """,
    Output("redirect-to-location", "href"),
    Input("interval-send-to-github-readme", "n_intervals"),
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

        hm = '<span>' + hour + ':' + minute + '</span>';
        sm = '<span style="font-size: .5em;">:' + second + '</span>';
        ampm ='<span style="font-size: .1em; margin-left: .15em;">' + ampm + '</span>';

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

        dayofweek = '<span">' + dayofweek + '</span>';
        month = '<span style="font-size: 1em; margin-left: .25em;">' + month + '</span>';
        day = '<span style="font-size: 1em; margin-left: .25em;">' + day + '</span>';
        year = '<span style="font-size: .5em; margin-left: .5em;">' + year + '</span>';

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
