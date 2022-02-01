from time import strftime

import dash

import dash_labs as dl

import dash_bootstrap_components as dbc

# Useful references:
# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Deploy_App_to_Web/PWA-Phone-App/res-seating/requirements.txt
# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/Complete_Guide/live_bootstrap.py
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
# https://hackerthemes.com/bootstrap-cheatsheet/
# https://dash.plotly.com/live-updates

app = dash.Dash(
    __name__,
    plugins=[dl.plugins.pages],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Simple Weather Clock - Plotly Dash App",
    brand_href="/",
    dark=True,
)

app.layout = dbc.Container(
    [navbar, dl.plugins.page_container],
    fluid=True,
    style={"font-size": "2vmin"},
)

if __name__ == "__main__":
    # app.run_server(debug=True, port=8000)
    app.run_server(
        debug=False,
        dev_tools_ui=False,
        dev_tools_silence_routes_logging=True,
    )
