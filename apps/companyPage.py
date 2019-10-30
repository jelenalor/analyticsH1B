import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import udf
from app import app



layout = html.Div([
                html.Div([html.H1('Salary by Company Analytics',
                                  style={"textAlign": "center", 'padding': '20px 0 0 0'})]),
                html.Br(),
                udf.returnFooter()

            ], style={'margin': 0})
