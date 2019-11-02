import pandas as pd
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots


""" Data -> was scraped for 2019 but as it turns out when request was made for 
the company that did not have any visa applications in 2019 - the code automatically 
scrapped the data for 2018 (or the last available data for that company) """
""" this is likely to impact only small companies, and therefore here we only analyse the
results from 2019 """
""" Future project ideas -> to scrap outstanding data and compare which companies/industries apply and get visa
e.g. how random is the random lottery """

ctags = {1: "#f35588",
         2: "#ffbbb4",
         3: "#71a95a",
         4: "#007944"}

""" Import Data """
df = pd.read_csv(r"data/h1b19_clean.csv")
"""Some base salary shows less than 20k, which is likely to be contractor etc job, remove these instances"""
df = df[df["base_salary"] >20000]

""" CITY PAGE """
""" Data clean and transform """

name = df.groupby("city").agg({"company": "count"}).sort_values(by="company",
                                                    ascending=False)[:500].index.tolist()


key_title_tokens = ["engin", "develop", "architect", "administr",
                        "account", "auditor", "analyst", "manag", "consult", "associ",
                        "presid", "programm"]


def create_scatter(salary_choice, city):
    x = df.groupby("city").agg({"company": "count",
                                "base_salary": salary_choice}).sort_values(by="company",
                                                    ascending=False)[:500]["company"].values

    y = df.groupby("city").agg({"company": "count",
                                "base_salary": salary_choice}).sort_values(by="company",
                                                    ascending=False)[:500]["base_salary"].values

    name = df.groupby("city").agg({"company": "count",
                                     "base_salary": salary_choice}).sort_values(by="company",
                                                    ascending=False)[:500].index.tolist()

    x_click = df[df.city == city].shape[0]
    y_click = df[df.city == city].agg({"base_salary": salary_choice})[0]
    name_click = city

    traces = []

    traces.append(go.Scatter(
            x=x,
            y=y,
            text=[i for i in name],
            customdata=name,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.8,
                'line': {'width': 0.5, 'color': 'black'},
                'color': ctags[1],}
        ))

    traces.append(go.Scatter(
        x=[x_click],
        y=[y_click],
        text=[name_click],
        customdata=[name_click],
        mode='markers',
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'black'},
            'color': ctags[3]}
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'automargin': True,
                'title': "number of roles per city",
            },
            yaxis={'automargin': True,
                'title': salary_choice + " salary per city"
            },
            margin={'l': 60, 'b': 50, 't': 50, 'r': 20},
            height=420,
            hovermode='closest',
            showlegend=False,
        )
    }


def getDataTopComp(city, salary_choice):
    top_companies = df[df.city == city].groupby("company").count()["job_title"].sort_values(ascending=False)[
                    :20].index.tolist()
    dff = df[df.company.isin(top_companies)].drop(["state", "city"], axis=1)
    dff_gp = dff.groupby("company").agg( \
        {"job_title": "count", "base_salary": salary_choice} \
        ).rename(columns={"job_title": "count"}).sort_values(by="count", ascending=False)

    dff_gp = dff_gp.sort_values(by="count")
    x = dff_gp.index.values
    y_count = dff_gp["count"].values
    y_choice = dff_gp["base_salary"].values
    return city, salary_choice, x, y_count, y_choice


