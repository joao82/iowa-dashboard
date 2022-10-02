from __future__ import annotations

import dash

dash.register_page(__name__, path='/', name='sales')

import pathlib

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from plotly.subplots import make_subplots

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

df = pd.read_csv(DATA_PATH.joinpath('liquor_iowa_2021.csv'))
df = df.dropna()

df["yyyy"] = pd.to_datetime(df["date"]).dt.year
df["mm"] = pd.to_datetime(df["date"]).dt.month
df["dd"] = pd.to_datetime(df["date"]).dt.day
df["wk"] = pd.to_datetime(df["date"]).dt.isocalendar().week

df["lon"] = df["store_location"].str.split(' ').str[1]
df["lon"] = df["lon"].str.split('(').str[1]
df["lon"].fillna(0,inplace=True)
df["lat"] = df["store_location"].str.split(' ').str[2]
df["lat"] = df["lat"].str.split(')').str[0]
df["lat"].fillna(0,inplace=True)
df["lat"] = df["lat"].astype(float)
df["lon"] = df["lon"].astype(float)

n_categories = len(df["category_name"].unique().tolist())
n_stores = len(df["store_name"].unique().tolist())
n_country = len(df["county"].unique().tolist())


season_dict = {1: 'Winter',
               2: 'Winter',
               3: 'Spring', 
               4: 'Spring',
               5: 'Spring',
               6: 'Summer',
               7: 'Summer',
               8: 'Summer',
               9: 'Fall',
               10: 'Fall',
               11: 'Fall',
               12: 'Winter'}

df['season'] = df['mm'].apply(lambda x: season_dict[x])

