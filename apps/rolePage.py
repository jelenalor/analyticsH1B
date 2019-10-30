import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import udf
from app import app


layout = html.Div([
            html.Div([html.H1('Salary by Type of Role Analytics',
                              style={"textAlign": "center", 'padding': '20px 0 0 0'})]),
                    html.Br(),
                    udf.returnFooter()

                    ], style={'margin': 0})




# html.Div([
#     html.Div([html.H3('Return Role page', style={"textAlign": "center"})]),
#     html.Div([
#         html.Div([dcc.Graph(id='crossfilter-scatter2'),
#                   ], style={'display': 'inline-block', 'width': '50%'}),
#
#         html.Div([
#             dcc.Graph(id='top-line-plot2', figure={
#                 'layout': {'height': 300,
#                            'margin': {'l': 40, 'b': 30, 'r': 20, 't': 40},
#                            'annotations': [{
#                                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
#                                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#                                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
#                                'text': "title", 'font': {'size': 14, 'color': "black"},
#                                'bordercolor': 'black', 'borderwidth': 2,
#                                'borderpad': 4, 'bgcolor': 'white',
#                                'opacity': 0.5
#                            }]}}),
#             dcc.Graph(id='bottom-line-plot2', figure={
#                 'layout': {'height': 300,
#                            'margin': {'l': 40, 'b': 30, 'r': 20, 't': 40},
#                            'annotations': [{
#                                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
#                                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#                                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
#                                'text': "title", 'font': {'size': 14, 'color': "black"},
#                                'bordercolor': 'black', 'borderwidth': 2,
#                                'borderpad': 4, 'bgcolor': 'white',
#                                'opacity': 0.5
#                            }]}})
#         ], style={'display': 'inline-block',
#                   'width': '50%'})
#     ])
# ])