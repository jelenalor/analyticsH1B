import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from udfs.udf import getTokenSummary
from udfs.udf import key_title_tokens

""" Import Data """
df = pd.read_csv(r"data/h1b19_clean.csv")
tokens_summary = getTokenSummary(df, key_title_tokens)


def dataForRoles(role):
    x = tokens_summary[role]["top_roles"][:-1]
    dff = df[df.tokens.isin(x)]

    # Roles
    y_count_roles = dff.groupby("tokens").agg({"job_title": "count",
                                          "base_salary": "mean"})["job_title"].values
    y_choice_roles = dff.groupby("tokens").agg({"job_title": "count",
                                          "base_salary": "mean"})["base_salary"].values

    # Locations
    loc_dff = dff.groupby("city").agg({"job_title": "count",
                                       "base_salary": "mean"}).sort_values(by="job_title",
                                                                           ascending=False)[:20]
    x_loc = loc_dff.index.tolist()
    y_count_loc = loc_dff["job_title"].values
    y_choice_loc = loc_dff["base_salary"].values

    # Companies
    loc_dff_comp = dff.groupby("company").agg({"job_title": "count",
                                       "base_salary": "mean"}).sort_values(by="job_title",
                                                                           ascending=False)[:20]
    x_comp = loc_dff_comp.index.tolist()
    y_count_comp = loc_dff_comp["job_title"].values
    y_choice_comp = loc_dff_comp["base_salary"].values

    return ((role, x, y_count_roles, y_choice_roles),
            (role, x_loc, y_count_loc, y_choice_loc),
            (role, x_comp, y_count_comp, y_choice_comp))


def createMultiGraphRoles(items, height):
    role, x, y_count, y_choice = items
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    zipped = list(zip(y_count, x, y_choice))
    y_count, x, y_choice = zip(*sorted(zipped))
    y_count = list(y_count)
    x = list(x)
    y_choice = list(y_choice)

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
        x=list(y_choice), y=list(x),
        mode='lines+markers',
        line_color='#f35588',
        name='mean salary',
    ), 1, 2)

    fig.update_layout(
        title=dict(text=role, font=dict(
            size=20,
            family='Comic Sans MS',
            color="#f35588"
        )),

        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0.02, 0.83],

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
        height=height,

    )

    return fig.to_dict()
