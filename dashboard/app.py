import json
from pathlib import Path

import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

def aeris_markdown(*args, **kwargs):
    kwargs["unsafe_allow_html"] = True
    if args and isinstance(args[0], str):
        args = (args[0].replace("\n\n", "\n"),) + args[1:]
    return st.markdown(*args, **kwargs)


from src.index_engine import (
    load_observations,
    calculate_daily_index,
)


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="AERIS — Airfare Intelligence",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# DESIGN SYSTEM
# =========================================================

aeris_markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap'
    );

    :root {
        --cream: #F5F4EF;
        --paper: #FBFAF6;
        --green: #17382D;
        --green-soft: #DCE6DF;
        --rust: #A74628;
        --rust-soft: #F0DCD3;
        --ink: #292925;
        --muted: #706F68;
        --line: #D9D7CE;
    }

    /* Page */

    .stApp {
        background: var(--cream);
        color: var(--ink);
    }

    .main .block-container {
        max-width: 1380px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit chrome */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Default text */

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }

    /* Brand */

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-mark {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: var(--green);
        color: var(--cream);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
    }

    .brand-name {
        font-family: "DM Sans", sans-serif;
        font-size: 25px;
        font-weight: 700;
        letter-spacing: 0.16em;
        color: var(--green);
    }

    .brand-subtitle {
        font-size: 9px;
        letter-spacing: 0.16em;
        color: var(--muted);
        margin-top: -2px;
    }

    /* Navigation */

    .nav {
        display: flex;
        justify-content: flex-end;
        gap: 32px;
        align-items: center;
        height: 48px;
        font-size: 12px;
        color: var(--muted);
        letter-spacing: 0.03em;
    }

    .nav-active {
        color: var(--green);
        font-weight: 700;
        border-bottom: 1px solid var(--green);
        padding-bottom: 5px;
    }

    /* Divider */

    .hairline {
        height: 1px;
        background: var(--line);
        margin: 18px 0 54px 0;
    }

    /* Section labels */

    .eyebrow {
        font-family: "DM Sans", sans-serif;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--rust);
        margin-bottom: 10px;
    }

    .section-title {
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 51px;
        line-height: 0.98;
        font-weight: 500;
        color: var(--green);
        margin: 0;
    }

    .section-copy {
        color: var(--muted);
        font-size: 14px;
        line-height: 1.65;
        max-width: 560px;
        margin-top: 15px;
    }

    /* Hero */

    .hero {
        padding-bottom: 40px;
    }

    .hero-kicker {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: var(--rust);
        font-weight: 700;
        margin-bottom: 14px;
    }

    .aeris-table {
        width: 100%;
        border-collapse: collapse;
        font-family: "DM Sans", sans-serif;
        font-size: 13px;
        background: #FBFAF6;
        border: 1px solid #D9D7CE;
        border-radius: 14px;
        overflow: hidden;
    }

    .aeris-table th {
        background: #17382D;
        color: #FBFAF6;
        padding: 14px 16px;
        text-align: left;
        font-size: 10px;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        font-weight: 700;
    }

    .aeris-table td {
        padding: 14px 16px;
        color: #292925;
        border-bottom: 1px solid #E5E3DC;
        white-space: nowrap;
    }

    .aeris-table tr:last-child td {
        border-bottom: none;
    }

    .aeris-table tr:hover td {
        background: #F0EDE5;
    }

    .aeris-table td:last-child {
        color: #A74628;
        font-weight: 700;
    }

    .hero-title {
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 76px;
        line-height: 0.88;
        font-weight: 500;
        color: var(--green);
        margin: 0;
    }

    .hero-description {
        max-width: 640px;
        margin-top: 22px;
        color: var(--muted);
        font-size: 15px;
        line-height: 1.7;
    }

    /* KPI */

    .kpi-label {
        font-size: 10px;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--muted);
        font-weight: 700;
    }

    .kpi-value {
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 60px;
        line-height: 0.9;
        color: var(--green);
        margin-top: 8px;
    }

    .kpi-change {
        margin-top: 10px;
        font-size: 12px;
        font-weight: 700;
        color: var(--rust);
    }

    /* Cards */

    .card {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 25px;
    }

    .card-title {
        font-family: "Cormorant Garamond", Georgia, serif;
        color: var(--green);
        font-size: 30px;
        font-weight: 600;
        line-height: 1;
    }

    .card-label {
        color: var(--muted);
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 700;
    }

    /* Route cards */

    .route-card {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 15px;
        padding: 22px;
        min-height: 175px;
    }

    .route {
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 31px;
        color: var(--green);
        font-weight: 600;
    }

    .route-index {
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 42px;
        color: var(--green);
        line-height: 1;
        margin-top: 22px;
    }

    .route-meta {
        color: var(--muted);
        font-size: 11px;
        margin-top: 7px;
    }

    /* Status */

    .status-high {
        display: inline-block;
        background: var(--rust-soft);
        color: var(--rust);
        padding: 5px 9px;
        border-radius: 999px;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 0.1em;
    }

    .status-medium {
        display: inline-block;
        background: #E9E5D3;
        color: #776526;
        padding: 5px 9px;
        border-radius: 999px;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 0.1em;
    }

    /* Methodology */

    .method-number {
        font-family: "Cormorant Garamond", Georgia, serif;
        color: var(--rust);
        font-size: 28px;
    }

    .method-title {
        font-family: "Cormorant Garamond", Georgia, serif;
        color: var(--green);
        font-size: 25px;
        font-weight: 600;
    }

    .method-copy {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.6;
    }

    /* Streamlit chart */

    [data-testid="stMetric"] {
        background: transparent;
        border: none;
    }

    [data-testid="stMetricLabel"] {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }

    [data-testid="stMetricValue"] {
        color: var(--green);
        font-family: "Cormorant Garamond", Georgia, serif;
    }

    /* Buttons */

    .stButton > button {
        border: 1px solid var(--line);
        border-radius: 999px;
        background: var(--paper);
        color: var(--green);
        font-family: "DM Sans", sans-serif;
        font-size: 11px;
    }

    .stButton > button:hover {
        border-color: var(--green);
        color: var(--green);
    }

    /* Dataframe */

    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
    }

    /* Footer */

    .footer {
        border-top: 1px solid var(--line);
        margin-top: 70px;
        padding-top: 20px;
        color: var(--muted);
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA
# =========================================================

OBSERVATION_FILE = Path(
    "data/raw/backtest_airfares.json"
)

SPIKE_FILE = Path(
    "data/processed/spike_explanations.json"
)


observations = load_observations(
    str(OBSERVATION_FILE)
)

daily_index = calculate_daily_index(
    observations
)

daily_df = pd.DataFrame(daily_index)

daily_df["date"] = pd.to_datetime(
    daily_df["date"]
)

daily_df = daily_df.sort_values("date")


# Route-level calculations

route_groups = {}

for obs in observations:

    route = (
        obs["origin"],
        obs["destination"]
    )

    route_groups.setdefault(route, []).append(obs)


route_results = []

for (origin, destination), items in route_groups.items():

    items = sorted(
        items,
        key=lambda x: x["collected_at"]
    )

    base_price = items[0]["total_fare"]

    relatives = [
        item["total_fare"] / base_price
        for item in items
        if item["total_fare"] > 0
    ]

    index = (
        sum(relatives) / len(relatives)
    ) * 100

    route_results.append({
        "origin": origin,
        "destination": destination,
        "index": round(index, 2),
        "base_price": round(base_price, 2),
        "observations": len(items),
    })


route_results = sorted(
    route_results,
    key=lambda x: x["index"],
    reverse=True,
)


# Spike data

if SPIKE_FILE.exists():

    with open(SPIKE_FILE, "r") as f:
        spikes = json.load(f)

else:

    spikes = []


# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns(
    [1.25, 2]
)

