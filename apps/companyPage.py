import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from udfs import udf_rol
from udfs import udf
from app import app

key_title_tokens = ["engin", "develop", "architect", "administr", \
                        "account", "auditor", \
                        "analyst", "manag", "consult", "associ",\
                        "presid", "programm", "professor"]





layout = html.Div([

                html.Div([html.H1('Salary by Company Analytics',
                                  style={"textAlign": "center", 'padding': '20px 0 0 0'})]),
                html.Br(),
                udf.returnFooter()

            ], style={'margin': 0})
