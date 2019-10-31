import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json
from app import app
from udfs import udf

# https://plot.ly/python/horizontal-bar-charts/


def returnScatter():
    return html.Div([html.H3('Roles Count & Salary by Company',
                             style={"textAlign": "center"}),
                     html.P('Hover over any of the points to discover which city it represents. Click on the point to continue analysing the patterns for chosen city. Switch between displaying mean, maximum or minimum salary. ', style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
         dcc.RadioItems(
             id='choice-items1',
             options=[{'label': k, 'value': k} for k in ["mean",
                                                         "min", "max"]],
             value='mean',
             inputStyle={'display': 'inline-block',
                         'padding': '0 0'}),
        dcc.Graph(id='crossfilter-scatter1',
                  figure=udf.create_scatter("mean", "NEW YORK"),
                  clickData={'points': [{'customdata': 'NEW YORK',
                                         'text': 'NEW YORK'}]}
                  ),
                              ], style={'width': '50%',
                                        'height': '600px', 'margin': '20px auto',
                                        "textAlign": "center"})


def returnTopCompanies():
    return html.Div([html.H3('Top Companies Analysis',
                             style={"textAlign": "center"}),
                     html.P('Analyse the quantity of roles available as well as salary in the top 20 employers for a chosen city.', style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
        dcc.Graph(id='top_companies_fig1',
                     figure=udf.createMultiGraph(udf.getDataTopComp("NEW YORK", "mean"), "None"))
                     ], style={'width': '70%',
                               'height': '800px', 'margin': '20px 250px'})


def returnTopRoles():
    return html.Div([html.H3('Top Roles Analysis',
                             style={"textAlign": "center"}),
                     html.P("Analyse the quantity of various roles available as well as salary for a chosen city. Roles are displayed as a main \'root\' word extracted from the original job title to present similar roles as one. Our analysis show that around 82% of job titles have at least one of these \'root\' words in it", style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
        dcc.Graph(id='top_roles_fig1',
                  clickData={'points': [{'y': 'analyst',
                                         'text': 'analyst'}]},
                  )
                     ], style={'width': '70%',
                               'height': '800px', 'margin': '20px 250px'})


def returnSalDist():
    return html.Div([html.H3('Salary Distribution & Role Analysis',
                             style={"textAlign": "center"}),
                     html.P("Analyst salaries vary widely. Discover which type of analysts have the highest pay. Check it out for other job roles by clicking on the corresponding bar plot", style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
                    dcc.Graph(id='sal_dist_fig1')
                     ], style={'width': '70%',
                               'height': '700px', 'margin': '20px 250px'})




layout = html.Div([
            html.Div([html.H1('Salary by Cities Analytics',
                              style={"textAlign": "center", 'padding': '20px 0 0 0'})]),
                    html.Div(id='intermediate-value', style={'display': 'none'}),
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
              [Input('choice-items1', 'value'),
               Input('crossfilter-scatter1', 'clickData')])
def updateScatter(value, clickData):
    city = clickData["points"][0]['customdata']
    return udf.create_scatter(str(value), city)


# @app.callback(Output('intermediate-value', 'children'),
#               [Input('crossfilter-scatter1', 'clickData')])
# def clean_data(clickData):
#      city = clickData["points"][0]['customdata']
#      # some expensive clean data step
#      dff = udf.df[udf.df.city == city]
#
#      # more generally, this line would be
#      # json.dumps(cleaned_df)
#      return json.dumps(dff)

"""Top Companies"""
@app.callback(Output('top_companies_fig1', 'figure'),
              [Input('choice-items1', 'value'),
               Input('crossfilter-scatter1', 'clickData')])
def updateTopCompanies(value, clickData):
    city = clickData["points"][0]['customdata']
    return udf.createMultiGraph(udf.getDataTopComp(city, str(value)), "None")


"""Top Roles"""
@app.callback(Output('top_roles_fig1', 'figure'),
              [Input('choice-items1', 'value'),
               Input('crossfilter-scatter1', 'clickData'),
               Input('top_roles_fig1', 'clickData')])
def updateTopCompanies(value, clickData, roleClickData):
    city = clickData["points"][0]['customdata']
    role = roleClickData["points"][0]['y']
    return udf.createMultiGraph(udf.dataForTopRoles(city, str(value)), str(role))


@app.callback(
    Output('sal_dist_fig1', 'figure'),
    [Input('crossfilter-scatter1', 'clickData'),
    Input('top_roles_fig1', 'clickData')])
def update_figure(clickData, roleClickData):
    city = clickData["points"][0]['customdata']
    role = roleClickData["points"][0]['y']
    return udf.createBoxPlot(str(city), str(role))





