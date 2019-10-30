import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

""" Data -> was scraped for 2019 but as it turns out when request was made for 
the company that did not have any visa applications in 2019 - the code automatically 
scrapped the data for 2018 (or the last available data for that company) """
""" this is likely to impact only small companies, and therefore here we only analyse the
results from 2019 """
""" Future project ideas -> to scrap outstanding data and compare which companies/industries apply and get visa
e.g. how random is the random lottery """


""" Import Data """
df = pd.read_csv(r"data/h1b19_clean.csv")

""" CITY PAGE """
""" Data clean and transform """


def create_scatter(salary_choice):
    x = df.groupby("city").agg({"company": "count",
                                "base_salary": salary_choice}).sort_values(by="company",
                                                    ascending=False)[:500]["company"].values

    y = df.groupby("city").agg({"company": "count",
                                "base_salary": salary_choice}).sort_values(by="company",
                                                    ascending=False)[:500]["base_salary"].values

    name = df.groupby("city").agg({"company": "count",
                                     "base_salary": salary_choice}).sort_values(by="company",
                                                    ascending=False)[:500].index.tolist()
    return {
        'data': [go.Scatter(
            x=x,
            y=y,
            text=[i for i in name],
            customdata=name,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.8,
                'line': {'width': 0.5, 'color': 'black'},
                'color': '#f35588',
            }
        )],
        'layout': go.Layout(
            xaxis={'automargin': True,
                'title': "count"
            },
            yaxis={'automargin': True,
                'title': salary_choice + " salary"
            },
            margin={'l': 60, 'b': 50, 't': 50, 'r': 20},
            height=420,
            hovermode='closest',
        )
    }


def create_top_comp_analysis(city, salary_choice):
    top_companies = df[df.city == city].groupby("company").count()[\
                        "job_title"].sort_values(ascending=\
                                                         False)[:20].index.tolist()
    dff = df[(df.company.isin(top_companies)) & (df.city == city)].drop(["state", "city"], axis=1)
    dff_gp = dff.groupby("company").agg( \
        {"job_title": "count", "base_salary": salary_choice} \
        ).rename(columns={"job_title": "count"}).sort_values(by="count", ascending=False)

    dff_gp = dff_gp.sort_values(by="count")
    x = dff_gp.index
    y_count = dff_gp["count"].values
    y_choice = dff_gp["base_salary"].values
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    fig.append_trace(go.Bar(
        x=y_count,
        y=x,
        marker=dict(
            color='#71a95a',
            line=dict(
                color='#71a95a',
                width=1),
        ),
        name='Roles Count',
        orientation='h',
        width=0.4,
    ), 1, 1)

    fig.append_trace(go.Scatter(
        x=y_choice, y=x,
        mode='lines+markers',
        line_color='#f35588',
        name= salary_choice + ' salary',
    ), 1, 2)

    fig.update_layout(
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0.03, 0.82],

        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            showticklabels=False,
            linecolor='rgba(102, 102, 102, 0.8)',
            linewidth=2,
            domain=[0, 0.85],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0, 0.42],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0.47, 1],
            side='top',
            dtick=25000,
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        paper_bgcolor="white",
        plot_bgcolor='white',
        height=700,

    )
    annotations = []
    y_s = np.round(y_count, decimals=2)
    y_nw = np.rint(y_choice)

    # Adding labels
    for ydn, yd, xd in zip(y_nw, y_s, x):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ydn - 20000,
                                text='{:,}'.format(ydn),
                                font=dict(family='Arial', size=12,
                                          color='rgb(128, 0, 128)'),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + 10,
                                text=str(yd),
                                font=dict(family='Arial', size=10,
                                          color='rgb(50, 171, 96)'),
                                showarrow=False))

    # fig.update_layout(annotations=annotations)
    return fig.to_dict()
# create_top_comp_analysis("NEW YORK", "mean")


"""" Footer is the same on all pages - Store code here """
def returnFooter():
    return html.Div([
        html.A('LinkedIn', href='https://www.linkedin.com/in/jelenalor/', target="_blank",
                 style={'font-weight': 'bold',
                        'color': 'white',
                        'padding': '5px 10px 10px'}),
        html.A('GitHub', href='https://github.com/jelenalor', target="_blank",
                 style={'font-weight': 'bold',
                        'color': 'white',
                        'padding': '5px 10px 10px'}),
        html.P('Copyright 2019  Jelena Lor', style={'display': 'inline-block',
                                    'padding': '10px 0 0 400px',
                                    'color': 'white',
                                    'margin-bottom': 0})

                     ], style={'height': '50px',
                               'background-color': '#007944',
                               'margin': 0,
                               'margin-bottom': 0,
                               })

