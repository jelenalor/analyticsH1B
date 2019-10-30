import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import udf

# https://plot.ly/python/horizontal-bar-charts/


def returnScatter():
    return html.Div([html.H3('Roles Count & Salary by Company',
                             style={"textAlign": "center"}),
                     html.P('Description', style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
         dcc.RadioItems(
             id='choice-items1',
             options=[{'label': k, 'value': k} for k in ["mean",
                                                         "min", "max"]],
             value='mean',
             inputStyle={'display': 'inline-block',
                         'padding': '0 0'}),
        dcc.Graph(id='crossfilter-scatter1',
                  figure=udf.create_scatter("mean"),
                  hoverData={'points': [{'customdata': 'NEW YORK',
                                         'text': 'NEW YORK'}]}
                  ),
                              ], style={'width': '50%',
                                        'height': '600px', 'margin': '20px auto',
                                        "textAlign": "center"})


def returnTopCompanies():
    return html.Div([html.H3('Top Companies Analysis',
                             style={"textAlign": "center"}),
                     html.P('Description', style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
        dcc.Graph(id='top_companies_fig1',
                     figure=udf.create_top_comp_analysis("NEW YORK", "mean"))
                     ], style={'width': '70%',
                               'height': '700px', 'margin': '20px 250px'})


def returnTopRoles():
    return html.Div([html.H3('Top Roles Analysis',
                             style={"textAlign": "center"}),
                     html.P('Description', style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
        dcc.Graph(id='top_roles_fig1')
                     ], style={'width': '50%',
                               'height': '600px', 'margin': '20px 450px'})


def returnSalDist():
    return html.Div([html.H3('Salary Distribution & Role Analysis',
                             style={"textAlign": "center"}),
                     html.P('Description', style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
                    dcc.Graph(id='sal_dist_fig1')
                     ], style={'width': '50%',
                               'height': '600px', 'margin': '20px 450px'})




layout = html.Div([
            html.Div([html.H1('Salary by Cities Analytics',
                              style={"textAlign": "center", 'padding': '20px 0 0 0'})]),
                    html.Br(),
                    returnScatter(),
                    html.Br(),
                    returnTopCompanies(),
                    html.Br(),
                    returnTopRoles(),
                    html.Br(),
                    returnSalDist(),
                    html.Br(),
                    udf.returnFooter()

                    ], style={'margin': 0,})

"""Tab1 Radio button"""
@app.callback(Output('crossfilter-scatter1', 'figure'),
              [Input('choice-items1', 'value')])
def render_content(value):
    return udf.create_scatter(str(value))