def createMultiGraph(items, y_click):
    city, salary_choice, x, y_count, y_choice = items
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    zipped = list(zip(y_count, x, y_choice))
    y_count, x, y_choice = zip(*sorted(zipped))
    y_count = list(y_count)
    x = list(x)
    y_choice = list(y_choice)

    if y_click == "None":
        fig.append_trace(go.Bar(
            x=y_count,
            y=x,
            marker=dict(
                color=ctags[3],
                line=dict(
                    color=ctags[3],
                    width=1),
            ),
            name='Roles Count',
            orientation='h',
            width=0.4,
        ), 1, 1)
    else:
        # Selected
        y_cl = y_count.pop(x.index(y_click))
        x_cl = x.pop(x.index(y_click))
        fig.append_trace(go.Bar(
            x=[y_cl],
            y=[x_cl],
            marker=dict(
                color=ctags[1],
                line=dict(
                    color=ctags[1],
                    width=1),
            ),
            name='Roles Count - Selected',
            orientation='h',
            width=0.4,
        ), 1, 1)
        # Not Selected
        fig.append_trace(go.Bar(
            x=y_count,
            y=x,
            marker=dict(
                color=ctags[3],
                line=dict(
                    color=ctags[3],
                    width=1),
            ),
            name='Roles Count',
            orientation='h',
            width=0.4,
        ), 1, 1)

    fig.append_trace(go.Scatter(
        x=list(y_choice), y=list(x),
        mode='lines+markers',
        line_color=ctags[1],
        name=salary_choice + ' salary',
    ), 1, 2)

    fig.update_layout(
        title=dict(text=city, font=dict(
            size=20,
            family='Comic Sans MS',
            color=ctags[1]
        )),
        
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

    return fig.to_dict()


"""" Roles Analsys """
"""Support Function"""


def getTokenSummary(dff, key_title_tokens):
    index_dict = {}
    for ind, row in enumerate(dff["tokens"]):
        try:
            for k in key_title_tokens:
                if k in row.split():
                    if k not in index_dict.keys():
                        index_dict[k] = []
                    index_dict[k].append(ind)
        except Exception:
            pass

    # structure - > key -> all -> [count, mean, min, max] , different title names -> keep top 10 roles and how many it represents
    result_dict = {}
    for k in index_dict.keys():
        df_temp = dff.iloc[index_dict[k]]
        result_dict[k] = {}
        # total
        my_list = [df_temp.shape[0], int(df_temp["base_salary"].mean()),
                   int(df_temp["base_salary"].min()),
                   int(df_temp["base_salary"].max())]
        result_dict[k]["all"] = my_list

        # by job_title type -> top 10
        top_roles = df_temp.groupby("tokens").agg({"company": "count", }).sort_values(by="company", ascending=False)[
                    :10].index.tolist()
        top_roles_perc = round(df_temp.groupby("tokens").agg( \
            {"company": "count"} \
            ).sort_values(by="company", \
                          ascending=False)[:10].company.sum() / df_temp.shape[0], 2)
        top_roles.append(top_roles_perc)
        result_dict[k]["top_roles"] = top_roles

    return result_dict


def dataForTopRoles(city, salary_choice):
    dff = df[df.city == city]
    tokens_summary = getTokenSummary(dff, key_title_tokens)
    x = [i for i in key_title_tokens]
    y_count = [tokens_summary[i]["all"][0] if i in tokens_summary.keys() else 0 for i in x]
    y_choice = [tokens_summary[i]["all"][1] if salary_choice == "mean"
                                               and i in tokens_summary.keys()
                    else tokens_summary[i]["all"][2] if salary_choice == "min"
                                                        and i in tokens_summary.keys()
                    else tokens_summary[i]["all"][3] if i in tokens_summary.keys() else 0
                        for i in x]

    return city, salary_choice, x, y_count, y_choice


def createBoxPlot(city, role):
    dff = df[df.city == city]
    tokens_summary = getTokenSummary(dff, key_title_tokens)
    x = dff[dff.tokens.isin(tokens_summary[role]["top_roles"][:-1])]["tokens"].unique()
    traces = []
    for r in x:
        traces.append(go.Box(y=dff[dff.tokens == r]["base_salary"],
                         name=r, marker={"size": 4, "color": ctags[1]}))

    return {"data": traces,
            "layout": go.Layout(autosize=True,
                                title=dict(text=role,
                                           font=dict(
                                               size=20,
                                               family='Comic Sans MS',
                                               color=ctags[1])),
                                margin={"l": 50, "b": 200, "r": 20, "t": 40},
                                xaxis={"showticklabels": True},
                                yaxis={"title": "Salary Distribution"},
                                showlegend=False)}


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
        html.P('© Copyright Jelena Lor 2019. All Rights Reserved.', style={'display': 'inline-block',
                                    'position': 'absolute',
                                    'left': '40%',
                                    'color': 'white',
                                    'margin-bottom': 0}),
        html.P('All data is from https://h1bdata.info/', style={'display': 'inline-block',
                                                                           'position': 'absolute',
                                                                           'right': '5%',
                                                                           'color': 'white',
                                                                           'margin-bottom': 0})

                     ], style={'height': '50px',
                               'background-color': ctags[4],
                               'margin': 0,
                               'margin-bottom': 0,
                               })

