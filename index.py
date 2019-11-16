import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app
from apps import cityPage, rolePage, companyPage

""" App """
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets=external_stylesheets

server = app.server

""" Define Layout with three tabs"""

app.layout = html.Div([
html.Div([
    html.Img(src='/image.png')
], style={'display': 'none'}),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Explore by City', value='tab-1'),
        dcc.Tab(label='Explore by Role', value='tab-2'),
        dcc.Tab(label='Explore by Company', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])


""" Assign Each Tab a Content """
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return cityPage.layout
    elif tab == 'tab-2':
        return rolePage.layout
    elif tab == 'tab-3':
        return companyPage.layout




if __name__ == '__main__':
    app.run_server(debug=True)