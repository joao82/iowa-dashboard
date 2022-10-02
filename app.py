import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

import dash
from dash import html

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]
external_stylesheets = [
    meta_tags,
    font_awesome,
    dbc.themes.FLATLY
]

url_theme1 = dbc.themes.FLATLY
template_theme1 = "flatly"
url_theme2 = dbc.themes.DARKLY
template_theme2 = "darkly"

app = dash.Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

server = app.server

theme_switch = ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])

theme_colors = [
    "primary",
    "secondary",
    "success",
    "warning",
    "danger",
    "info",
    "light",
    "dark",
    "link",
]
# buttons = html.Div(
#     [dbc.Button(f"{color}", color=f"{color}", size="sm") for color in theme_colors]
# )
# colors = html.Div(["Theme Colors:", buttons], className="mt-2")


navbar = dbc.NavbarSimple(
children = [
    dbc.NavItem(theme_switch,
                className="text-primary d-flex align-items-center m-2"),
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
        ],
        nav=True,
        label="Menu"
    )],
    brand="Iowa Liquor Sales Dashboard",
    color="light",
    dark=False,
    className="text-primary d-flex align-items-center m-2"
)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container
    ],
    fluid=False,
)


if __name__ == "__main__":
    app.run(debug=True)