with header_left:

    aeris_markdown(
        """
        <div class="brand">
            <div class="brand-mark">✈</div>
            <div>
                <div class="brand-name">AERIS</div>
                <div class="brand-subtitle">
                    AIRFARE ECONOMICS & REGIONAL INTELLIGENCE
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)


with header_right:

    aeris_markdown(
        """
        <div class="nav">
            <span class="nav-active">Narrative</span>
            <span>Visualizer</span>
            <span>Taxonomy Engine</span>
            <span>CPI Impact</span>
        </div>
        """,
        unsafe_allow_html=True,
)


aeris_markdown(
    '<div class="hairline"></div>',
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

latest_index = float(
    daily_df.iloc[-1]["index"]
)

first_index = float(
    daily_df.iloc[0]["index"]
)

peak_index = float(
    daily_df["index"].max()
)

change_pct = (
    (latest_index - first_index)
    / first_index
) * 100

peak_date = daily_df.loc[
    daily_df["index"].idxmax(),
    "date"
].strftime("%d %b %Y")


hero_left, hero_right = st.columns(
    [1.7, 1]
)

with hero_left:

    aeris_markdown(
        """
        <div class="hero">
            <div class="hero-kicker">
                National Airfare Intelligence
            </div>

            <div class="hero-title">
                Reading the<br>
                movement of airfares.
            </div>

            <div class="hero-description">
                AERIS transforms repeated airfare observations
                across Indian routes and booking horizons into
                a standardized price signal for inflation
                monitoring, regional analysis and policy insight.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)