layout = dbc.Container(
    [
        # ======================= Title & Date Selection
        dbc.Row(
            [
                dbc.Col(
                    html.H5(
                        "Global Liquor Sales",
                        className="text-center text-info mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    html.Div(
                        dbc.Container(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label("YEAR", className="text-center text-info mb-4"),
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="year",
                                                searchable=False,
                                                multi=False,
                                                placeholder="Select year",
                                                options=[
                                                    {"label": c, "value": c}
                                                    for c in sorted(df["yyyy"].unique())
                                                ],
                                                value=2021,
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Label("MONTH", className="text-center text-info mb-4"),
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="month",
                                                searchable=False,
                                                multi=False,
                                                placeholder="Select month",
                                                options=[
                                                    {"label": "Jan", "value": 1},
                                                    {"label": "Feb", "value": 2},
                                                    {"label": "Mar", "value": 3},
                                                    {"label": "Apr", "value": 4},
                                                    {"label": "May", "value": 5},
                                                    {"label": "Jun", "value": 6},
                                                    {"label": "Jul", "value": 7},
                                                    {"label": "Aug", "value": 8},
                                                    {"label": "Sep", "value": 9},
                                                    {"label": "Oct", "value": 10},
                                                    {"label": "Nov", "value": 11},
                                                    {"label": "Dec", "value": 12},
                                                ],
                                                value=11,
                                            ),
                                        ),
                                    ],
                                    className="text-center text-info mb-4",
                                )
                            ],
                            className="period-wrapper",
                            ), className="period-wrapper"), width=6
                ),
            ],
        ),
        # ====================== Header with 6 Cards
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label(
                                    "Month Bottles Sold",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card1",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator1",
                                    className="text-center mb-0 fs-6 text",
                                ),
                            ],
                            className="text-center text-info mb-1",
                        ),
                        className="card-header",
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=2,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label(
                                    "Month Revenue",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card2",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator2",
                                    className="text-center mb-0 fs-6 text",
                                ),
                            ],
                            className="text-center text-info mb-1",
                        ),
                        className="card-header",
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=2,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label(
                                    "Month Costs",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card3",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator3",
                                    className="text-center mb-0 fs-6 text",
                                ),
                            ],
                            className="text-center text-info mb-1",
                        ),
                        className="card-header",
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=2,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label(
                                    "Month Vendors",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card4",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator4",
                                    className="text-center mb-0 fs-6 text",
                                ),
                            ],
                            className="text-center text-info mb-1",
                        ),
                        className="card-header",
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=2,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label(
                                    "Month Unique Items",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card5",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator5",
                                    className="text-center mb-0 fs-6 text",
                                ),
                            ],
                            className="text-center text-info mb-1",
                        ),
                        className="card-header",
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=2,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label(
                                    "Month Cities",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card6",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator6",
                                    className="text-center mb-0 fs-6 text",
                                ),
                            ],
                            className="text-center text-info mb-1",
                        ),
                        className="card-header",
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=2,
                ),
            ]
        ),
        # ====================== Bar Chart with Annual Sales
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.Div(id="sold_chart"))
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.Div(id="top_county")),
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                ),
            ], className='my-4'
        ),                 
        # ====================== Bar Chart vendors
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="county",
                                                searchable=False,
                                                multi=True,
                                                placeholder="County",
                                                options=df["county"]
                                                .unique()
                                                .tolist(),
                                                value=["LINN", "POLK"],
                                            ),
                                            className="mb-5",
                                            width={"size": 8, "offset": 2},
                                        ),
                                    ]
                                ),
                                dbc.Row(html.Div(id="anual_county")),
                            ]
                        )
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("TOP 3 Products", className="d-flex align-items-center text-center text-secondary mb-2"),
                                dbc.Row(
                                    dbc.Col(
                                        [
                                            html.Div(id="high_products"),
                                        ]
                                    ),
                                    className="text-center text-info mb-2",
                                ),
                                dbc.Row(
                                    dcc.Dropdown(
                                        id="product",
                                        searchable=False,
                                        multi=True,
                                        placeholder="products",
                                        options=df["item_description"]
                                        .unique()
                                        .tolist(),
                                        value=["Titos Handmade Vodka"],
                                    ),
                                    className="product-drpn",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    dbc.CardBody(
                                                        [
                                                            dbc.Label(
                                                                "Month Orders",
                                                                className="card_title text-secondary",
                                                            ),
                                                            html.H5(
                                                                id="month_orders",
                                                                className="card-text mb-0 fs-4 text",
                                                            ),
                                                            html.P(
                                                                id="orders",
                                                                className="text-center mb-0 fs-6 text",
                                                            ),
                                                        ],
                                                        className="text-center text-info mb-1",
                                                    ),
                                                    className="card-header-product",
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    dbc.CardBody(
                                                        [
                                                            dbc.Label(
                                                                "Month Stores",
                                                                className="card_title text-secondary",
                                                            ),
                                                            html.H5(
                                                                id="month_stores",
                                                                className="card-text mb-0 fs-4 text",
                                                            ),
                                                            html.P(
                                                                id="stores",
                                                                className="text-center mb-0 fs-6 text",
                                                            ),
                                                        ],
                                                        className="text-center text-info mb-1",
                                                    ),
                                                    className="card-header-product",
                                                ),
                                            ],
                                        ),
                                    ],
                                    className="my-2",
                                ),
                            ]
                        )
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                ),
            ], className='my-4'
        ),
        # ====================== Products Table
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                dbc.Row(id="products"),
                            ), className="p-3"
                        ),
                    ],
                    xs=12,
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dbc.Col(
                                [
                                dbc.Row(
                                    dcc.Dropdown(id='my_opinon',
                                                 options=['volume_sold_liters', 'volume_sold_gallons', 'bottle_volume_ml', 'sale_dollars'],
                                                 value='bottle_volume_ml', clearable=False
    )),
                                dbc.Row(
                                    dcc.Graph(id="product_season")),
                                ]
                            )
                        )
                    ), className="p-3",
                    xs=12,
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                ),
            ], className='my-4'
        )
    ],
)


