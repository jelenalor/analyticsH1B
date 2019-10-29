import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def returnCompanyPage():
    return html.Div([
        html.Div([html.H3('Return Company page', style={"textAlign": "center"})]),
        html.Div([
            html.Div([dcc.Graph(id='crossfilter-scatter3'),
                      ], style={'display': 'inline-block', 'width': '50%'}),

            html.Div([
                dcc.Graph(id='top-line-plot3', figure={
                    'layout': {'height': 300,
                               'margin': {'l': 40, 'b': 30, 'r': 20, 't': 40},
                               'annotations': [{
                                   'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                                   'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                                   'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                                   'text': "title", 'font': {'size': 14, 'color': "black"},
                                   'bordercolor': 'black', 'borderwidth': 2,
                                   'borderpad': 4, 'bgcolor': 'white',
                                   'opacity': 0.5
                               }]}}),
                dcc.Graph(id='bottom-line-plot3', figure={
                    'layout': {'height': 300,
                               'margin': {'l': 40, 'b': 30, 'r': 20, 't': 40},
                               'annotations': [{
                                   'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                                   'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                                   'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                                   'text': "title", 'font': {'size': 14, 'color': "black"},
                                   'bordercolor': 'black', 'borderwidth': 2,
                                   'borderpad': 4, 'bgcolor': 'white',
                                   'opacity': 0.5
                               }]}})
            ], style={'display': 'inline-block',
                      'width': '50%'})
        ])
    ])