with hero_right:

    aeris_markdown(
        '<div class="kpi-label">Current Airfare Index</div>',
        unsafe_allow_html=True,
)

    aeris_markdown(
        f'<div class="kpi-value">{latest_index:.2f}</div>',
        unsafe_allow_html=True,
)

    aeris_markdown(
        f'<div class="kpi-change">'
        f'{change_pct:+.2f}% since base period'
        f'</div>',
        unsafe_allow_html=True,
)

    aeris_markdown(
        f"""
        <div style="
            margin-top:28px;
            color:#706F68;
            font-size:11px;
            line-height:1.7;
        ">
            30-day observation window<br>
            7 representative corridors<br>
            5 booking horizons
        </div>
        """,
        unsafe_allow_html=True,
)


# =========================================================
# NATIONAL INDEX
# =========================================================

aeris_markdown(
    """
    <div class="eyebrow">01 — National movement</div>
    <div class="section-title">
        The national story
    </div>
    <div class="section-copy">
        The index begins at 100 and tracks standardized
        movement in observed airfare prices across the
        prototype route basket.
    </div>
    """,
    unsafe_allow_html=True,
)


aeris_markdown("<br>", unsafe_allow_html=True)


chart_left, chart_right = st.columns(
    [2.2, 1]
)

with chart_left:

    import altair as alt

    chart_df = daily_df.copy()

    chart = alt.Chart(chart_df).mark_line(
        color="#17382D",
        strokeWidth=3
    ).encode(
        x=alt.X(
            "date:T",
            title=None,
            axis=alt.Axis(
                labelColor="#292925",
                labelFont="DM Sans",
                labelFontSize=12,
                tickColor="#D9D7CE",
                domainColor="#D9D7CE",
                grid=False,
            ),
        ),
        y=alt.Y(
            "index:Q",
            title=None,
            scale=alt.Scale(zero=False),
            axis=alt.Axis(
                labelColor="#292925",
                labelFont="DM Sans",
                labelFontSize=12,
                tickColor="#D9D7CE",
                domainColor="#D9D7CE",
                grid=True,
                gridColor="#D9D7CE",
                gridOpacity=0.55,
            ),
        ),
        tooltip=[
            alt.Tooltip("date:T", title="Date", format="%d %b %Y"),
            alt.Tooltip("index:Q", title="Airfare index", format=".2f"),
        ],
    ).properties(
        height=350,
        background="transparent",
    ).configure_view(
        strokeWidth=0,
    )

    st.altair_chart(chart, width="stretch")