# =========================== Header with 6 Cards ===============================
# -------------------------- Callback card 1 ------------------------------------
@callback(
    Output(component_id="card1", component_property="children"),
    Input(component_id="year", component_property="value"),
    Input(component_id="month", component_property="value"),
)
def update_card1(year, month):
    data3 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data3 = data3["bottles_sold"].sum()

    return html.P(f"{data3:,.0f}")


#  ------------------------- Callback card 1 INDICATOR ----------------------------
@callback(
    Output(component_id="indicator1", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month - 1)]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

    reference_month = month - 1

    if reference > 0:
        return html.P(
            f"+{reference:,.0f}%",
            style={
                "color": "rgb(102, 255, 204)",
                "font-weight": "bold",
            },
            className="card-indicator",
        )

    return html.P(
        f"{reference:,.0f}%",
        style={
            "color": "#EC1E3D",
            "font-weight": "bold",
        },
        className="card-indicator",
    )


#  ------------------------- Callback card 2 ----------------------------
@callback(
    Output(component_id="card2", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    sell = data2["sale_dollars"].sum()
    cost = data2["state_bottle_cost"].sum()
    revenue = sell - cost

    return (html.P(f" ${revenue:,.0f}"),)


#  ------------------------- Callback card 2 INDICATOR ----------------------------
@callback(
    Output(component_id="indicator2", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month - 1)]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

    reference_month = month - 1

    if reference > 0:
        return html.P(
            f"+{reference:,.2f}%",
            style={
                "color": "rgb(102, 255, 204)",
                "font-weight": "bold",
            },
            className="card-indicator",
        )

    return html.P(
        f"{reference:,.0f}%",
        style={
            "color": "#EC1E3D",
            "font-weight": "bold",
        },
        className="card-indicator",
    )


#  ------------------------- Callback card 3 ----------------------------
@callback(
    Output(component_id="card3", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    cost = data2["state_bottle_cost"].sum()

    return (html.P(f" ${cost:,.0f}"),)


#  ------------------------- Callback card 3 INDICATOR ----------------------------
@callback(
    Output(component_id="indicator3", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month - 1)]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

    reference_month = month - 1

    if reference > 0:
        return html.P(
            f"+{reference:,.2f}%",
            style={
                "color": "rgb(102, 255, 204)",
                "font-weight": "bold",
            },
            className="card-indicator",
        )

    return html.P(
        f"{reference:,.0f}%",
        style={
            "color": "#EC1E3D",
            "font-weight": "bold",
        },
        className="card-indicator",
    )


#  ------------------------- Callback card 4 ----------------------------
@callback(
    Output(component_id="card4", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data2 = len(data2["vendor_number"].unique().tolist())

    return (html.P(f"{data2:,.0f}"),)


#  ------------------------- Callback card 4 INDICATOR ----------------------------
@callback(
    Output(component_id="indicator4", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month - 1)]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

    reference_month = month - 1

    if reference > 0:
        return html.P(
            f"+{reference:,.2f}%",
            style={
                "color": "rgb(102, 255, 204)",
                "font-weight": "bold",
            },
            className="card-indicator",
        )

    return html.P(
        f"{reference:,.0f}%",
        style={
            "color": "#EC1E3D",
            "font-weight": "bold",
        },
        className="card-indicator",
    )


#  ------------------------- Callback card 5 ----------------------------
@callback(
    Output(component_id="card5", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data2 = len(data2["item_description"].unique().tolist())

    return (html.P(f"{data2:,.0f}"),)


#  ------------------------- Callback card 5 INDICATOR ----------------------------
@callback(
    Output(component_id="indicator5", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month - 1)]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

    reference_month = month - 1

    if reference > 0:
        return html.P(
            f"+{reference:,.2f}%",
            style={
                "color": "rgb(102, 255, 204)",
                "font-weight": "bold",
            },
            className="card-indicator",
        )

    return html.P(
        f"{reference:,.0f}%",
        style={
            "color": "#EC1E3D",
            "font-weight": "bold",
        },
        className="card-indicator",
    )


#  ------------------------- Callback card 6 ----------------------------
@callback(
    Output(component_id="card6", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data2 = len(data2["city"].unique().tolist())

    return (html.P(f"{data2:,.0f}"),)


#  ------------------------- Callback card 6 INDICATOR ----------------------------
@callback(
    Output(component_id="indicator6", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_card1(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] == month - 1)]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year) & (df["mm"] == month)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

    reference_month = month - 1

    if reference > 0:
        return html.P(
            f"+{reference:,.2f}%",
            style={
                "color": "rgb(102, 255, 204)",
                "font-weight": "bold",
            },
            className="card-indicator",
        )

    return html.P(
        f"{reference:,.0f}%",
        style={
            "color": "#EC1E3D",
            "font-weight": "bold",
        },
        className="card-indicator",
    )

# ----------------------------------- Header with 6 Cards ---------------------------
# ----------------------------------- Graph I ---------------------------------------
@callback(
    Output(component_id="sold_chart", component_property="children"),
    Input(component_id="year", component_property="value"),
    Input(component_id="month", component_property="value"),
)
def update_graph(year, month):

    data2 = (
        df.groupby(["yyyy", "mm"])["bottles_sold", "sale_dollars"].sum().reset_index()
    )
    data2 = data2[(data2["yyyy"] == year) & (data2["mm"] <= 12)]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=data2["mm"],
            y=data2["bottles_sold"],
            name="Total Bottles Sold",
            text=data2["bottles_sold"],
            textposition="outside",
            texttemplate="%{text:.2s}",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=data2["mm"],
            y=data2["sale_dollars"],
            name="Total Sales in $",
            marker=dict(size=12, line=dict(width=2, color="rgb(102, 255, 204)")),
            line=dict(width=2, color="rgb(102, 255, 204)"),
            text=data2["sale_dollars"],
            textposition="top right",
            textfont=dict(color="rgb(102, 255, 204)"),
            mode="lines+markers+text",
            texttemplate="%{text:.2s}",
        ),
        secondary_y=True,
    )

    fig.update_traces(marker_color="rgb(33, 60, 99)")

    fig.update_layout(
        height=315,
        margin=dict(l=20, r=30, t=30, b=30),
        plot_bgcolor="rgb(0,0,0,0)",
        legend_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgb(0,0,0,0)",
        font_color="#909090",
        hovermode="closest",
        xaxis_title="Months",
        yaxis_title="Total of Bottles Sold",
        legend=dict(yanchor="top", y=1.4, xanchor="left", x=0),
        title={
            "text": "Bottles Sold vs Revenue",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    fig["data"][0]["marker"]["color"] = ["#E74C3C" if c == month else "#2C3E50" for c in fig["data"][0]["x"]]
    
    return html.Div(dcc.Graph(figure=fig), id="sold_chart")


#  ---------------------------- Graph II -------------------------------------
@callback(
    Output(component_id="top_county", component_property="children"),
    Input(component_id="year", component_property="value"),
    Input(component_id="month", component_property="value"),
)
def update_graph(year, month):

    data2 = df[(df["yyyy"] == year) & (df["mm"] <= (month + 1))]
    data2 = data2.groupby(["county"])["bottles_sold"].sum().reset_index()
    data_new = data2.sort_values(by=["bottles_sold"], ascending=True).iloc[-5:]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=data_new["bottles_sold"],
            y=data_new["county"],
            name="yaxis data",
            orientation="h",
        ),
        secondary_y=False,
    )

    fig.update_traces(
        marker_color="rgb(33, 60, 99)",
    )

    fig.update_layout(
        height=315,
        margin=dict(l=20, r=30, t=50, b=30),
        plot_bgcolor="rgb(0,0,0,0)",
        legend_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgb(0,0,0,0)",
        font_color="#909090",
        hovermode="closest",
        title={
            "text": "Top 5 Counties",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    fig.for_each_trace(
        lambda trace: trace.update(marker_color="#9D3469") if trace == month else (),
    )

    return html.Div(dcc.Graph(figure=fig), id="top_county")


# =========================== Bar Chart Vendor
# ----------------------------------- Graph I ---------------------------------------
@callback(
    Output(component_id="anual_county", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
        Input(component_id="county", component_property="value"),
    ],
)
def update_graph(year, month, county):

    data2 = (
        df.groupby(
            [
                "yyyy",
                "mm",
                "county",
            ]
        )["bottles_sold"]
        .sum()
        .reset_index()
    )

    data2 = data2[(data2["yyyy"] == year) & (data2["mm"] <= 12)]
    data2 = data2[data2["county"].isin(county)]

    data3 = df.groupby(["yyyy", "mm"])["bottles_sold"].sum().reset_index()
    data3 = data3[(data3["yyyy"] == year) & (data3["mm"] <= 12)]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=data2["mm"],
            y=data2["bottles_sold"],
            name="Total Bottles Sold",
            text=data2["bottles_sold"],
            textposition="outside",
            texttemplate="%{text:.2s}",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=data3["mm"],
            y=data3["bottles_sold"],
            name="total Sales in $",
            marker=dict(
                size=12,
                line=dict(
                    width=2,
                    color="#FFA500",
                ),
            ),
            line=dict(width=2, color="#FFA500"),
            text=data3["bottles_sold"],
            textposition="top right",
            textfont=dict(color="#E58606"),
            mode="lines+markers+text",
            texttemplate="%{text:.2s}",
        ),
        secondary_y=False,
    )

    fig.update_traces(
        marker_color="rgb(33, 60, 99)",
    )

    fig.update_layout(
        height=315,
        margin=dict(l=20, r=30, t=50, b=30),
        plot_bgcolor="rgb(0,0,0,0)",
        legend_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgb(0,0,0,0)",
        font_color="#909090",
        hovermode="closest",
        xaxis_title="Months",
        yaxis_title="Total of Bottles Sold by County",
        legend=dict(yanchor="top", y=1.4, xanchor="left", x=0),
        title={
            "text": "Total of Bottles Sold by County",
            "y": 0.98,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    fig["data"][0]["marker"]["color"] = ["#E74C3C" if c == month else "#2C3E50" for c in fig["data"][0]["x"]]

    return html.Div(dcc.Graph(figure=fig), id="anual_county")


# ----------------------------------- Card 1 ---------------------------------------
@callback(
    Output(component_id="month_orders", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
        Input(component_id="product", component_property="value"),
    ],
)
def update_graph(year, month, product):

    data2 = (
        df.groupby(["yyyy", "mm", "item_description"])["invoice_and_item_number"]
        .count()
        .reset_index()
    )
    data2 = data2[(data2["yyyy"] == year) & (data2["mm"] == month)]
    data2 = data2[data2["item_description"].isin(product)]
    month_orders = data2["invoice_and_item_number"].sum()

    return html.P(f"{month_orders:,.0f}")


# ------
@callback(
    Output(component_id="orders", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
        Input(component_id="product", component_property="value"),
    ],
)
def update_graph(year, month, product):

    data2 = (
        df.groupby(["yyyy", "mm", "item_description"])["invoice_and_item_number"]
        .count()
        .reset_index()
    )
    data2 = data2[(data2["yyyy"] == year) & (data2["mm"] <= (month))]
    data2 = data2[data2["item_description"].isin(product)]
    orders = data2["invoice_and_item_number"].sum()

    return html.P(
        f"{orders:,.0f} orders",
        style={
            "color": "rgb(102, 255, 204)",
            "font-weight": "bold",
        },
        className="card-indicator",
    )


# ----------------------------------- Card 2 ---------------------------------------
@callback(
    Output(component_id="month_stores", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
        Input(component_id="product", component_property="value"),
    ],
)
def update_graph(year, month, product):

    data2 = (
        df.groupby(["yyyy", "mm", "item_description"])["store_name"]
        .count()
        .reset_index()
    )
    data2 = data2[(data2["yyyy"] == year) & (data2["mm"] == month)]
    data2 = data2[data2["item_description"].isin(product)]
    month_stores = data2["store_name"].sum()

    return html.P(f"{month_stores:,.0f}")


# ---------
@callback(
    Output(component_id="stores", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
        Input(component_id="product", component_property="value"),
    ],
)
def update_graph(year, month, product):

    data2 = (
        df.groupby(["yyyy", "mm", "item_description"])["store_name"]
        .count()
        .reset_index()
    )
    data2 = data2[(data2["yyyy"] == year) & (data2["mm"] <= month)]
    data2 = data2[data2["item_description"].isin(product)]
    stores = data2["store_name"].sum()

    return html.P(
        f"{stores:,.0f} stores",
        style={
            "color": "rgb(102, 255, 204)",
            "font-weight": "bold",
        },
        className="card-indicator",
    )


#  ------------- PRODUCT 1 -----------
@callback(
    Output(component_id="high_products", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
    ],
)
def update_graph(year):
    data2 = df[(df["yyyy"] == year)]
    data2 = data2.groupby(["item_description"])["sale_dollars"].sum().reset_index()
    product1 = data2.sort_values(by=["sale_dollars"], ascending=True).iloc[-1:]
    product1_name = product1.values.tolist()[0][0]
    product1_value = product1.values.tolist()[0][1]
    

    product2 = data2.sort_values(by=["sale_dollars"], ascending=True).iloc[-2:]
    product2_name = product2.values.tolist()[0][0]
    product2_value = product2.values.tolist()[0][1]

    product3 = data2.sort_values(by=["sale_dollars"], ascending=True).iloc[-3:]
    product3_name = product3.values.tolist()[0][0]
    product3_value = product3.values.tolist()[0][1]

    return html.Div(
        [
            dbc.Row(html.P(f"{product1_name} (${product1_value:,.0f})")),
            dbc.Row(html.P(f"{product2_name} (${product2_value:,.0f})")),
            dbc.Row(html.P(f"{product3_name} (${product3_value:,.0f})")),
        ], className="high_products"
        )


#  ---------------------------- Products Table -----------------------------------
#  ---------------------------- Table Row 1 -------------------------------------
@callback(
    Output(component_id="products", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="month", component_property="value"),
    ],
)
def update_graph(year, month):
    data2 = df[(df["yyyy"] == year) & (df["mm"] <= month)]

    data2 = (
        data2.groupby(["item_description"])[["sale_dollars", "bottles_sold"]]
        .sum()
        .reset_index()
    )
    data2["perc"] = (data2["sale_dollars"] / (data2["sale_dollars"].sum()) * 100).round(
        2
    )
    data2.sort_values(by=["sale_dollars"], ascending=True)[-1:]
    products = data2.sort_values(by=["sale_dollars"], ascending=True)[-8:]

    return html.Div(
        dbc.Table.from_dataframe(products, striped=True, bordered=False, hover=True)
    )


#  ---------------------------- Pie Chart I -------------------------------------
@callback(
    Output(component_id="product_season", component_property="figure"),
    Input(component_id="year", component_property="value"),
    Input(component_id="product", component_property="value"),
    Input(component_id="my_opinon", component_property="value"),
    
)
def update_graph(year, product, radio):
    data2 = df[(df["yyyy"] == 2021)]
    data2 = data2[(data2["item_description"].isin(product))]

    fig = px.pie(data2, values=radio, names='season', hole=.3, color_discrete_sequence=px.colors.sequential.RdBu,
                 title="% consumption per season")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide', 
                      annotations=[dict(text="Seasons",x=0.5, y=0.5, font_size=12, showarrow=False)])
    

    return fig
