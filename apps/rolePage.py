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


def returnTopRoles():
    return html.Div([html.H3('Top Roles Analysis',
                             style={"textAlign": "center"}),
                     html.P("Analysent ", style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
        dcc.Graph(id='top_roles_fig2',
                  clickData={'points': [{'y': 'analyst',
                                         'text': 'analyst'}]},
                  )
                     ], style={'width': '70%',
                               'height': '700px', 'margin': '20px 250px'})

def returnTopLocations():
    return html.Div([html.H3('Top Locations Analysis',
                             style={"textAlign": "center"}),
                     html.P("Analysent ", style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
        dcc.Graph(id='top_loc_fig2',
                  clickData={'points': [{'y': 'analyst',
                                         'text': 'analyst'}]},
                  )
                     ], style={'width': '70%',
                               'height': '900px', 'margin': '20px 250px'})


def returnTopCompanies():
    return html.Div([html.H3('Top Companies Analysis',
                             style={"textAlign": "center"}),
                     html.P("Analysent ", style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
        dcc.Graph(id='top_comp_fig2',
                  clickData={'points': [{'y': 'analyst',
                                         'text': 'analyst'}]},
                  )
                     ], style={'width': '70%',
                               'height': '900px', 'margin': '20px 250px'})


layout = html.Div([
            html.Div([html.H1('Salary by Type of Role Analytics',
                              style={"textAlign": "center", 'padding': '20px 0 0 0'})]),
                    html.Br(),
                    html.Div([
                    dcc.RadioItems(
                         id='choice-items2',
                         options=[{'label': k, 'value': k} for k in key_title_tokens],
                         value='analyst',
                         inputStyle={'display': 'inline-block',
                                     "margin-left": "20px"})],
                        style={'margin': '0 auto', "textAlign": "center"}
                    ),
                    returnTopRoles(),
                    html.Br(),
                    returnTopLocations(),
                    html.Br(),
                    returnTopCompanies(),
                    udf.returnFooter()

                    ], style={'margin': 0})


@app.callback([Output('top_roles_fig2', 'figure'),
               Output('top_loc_fig2', 'figure'),
               Output('top_comp_fig2', 'figure')],
              [Input('choice-items2', 'value')])
def updateTopCompanies(value):
    items_roles = udf_rol.dataForRoles(str(value))[0]
    items_locations = udf_rol.dataForRoles(str(value))[1]
    items_companies = udf_rol.dataForRoles(str(value))[2]
    return udf_rol.createMultiGraphRoles(items_roles, 500), \
           udf_rol.createMultiGraphRoles(items_locations, 700), \
           udf_rol.createMultiGraphRoles(items_companies, 700)