with chart_right:

    aeris_markdown(
        """
        <div class="card">
            <div class="card-label">Peak reading</div>
            <div class="card-title"
                 style="margin-top:10px;">
                National pressure
            </div>
        """,
        unsafe_allow_html=True,
)

    aeris_markdown(
        f"""
        <div style="
            font-family:'Cormorant Garamond';
            font-size:52px;
            color:#17382D;
            margin-top:20px;
        ">
            {peak_index:.2f}
        </div>

        <div style="
            color:#706F68;
            font-size:11px;
            line-height:1.6;
        ">
            Peak observed on {peak_date}.
            The movement represents a synthetic
            backtest surge used to validate the
            AERIS measurement pipeline.
        </div>
        """,
        unsafe_allow_html=True,
)

    aeris_markdown(
        "</div>",
        unsafe_allow_html=True,
)


# =========================================================
# ROUTE VISUALIZER
# =========================================================

aeris_markdown("<br><br>", unsafe_allow_html=True)

aeris_markdown(
    """
    <div class="eyebrow">02 — Regional intelligence</div>
    <div class="section-title">
        Where the pressure is moving
    </div>
    <div class="section-copy">
        Route-level indices reveal how heterogeneous airfare
        movements can be hidden inside a national aggregate.
    </div>
    """,
    unsafe_allow_html=True,
)

aeris_markdown("<br>", unsafe_allow_html=True)


route_columns = st.columns(3)

for i, route in enumerate(route_results):

    with route_columns[i % 3]:

        aeris_markdown(
            f"""
            <div class="route-card">
                <div class="card-label">
                    AIR ROUTE
                </div>

                <div class="route">
                    {route['origin']}
                    <span style="font-family:DM Sans;
                    font-size:18px;">→</span>
                    {route['destination']}
                </div>

                <div class="route-index">
                    {route['index']}
                </div>

                <div class="route-meta">
                    Index · {route['observations']}
                    observations
                </div>
            </div>
            """,
            unsafe_allow_html=True,
)

        aeris_markdown("<br>", unsafe_allow_html=True)


# =========================================================
# SURGE DETECTION
# =========================================================

aeris_markdown("<br>", unsafe_allow_html=True)

aeris_markdown(
    """
    <div class="eyebrow">03 — Anomaly intelligence</div>
    <div class="section-title">
        When the signal changes
    </div>
    <div class="section-copy">
        AERIS identifies unusually large movements and
        decomposes them into the route and booking-window
        strata contributing to the change.
    </div>
    """,
    unsafe_allow_html=True,
)

aeris_markdown("<br>", unsafe_allow_html=True)


