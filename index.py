import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from apps.rolePage import returnRolePage
from apps.companyPage import returnCompanyPage
from apps.cityPage import returnCityPage




""" App """
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets=external_stylesheets
app = dash.Dash(__name__)


""" Define Layout with three tabs"""

app.layout = html.Div([
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
        return returnCityPage()
    elif tab == 'tab-2':
        return returnRolePage()
    elif tab == 'tab-3':
        return returnCompanyPage()


if __name__ == '__main__':
    app.run_server(debug=True)