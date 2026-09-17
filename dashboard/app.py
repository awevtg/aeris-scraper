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
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');
    :root { --cream:#F5F4EF; --paper:#FBFAF6; --green:#17382D; --green-soft:#DCE6DF; --rust:#A74628; --rust-soft:#F0DCD3; --ink:#292925; --muted:#706F68; --line:#D9D7CE; --line-dark:#C6C3B9; }
    .stApp{background:var(--cream);color:var(--ink)}
    .main .block-container{max-width:1440px;padding:1.15rem 4.5rem 4.5rem}
    html,body,[class*=css]{font-family:"DM Sans",sans-serif}
    #MainMenu,footer{visibility:hidden}
    header,[data-testid="stHeader"]{background:transparent!important}
    [data-testid="stToolbar"],[data-testid="stDecoration"]{display:none}
    [data-testid="column"]{min-width:0}
    .topbar{min-height:54px;display:flex;align-items:center}
    .brand{display:flex;align-items:center;gap:13px}
    .brand-mark{width:40px;height:40px;flex:0 0 40px;border-radius:50%;background:var(--green);color:var(--cream);display:flex;align-items:center;justify-content:center;font-size:18px}
    .brand-name{color:var(--green);font-size:21px;font-weight:700;letter-spacing:.19em;line-height:1}
    .brand-subtitle{color:var(--muted);font-size:8px;font-weight:600;letter-spacing:.13em;margin-top:5px}
    .nav-wrap{display:flex;justify-content:flex-end;align-items:center;gap:23px;min-height:54px;flex-wrap:nowrap}
    .nav-wrap + *{margin-top:0!important}
    .nav-current,[data-testid="stPageLink"] a{color:var(--muted)!important;font-size:9px!important;font-weight:700!important;letter-spacing:.13em!important;text-transform:uppercase!important;text-decoration:none!important;padding:7px 0!important;border-bottom:1px solid transparent;white-space:nowrap}
    .nav-current{color:var(--green)!important;border-bottom-color:var(--rust)}
    [data-testid="stPageLink"]{display:inline-flex!important;width:auto!important;margin:0!important;padding:0!important}
    [data-testid="stPageLink"] > div{padding:0!important}
    [data-testid="stPageLink"] a{display:inline-block!important}
    [data-testid="stPageLink"] a:hover{color:var(--green)!important;border-bottom-color:var(--rust)}
    .hairline{height:1px;background:var(--line);margin:14px 0 68px}
    .eyebrow{color:var(--rust);font-size:9px;font-weight:700;letter-spacing:.19em;text-transform:uppercase;margin-bottom:11px}
    .section-title{color:var(--green);font-family:"Cormorant Garamond",Georgia,serif;font-size:48px;font-weight:500;line-height:.95;letter-spacing:-.018em;margin:0}
    .section-copy{max-width:610px;color:var(--muted);font-size:12px;line-height:1.7;margin-top:14px}
    .hero{padding-bottom:30px}
    .hero-kicker{color:var(--rust);font-size:9px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;margin-bottom:14px}
    .hero-title{color:var(--green);font-family:"Cormorant Garamond",Georgia,serif;font-size:clamp(56px,5.4vw,82px);font-weight:500;line-height:.84;letter-spacing:-.028em;margin:0;max-width:790px}
    .hero-description{max-width:620px;color:var(--muted);font-size:12px;line-height:1.75;margin-top:24px}
    .hero-side{border-left:1px solid var(--line);padding:8px 0 10px 35px;min-height:218px}
    .kpi-label,.card-label{color:var(--muted);font-size:8px;font-weight:700;letter-spacing:.16em;text-transform:uppercase}
    .kpi-value{color:var(--green);font-family:"Cormorant Garamond",Georgia,serif;font-size:72px;font-weight:500;line-height:.82;letter-spacing:-.025em;margin-top:15px}
    .kpi-change{color:var(--rust);font-size:10px;font-weight:700;margin-top:10px}
    .kpi-rule{width:38px;height:2px;background:var(--rust);margin:20px 0 15px}
    .kpi-meta{color:var(--muted);font-size:9px;line-height:1.75}
    .card,.chart-shell,.route-card{background:var(--paper);border:1px solid var(--line);border-radius:11px}
    .card{padding:23px}.chart-shell{padding:9px 14px 7px}.chart-caption{color:var(--muted);font-size:8px;letter-spacing:.05em;margin:0 3px 2px}
    .card-title{color:var(--green);font-family:"Cormorant Garamond",Georgia,serif;font-size:28px;font-weight:600;line-height:1}
    .route-card{padding:19px;min-height:151px;transition:border-color .16s ease,transform .16s ease}.route-card:hover{border-color:var(--line-dark);transform:translateY(-2px)}
    .route{color:var(--green);font-family:"Cormorant Garamond",Georgia,serif;font-size:29px;font-weight:600;line-height:1;margin-top:8px}.route-index{color:var(--green);font-family:"Cormorant Garamond",Georgia,serif;font-size:40px;line-height:.9;margin-top:20px}.route-meta{color:var(--muted);font-size:8px;letter-spacing:.04em;margin-top:8px}
    .status-high,.status-medium{display:inline-block;border-radius:999px;padding:5px 9px;font-size:8px;font-weight:700;letter-spacing:.12em}.status-high{color:var(--rust);background:var(--rust-soft)}.status-medium{color:#776526;background:#E9E5D3}
    .aeris-table{width:100%;border-collapse:collapse;font-family:"DM Sans",sans-serif;font-size:10px;background:var(--paper);border:1px solid var(--line);border-radius:11px;overflow:hidden}.aeris-table th{background:var(--green);color:var(--paper);padding:12px 14px;text-align:left;font-size:8px;letter-spacing:.12em;text-transform:uppercase;font-weight:700}.aeris-table td{color:var(--ink);padding:12px 14px;border-bottom:1px solid #E5E3DC;white-space:nowrap}.aeris-table tr:last-child td{border-bottom:none}.aeris-table tr:hover td{background:#F0EDE5}.aeris-table td:last-child{color:var(--rust);font-weight:700}
    .horizon-card{background:var(--paper);border:1px solid var(--line);border-radius:11px;padding:17px 10px;min-height:105px;text-align:center}.horizon-value{color:var(--green);font-family:"Cormorant Garamond",Georgia,serif;font-size:36px;line-height:1;margin-top:12px}.horizon-meaning{color:var(--muted);font-size:8px;margin-top:6px}
    .method-card{border-top:1px solid var(--line);padding-top:15px}.method-number{color:var(--rust);font-family:"Cormorant Garamond",Georgia,serif;font-size:25px;line-height:1}.method-title{color:var(--green);font-family:"Cormorant Garamond",Georgia,serif;font-size:24px;font-weight:600;margin-top:5px}.method-copy{color:var(--muted);font-size:10px;line-height:1.65;margin-top:7px}
    .stButton>button{border:1px solid var(--line);border-radius:999px;background:var(--paper);color:var(--green);font-family:"DM Sans",sans-serif;font-size:10px;font-weight:700}.stButton>button:hover{border-color:var(--green);color:var(--green)}
    .footer{border-top:1px solid var(--line);margin-top:70px;padding-top:18px;color:var(--muted);font-size:8px;font-weight:600;letter-spacing:.11em;text-transform:uppercase}
    [data-testid="stPageLink"] a, [data-testid="stPageLink"] a:visited{color:var(--muted)!important;background:transparent!important}
    [data-testid="stPageLink"] a:hover{color:var(--green)!important;background:transparent!important}
    [data-testid="stPageLink"] p{margin:0!important}
    /* Hide Streamlit's built-in navigation sidebar */

    [data-testid="stSidebar"] {
        display: none !important;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    /* FINAL AERIS NAVIGATION */
    .nav-current{
        display:inline-flex!important;
        align-items:center!important;
        min-height:32px!important;
        padding:7px 0!important;
        color:#17382D!important;
        font-family:"DM Sans",sans-serif!important;
        font-size:9px!important;
        font-weight:700!important;
        letter-spacing:.13em!important;
        text-transform:uppercase!important;
        border-bottom:1px solid #A74628!important;
        white-space:nowrap!important;
    }

    [data-testid="stPageLink"]{
        width:100%!important;
        min-width:0!important;
        margin:0!important;
        padding:0!important;
    }

    [data-testid="stPageLink"] > div{
        width:100%!important;
        min-width:0!important;
        margin:0!important;
        padding:0!important;
    }

    [data-testid="stPageLink"] a,
    [data-testid="stPageLink"] a:visited,
    [data-testid="stPageLink"] button{
        display:flex!important;
        align-items:center!important;
        justify-content:flex-start!important;
        width:max-content!important;
        min-width:0!important;
        height:32px!important;
        min-height:32px!important;
        margin:0!important;
        padding:7px 0!important;
        border:0!important;
        border-bottom:1px solid transparent!important;
        border-radius:0!important;
        box-shadow:none!important;
        background:transparent!important;
        background-color:transparent!important;
        color:#706F68!important;
        font-family:"DM Sans",sans-serif!important;
        font-size:9px!important;
        font-weight:700!important;
        letter-spacing:.13em!important;
        line-height:1!important;
        text-transform:uppercase!important;
        white-space:nowrap!important;
    }

    [data-testid="stPageLink"] a:hover,
    [data-testid="stPageLink"] button:hover{
        color:#17382D!important;
        background:transparent!important;
        border-bottom-color:#A74628!important;
    }

    [data-testid="stPageLink"] a p,
    [data-testid="stPageLink"] button p,
    [data-testid="stPageLink"] a span,
    [data-testid="stPageLink"] button span{
        margin:0!important;
        padding:0!important;
        color:inherit!important;
        font-family:inherit!important;
        font-size:inherit!important;
        font-weight:inherit!important;
        letter-spacing:inherit!important;
        text-transform:inherit!important;
    }
    @media(max-width:900px){.main .block-container{padding-left:1.35rem;padding-right:1.35rem}.hero-title{font-size:55px}.section-title{font-size:40px}.hero-side{border-left:none;border-top:1px solid var(--line);padding:24px 0 0;margin-top:10px}.nav-wrap{gap:12px}}
    </style>
    """,
    unsafe_allow_html=True,
)

# Final navigation override: keep Streamlit page links visually quiet.
aeris_markdown(
    """
    <style>
    [data-testid="stPageLink"] {
        width:auto!important; margin:0!important; padding:0!important;
    }
    [data-testid="stPageLink"] > div {
        width:auto!important; padding:0!important;
    }
    [data-testid="stPageLink"] a,
    [data-testid="stPageLink"] a:visited,
    [data-testid="stPageLink"] a:hover,
    [data-testid="stPageLink"] button {
        display:inline-flex!important; align-items:center!important;
        width:auto!important; min-height:0!important; height:auto!important;
        padding:7px 0!important; margin:0!important;
        border:0!important; border-bottom:1px solid transparent!important;
        border-radius:0!important; box-shadow:none!important;
        background:transparent!important; background-color:transparent!important;
        color:#706F68!important; font-family:"DM Sans",sans-serif!important;
        font-size:9px!important; font-weight:700!important;
        letter-spacing:.13em!important; text-transform:uppercase!important;
    }
    [data-testid="stPageLink"] a:hover,
    [data-testid="stPageLink"] button:hover {
        color:#17382D!important; border-bottom-color:#A74628!important;
    }
    [data-testid="stPageLink"] p { margin:0!important; color:inherit!important; }
    
/* AERIS GLOBAL NAVIGATION VISIBILITY FIX */

[data-testid="stPageLink"],
[data-testid="stPageLink"] > div,
[data-testid="stPageLink"] a,
[data-testid="stPageLink"] a *,
[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span,
[data-testid="stPageLink"] button,
[data-testid="stPageLink"] button *,
[data-testid="stPageLink"] button p,
[data-testid="stPageLink"] button span {
    color: #706F68 !important;
    -webkit-text-fill-color: #706F68 !important;
    opacity: 1 !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stPageLink"] a:hover,
[data-testid="stPageLink"] a:hover *,
[data-testid="stPageLink"] button:hover,
[data-testid="stPageLink"] button:hover * {
    color: #17382D !important;
    -webkit-text-fill-color: #17382D !important;
}

.nav-active,
.nav-active * {
    color: #A74628 !important;
    -webkit-text-fill-color: #A74628 !important;
    opacity: 1 !important;
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

    nav_cols = st.columns([1, 1, 1, 1], gap="small")

    with nav_cols[0]:
        aeris_markdown(
            '<div class="nav-current">NARRATIVE</div>',
            unsafe_allow_html=True,
        )

    with nav_cols[1]:
        st.page_link(
            "pages/1_Visualizer.py",
            label="VISUALIZER",
        )

    with nav_cols[2]:
        st.page_link(
            "pages/2_Blooms_Taxonomy.py",
            label="TAXONOMY",
        )

    with nav_cols[3]:
        st.page_link(
            "pages/3_CPI_Impact.py",
            label="CPI IMPACT",
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
        f"""
        <div class="hero-side">
            <div class="kpi-label">Current Airfare Index</div>
            <div class="kpi-value">{latest_index:.2f}</div>
            <div class="kpi-change">{change_pct:+.2f} % since base period</div>
            <div class="kpi-rule"></div>
            <div class="kpi-meta">
                30-day observation window<br>
                7 representative corridors<br>
                5 booking horizons
            </div>
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