if spikes:

    for spike in spikes:

        severity = spike.get(
            "severity",
            "UNKNOWN"
        )

        if severity == "HIGH":

            status_html = (
                '<span class="status-high">HIGH</span>'
            )

        else:

            status_html = (
                '<span class="status-medium">'
                f'{severity}'
                '</span>'
            )

        aeris_markdown(
            f"""
            <div class="card"
                 style="margin-bottom:15px;">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div>
                        <div class="card-label">
                            {spike['date']}
                        </div>

                        <div class="card-title"
                             style="margin-top:8px;">
                            Airfare movement detected
                        </div>
                    </div>

                    <div>
                        {status_html}
                    </div>

                </div>

                <div style="
                    margin-top:20px;
                    font-family:'Cormorant Garamond';
                    font-size:34px;
                    color:#17382D;
                ">
                    {spike['previous_index']:.2f}
                    →
                    {spike['index']:.2f}

                    <span style="
                        font-family:'DM Sans';
                        font-size:13px;
                        color:#A74628;
                    ">
                        +{spike['index_change_pct']:.2f}%
                    </span>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
)

        routes = spike.get(
            "top_affected_routes",
            []
        )

        if routes:

            route_df = pd.DataFrame(routes)

            route_df = route_df.rename(
                columns={
                    "origin": "Origin",
                    "destination": "Destination",
                    "booking_window": "Booking window",
                    "previous_fare": "Previous fare",
                    "current_fare": "Current fare",
                    "change_pct": "Movement %",
                }
            )

            route_df["Previous fare"] = route_df["Previous fare"].map(
                lambda x: f"₹{x:,.0f}"
            )

            route_df["Current fare"] = route_df["Current fare"].map(
                lambda x: f"₹{x:,.0f}"
            )

            route_df["Movement %"] = route_df["Movement %"].map(
                lambda x: f"{x:+.2f}%"
            )

            aeris_markdown(
                route_df.to_html(
                    index=False,
                    classes="aeris-table",
                    border=0,
                ),
                unsafe_allow_html=True,
            )


# =========================================================
# BOOKING HORIZON
# =========================================================

aeris_markdown("<br><br>", unsafe_allow_html=True)

aeris_markdown(
    """
    <div class="eyebrow">04 — Booking horizon</div>
    <div class="section-title">
        The time before takeoff matters
    </div>
    <div class="section-copy">
        AERIS observes fares at standardized lead-time
        windows so that movements can be compared across
        equivalent booking horizons.
    </div>
    """,
    unsafe_allow_html=True,
)

aeris_markdown("<br>", unsafe_allow_html=True)


windows = [
    ("T+1", "Tomorrow"),
    ("T+7", "7 days"),
    ("T+15", "15 days"),
    ("T+30", "30 days"),
    ("T+45", "45 days"),
]


window_cols = st.columns(5)

for col, (window, meaning) in zip(
    window_cols,
    windows
):

    with col:

        aeris_markdown(
            f"""
            <div class="card"
                 style="text-align:center;
                 min-height:125px;">

                <div class="card-label">
                    BOOKING WINDOW
                </div>

                <div style="
                    font-family:'Cormorant Garamond';
                    font-size:39px;
                    color:#17382D;
                    margin-top:13px;
                ">
                    {window}
                </div>

                <div style="
                    font-size:10px;
                    color:#706F68;
                ">
                    {meaning}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
)


# =========================================================
# METHODOLOGY
# =========================================================

aeris_markdown("<br><br>", unsafe_allow_html=True)

aeris_markdown(
    """
    <div class="eyebrow">05 — Measurement framework</div>
    <div class="section-title">
        Built as a price index, not a price tracker.
    </div>
    <div class="section-copy">
        The prototype separates measurement from prediction:
        repeated observations are standardized first, then
        aggregated into an interpretable macro-level signal.
    </div>
    """,
    unsafe_allow_html=True,
)

aeris_markdown("<br>", unsafe_allow_html=True)


method_cols = st.columns(3)

methods = [
    (
        "01",
        "Observe",
        "Collect repeated airfare observations across "
        "routes, carriers and booking horizons."
    ),
    (
        "02",
        "Standardize",
        "Validate fare components, availability, "
        "booking windows and route metadata."
    ),
    (
        "03",
        "Measure",
        "Convert comparable price relatives into a "
        "transparent aggregate airfare index."
    ),
]


for col, (number, title, copy) in zip(
    method_cols,
    methods
):

    with col:

        aeris_markdown(
            f"""
            <div class="card">

                <div class="method-number">
                    {number}
                </div>

                <div class="method-title">
                    {title}
                </div>

                <div class="method-copy"
                     style="margin-top:9px;">
                    {copy}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
)


# =========================================================
# FOOTER
# =========================================================

aeris_markdown(
    """
    <div class="footer">
        AERIS · Airfare Economics & Regional Intelligence
        · Prototype · Synthetic 30-day backtest
    </div>
    """,
    unsafe_allow_html=True,
)
