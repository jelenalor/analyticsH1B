import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from udfs import udf_comp
from udfs import udf
from app import app

key_title_tokens = udf.key_title_tokens


def returnScatter():
    return html.Div([html.H3('Roles Count & Salary by Company',
                             style={"textAlign": "center"}),
                     html.P('Hover over any of the points to discover which company it represents. Pick a company in the dropdown or by clicking on any of the points to discover the patterns for a chosen company.', style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
         dcc.Dropdown(id="dropdown3", placeholder="Pick a company",
                      options=[{'label': str(i), 'value': i} for i in udf_comp.name],
                      style={"width": '50%', "textAlign": "center", 'margin': '0 auto'}),
        dcc.Graph(id='crossfilter-scatter3',
                  figure=udf.create_scatter("mean", "ACCENTURE LLP"),
                  clickData={'points': [{'customdata': 'ACCENTURE LLP',
                                         'text': 'ACCENTURE LLP'}]}
                  ),
                              ], style={'width': '50%',
                                        'height': '600px', 'margin': '20px auto',
                                        "textAlign": "center"})


def returnSalDist():
    return html.Div([html.H3('Salary Distribution & Top Roles Analysis',
                             style={"textAlign": "center"}),
                     html.P("Discover which type of role have the highest pay at a chosen company.", style={'padding': '10px 10px',
                                                  "textAlign": "center"}),

                    dcc.Graph(id='sal_dist_fig3')
                     ], style={'width': '70%',
                               'height': '800px', 'margin': '20px 250px'})


def returnTopLoc():
    return html.Div([html.H3('Top Locations Analysis',
                             style={"textAlign": "center"}),
                     html.P('Discover the cities with the most jobs and its corresponding salaries', style={'padding': '10px 10px',
                                                  "textAlign": "center"}),
        dcc.Graph(id='top_loc_fig3',
                     figure=udf_comp.createMultiGraphComp(udf_comp.getDataComp("ACCENTURE LLP")))
                     ], style={'width': '80%',
                               'textAlign': 'center',
                               'height': '700px', 'margin': '20px auto'})


layout = html.Div([

                html.Div([html.H1('Salary by Company Analytics',
                                  style={"textAlign": "center", 'padding': '20px 0 0 0'})]),
                html.Br(),
                returnScatter(),
                html.Br(),
                returnSalDist(),
                returnTopLoc(),
                udf.returnFooter(),
            ], style={'margin': 0})


prev_value = ""
"""Tab1 Radio button"""
@app.callback([Output('crossfilter-scatter3', 'figure'),
                Output('top_loc_fig3', 'figure')],
              [Input('crossfilter-scatter3', 'clickData'),
               Input('dropdown3', 'value')])
def updateScatter(clickData, dropdown):
    if dropdown is not None and prev_value != dropdown:
        comp = dropdown
    else:
        comp = clickData["points"][0]['customdata']

    return udf_comp.create_scatter_comp(comp), \
           udf_comp.createMultiGraphComp(udf_comp.getDataComp(comp))



@app.callback(
    Output('sal_dist_fig3', 'figure'),
    [Input('crossfilter-scatter3', 'clickData'),
     Input('dropdown3', 'value')])
def update_figure(clickData, dropdown):
    if dropdown is not None and prev_value != dropdown:
        comp = dropdown
    else:
        comp = clickData["points"][0]['customdata']
    return udf_comp.createBoxPlot(comp)


