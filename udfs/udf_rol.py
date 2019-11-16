import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from udfs.udf import getTokenSummary
from udfs.udf import key_title_tokens
from udfs.udf import ctags

""" Import Data """


def dataForRoles(role):
    dff_roles = pd.read_csv(r"data/%s/dff_roles.csv" % role, index_col="tokens")
    loc_dff = pd.read_csv(r"data/%s/loc_dff.csv" % role, index_col="city")
    loc_dff_comp = pd.read_csv(r"data/%s/loc_dff_comp.csv" % role, index_col="company")


    x = dff_roles.index.tolist()
    y_count_roles = dff_roles["count"].values
    y_mean_roles = dff_roles["mean"].values
    y_max_roles = dff_roles["max"].values
    y_min_roles = dff_roles["min"].values


    x_loc = loc_dff.index.tolist()
    y_count_loc = loc_dff["count"].values
    y_mean_loc = loc_dff["mean"].values
    y_max_loc = loc_dff["max"].values
    y_min_loc = loc_dff["min"].values

    # Companies

    x_comp = loc_dff_comp.index.tolist()
    y_count_comp = loc_dff_comp["count"].values
    y_mean_comp = loc_dff_comp["mean"].values
    y_max_comp  = loc_dff_comp["max"].values
    y_min_comp = loc_dff_comp["min"].values

    return ((role, x, y_count_roles, y_mean_roles, y_max_roles, y_min_roles),
            (role, x_loc, y_count_loc, y_mean_loc, y_max_loc, y_min_loc),
            (role, x_comp, y_count_comp, y_mean_comp, y_max_comp, y_min_comp))


def createMultiGraphRoles(items, height):
    role, x, y_count, y_mean, y_max, y_min = items
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    zipped = list(zip(y_count, x, y_mean, y_max, y_min))
    y_count, x, y_mean, y_max, y_min = zip(*sorted(zipped))
    y_count = list(y_count)
    x = list(x)
    y_mean = list(y_mean)
    y_max = list(y_max)
    y_min = list(y_min)

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
        x=list(y_min), y=list(x),
        mode='lines+markers',
        line_color=ctags[3],
        name='min salary',
    ), 1, 2)

    fig.append_trace(go.Scatter(
        x=list(y_mean), y=list(x),
        mode='lines+markers',
        line_color=ctags[1],
        name='mean salary',
        fill='tonexty',
    ), 1, 2)

    fig.append_trace(go.Scatter(
        x=list(y_max), y=list(x),
        mode='lines+markers',
        line_color=ctags[4],
        name='max salary',
        fill='tonexty',
    ), 1, 2)

    fig.update_layout(
        title=dict(text=role, font=dict(
            size=20,
            family='Comic Sans MS',
            color=ctags[1]
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
            domain=[0, 0.10],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0.12, 1],
            side='top',
            dtick=50000,
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        paper_bgcolor="white",
        plot_bgcolor='white',
        height=height,
        width=1200

    )

    return fig.to_dict()
