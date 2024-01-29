from dash import Dash, html, dcc, Input, Output, no_update
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO, load_figure_template


load_figure_template(["minty", "darkly"])
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

# app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.scripts.config.serve_locally = True
server = app.server