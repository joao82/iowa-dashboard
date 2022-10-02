import dash

dash.register_page(__name__, path='/finance', name='finance')

import pathlib

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html
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
                        "Iowa Liquor Finance Analysis",
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
                                    "Annual Revenue",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card9",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator9",
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
                                    "Annual Costs",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card10",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator10",
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
                                    "Annual Bottle Sold",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card11",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator11",
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
                                    "Total Vendors",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card12",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator12",
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
                                    "Total Orders",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card13",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator13",
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
                                    "Total Products",
                                    className="card_title text-secondary",
                                ),
                                html.P(
                                    id="card14",
                                    className="card-text mb-0 fs-4 text",
                                ),
                                html.P(
                                    id="indicator14",
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
        # ====================== Bar Chart with Annual Financial
        dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.Div(id="annual_financial"))
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=12,
                    xl=12,
                ), className='my-4'
        ),                 
        # ====================== Bar Chart vendors
        dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dbc.Row(html.Div(id="anual_products")),
                        )
                    ),
                    xs=12,
                    sm=12,
                    md=12,
                    lg=12,
                    xl=12,
                ), className='my-4'
        ),
    ],
)

# -------------------------- Header with 6 Cards
#  ------------------------- Callback card 9 - Annual Revenue ----------------------------
@callback(
    Output(component_id="card9", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data2 = df[(df["yyyy"] == year)]
    sell = data2["sale_dollars"].sum()
    cost = data2["state_bottle_cost"].sum()
    revenue = sell - cost

    return (html.P(f" ${revenue:,.0f}"),)


#  ------------------------- Callback card 9 - Annual Revenue Indicator ----------------------------
@callback(
    Output(component_id="indicator9", component_property="children"),
    Input(component_id="year", component_property="value")
)
def update_card1(year):
    data2 = df[(df["yyyy"] == (year-1))]
    data2 = data2["sale_dollars"].sum()
    
    data3 = df[(df["yyyy"] == year)]
    data3 = data3["sale_dollars"].sum()


    reference = (data3 - data2) / data2 * 100

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


#  ------------------------- Callback card 10 - Annual Costs ----------------------------
@callback(
    Output(component_id="card10", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data2 = df[(df["yyyy"] == year)]
    cost = data2["state_bottle_cost"].sum()

    return (html.P(f" ${cost:,.0f}"),)


#  ------------------------- Callback card 10 - Annual Costs INDICATOR ----------------------------
@callback(
    Output(component_id="indicator10", component_property="children"),
    [
        Input(component_id="year", component_property="value"),
    ],
)
def update_card1(year):
    data2 = df[(df["yyyy"] == (year-1))]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

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


# -------------------------- Callback card 11 - Annual Bottles Sold ----------------------------
@callback(
    Output(component_id="card11", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data3 = df[(df["yyyy"] == year)]
    data3 = data3["bottles_sold"].sum()

    return html.P(f"{data3:,.0f}")


#  ------------------------- Callback card 11 - Annual Bottles Sold INDICATOR ----------------------------
@callback(
    Output(component_id="indicator11", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data2 = df[(df["yyyy"] == (year-1))]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

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


#  ------------------------- Callback card 12 - Total vendors ----------------------------
@callback(
    Output(component_id="card12", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data2 = df[(df["yyyy"] == year)]
    data2 = len(data2["vendor_number"].unique().tolist())

    return (html.P(f"{data2:,.0f}"),)


#  ------------------------- Callback card 12 - Total vendors INDICATOR ----------------------------
@callback(
    Output(component_id="indicator12", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data2 = df[(df["yyyy"] == (year-1))]
    data2 = data2["bottles_sold"].sum()

    data3 = df[(df["yyyy"] == year)]
    data3 = data3["bottles_sold"].sum()

    reference = (data3 - data2) / data2 * 100

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


#  ------------------------- Callback card 13 - Total Orders ----------------------------
@callback(
    Output(component_id="card13", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data2 = df[(df["yyyy"] == year)]
    data2 = data2["invoice_and_item_number"].count()

    return (html.P(f"{data2:,.0f}"),)


#  ------------------------- Callback card 13 - Total Orders INDICATOR ----------------------------
@callback(
    Output(component_id="indicator13", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data2 = df[(df["yyyy"] == (year-1))]
    data2 = data2["invoice_and_item_number"].count()

    data3 = df[(df["yyyy"] == year)]
    data3 = data3["invoice_and_item_number"].count()

    reference = (data3 - data2) / data2 * 100


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


#  ------------------------- Callback card 14 - total Products ----------------------------
@callback(
    Output(component_id="card14", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_card1(year):
    data2 = df[(df["yyyy"] == year)]
    data2 = len(data2["item_description"].unique().tolist())

    return (html.P(f"{data2:,.0f}"),)


#  ------------------------- Callback card 14 - total Products INDICATOR ----------------------------
@callback(
    Output(component_id="indicator14", component_property="children"),
    Input(component_id="year", component_property="value"),

)
def update_card1(year):
    data2 = df[(df["yyyy"] == (year-1)) ]
    data2 = len(data2["item_description"].unique().tolist())

    data3 = df[(df["yyyy"] == year) ]
    data3 = len(data3["item_description"].unique().tolist())

    reference = (data3 - data2) / data2 * 100

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


# ----------------------------------- Bar Chart with Annual Financial ---------------------------
# ----------------------------------- Graph I ---------------------------------------
@callback(
    Output(component_id="annual_financial", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_graph(year):

    data2 = (
        df.groupby(["yyyy", "wk"])["bottles_sold", "sale_dollars"].sum().reset_index()
    )
    data2 = data2[(data2["yyyy"] == year)]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=data2["wk"],
            y=data2["sale_dollars"],
            name="Annual Iowa Liquor Revenue",
            text=data2["sale_dollars"],
            textposition="outside",
            texttemplate="%{text:.2s}",
        ),
        secondary_y=False,
    )
    
    fig.update_traces(marker_color="rgb(33, 60, 99)")

    fig.update_layout(
        height=315,
        margin=dict(l=20, r=30, t=50, b=30),
        plot_bgcolor="rgb(0,0,0,0)",
        legend_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgb(0,0,0,0)",
        font_color="#909090",
        hovermode="closest",
        xaxis={
        "range": [data2["wk"].iloc[5], data2["wk"].max()],
        "rangeslider": {"visible": True},
        },
        yaxis_title="Bottles Sales in $",
        legend=dict(yanchor="top", y=1.4, xanchor="left", x=0),
        title={
            "text": "Annual Revenue",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )
    
    fig.update_xaxes(
        tickangle = 0,
        title_text = "Weeks",
        title_standoff = 2)

    fig.update_yaxes(
            title_text = "Bottles Sold",
            title_standoff = 25)

    return html.Div(dcc.Graph(figure=fig), id="annual_financial")


# ================================= Last Line 
# ----------------------------------- Graph II ---------------------------------------
@callback(
    Output(component_id="anual_products", component_property="children"),
    Input(component_id="year", component_property="value"),
)
def update_graph(year):

    data2 = (
        df.groupby(
            [
                "yyyy",
                "mm",
                "item_description",
            ]
        )["bottles_sold", "sale_dollars"]
        .sum()
        .reset_index()
    )
    data2 = data2[(data2["yyyy"] == year)]
    data2 = data2.sort_values(by=["bottles_sold","mm"], ascending=True).iloc[-220:]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=data2["mm"],
            y=data2["bottles_sold"],
            name="Total Bottles Sold",
            text=data2["item_description"],
            textposition="outside",
            texttemplate="%{text:.0s}",
        ),
        secondary_y=False,
    )

    fig.update_traces(
        marker_color=data2["bottles_sold"],
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
        yaxis_title="Bottles Sold",
        legend=dict(yanchor="top", y=1.4, xanchor="left", x=0),
        title={
            "text": "Annual Bottles Sold",
            "y": 0.98,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    return html.Div(dcc.Graph(figure=fig), id="anual_products")


