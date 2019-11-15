import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from udfs.udf import getTokenSummary
from udfs.udf import key_title_tokens
from udfs.udf import ctags

""" Import Data """
df = pd.read_csv(r"data/h1b19_clean.csv")
tokens_summary = getTokenSummary(df, key_title_tokens)
name = df.groupby("company").agg({"city": "count",
                                     "base_salary": "mean"}).sort_values(by="city",
                                                    ascending=False)[:500].index.tolist()


def create_scatter_comp(comp):
    x = df.groupby("company").agg({"city": "count",
                                "base_salary": "mean"}).sort_values(by="city",
                                                    ascending=False)[:500]["city"].values

    y = df.groupby("company").agg({"city": "count",
                                "base_salary": "mean"}).sort_values(by="city",
                                                    ascending=False)[:500]["base_salary"].values

    name = df.groupby("company").agg({"city": "count",
                                     "base_salary": "mean"}).sort_values(by="city",
                                                    ascending=False)[:500].index.tolist()

    x_click = df[df.company == comp].shape[0]
    y_click = df[df.company == comp].agg({"base_salary": "mean"})[0]
    name_click = comp
    traces = []
    traces.append(go.Scatter(
            x=x,
            y=y,
            text=[i for i in name],
            customdata=name,
            mode='markers',
            name="",
            marker={
                'size': 15,
                'opacity': 0.8,
                'line': {'width': 0.5, 'color': 'black'},
                'color': ctags[1]}
        ))

    traces.append(go.Scatter(
        x=[x_click],
        y=[y_click],
        text=[name_click],
        customdata=[name_click],
        mode='markers',
        name="",
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'black'},
            'color': ctags[3]}
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'automargin': True,
                'title': "number of jobs per company",
            },
            yaxis={'automargin': True,
                'title': "mean salary per company"
            },
            margin={'l': 60, 'b': 50, 't': 50, 'r': 20},
            height=420,
            hovermode='closest',
            showlegend=False,
        )
    }


def createBoxPlot(comp):
    dff = df[df.company == comp]
    x = dff.groupby("tokens").count().sort_values(by="company", ascending=False)[:20].index.tolist()
    traces = []
    for r in x:
        traces.append(go.Box(y=dff[dff.tokens == r]["base_salary"],
                         name=r, marker={"size": 4, "color": ctags[3]}))

    return {"data": traces,
            "layout": go.Layout(autosize=True,
                                margin={"l": 50, "b": 200, "r": 20, "t": 40},
                                xaxis={"showticklabels": True, "title": "Top 20 job titles by count"},
                                yaxis={"title": "Salary Distribution"},
                                showlegend=False,
                                title=dict(text=comp,
                                        font=dict(
                                            size=20,
                                            family='Comic Sans MS',
                                            color=ctags[1])),
                                height=500)}


def getDataComp(comp):
    top_loc = df[df.company == comp].groupby("city").count()["job_title"].sort_values(ascending=False)[
                    :20].index.tolist()
    dff = df[(df.city.isin(top_loc) & (df.company == comp))].drop(["state"], axis=1)
    dff_gp = dff.groupby("city", as_index=False).agg(["count", "min", "mean", "max"]).sort_values(
        by=("base_salary", "count"), ascending=False)
    dff_gp.columns = dff_gp.columns.get_level_values(1)

    dff_gp = dff_gp.sort_values(by="count")
    x = dff_gp.index.values
    y_count = dff_gp["count"].values
    y_min = dff_gp["min"].values
    y_mean = dff_gp["mean"].values
    y_max = dff_gp["max"].values

    min_text = [tuple(dff[(dff.base_salary == i) & \
                          (dff.city==j)].iloc[0][["job_title"]].values) for i, j in zip(y_min, x)]
    max_text = [tuple(dff[(dff.base_salary == i) & \
                          (dff.city==j)].iloc[0][["job_title"]].values) for i, j in zip(y_max, x)]

    return comp, x, y_count, y_min, y_mean, y_max, min_text, max_text


def createMultiGraphComp(items):
    comp, x, y_count, y_min, y_mean, y_max, min_text, max_text = items

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    zipped = list(zip(y_count, x, y_min, y_mean, y_max))
    y_count, x, y_min, y_mean, y_max = zip(*sorted(zipped))
    y_count = list(y_count)
    x = list(x)
    y_min = list(y_min)
    y_mean = list(y_mean)
    y_max = list(y_max)

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
        hoveron='points',
        text=min_text,
        hoverinfo='text+x+y'
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
        hoveron='points',
        text=max_text,
        hoverinfo='text+x+y'
    ), 1, 2)


    fig.update_layout(
        title=dict(text=comp, font=dict(
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
        height=600,
        width=1400

    )

    return fig.to_dict()
