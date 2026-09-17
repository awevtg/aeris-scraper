import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

import plotly.graph_objects as go


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

def aeris_markdown(*args, **kwargs):
    kwargs["unsafe_allow_html"] = True
    if args and isinstance(args[0], str):
        args = (args[0].replace("\n\n", "\n"),) + args[1:]
    return st.markdown(*args, **kwargs)

st.set_page_config(
    page_title="AERIS — CPI Impact",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
    <style>

    .stApp {
        background: #F5F4EF !important;
        color: #292925 !important;
    }

    .block-container {
        max-width: 1450px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 5rem !important;
    }

    [data-testid="stSidebar"] {
        display: none !important;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    #MainMenu {
        visibility: hidden !important;
    }

    footer {
        visibility: hidden !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

DATA_PATH = ROOT / "data" / "raw" / "backtest_airfares.json"

with open(DATA_PATH, "r") as f:
    observations = json.load(f)


df = pd.DataFrame(observations)

df["collected_at"] = pd.to_datetime(df["collected_at"])
df["date"] = df["collected_at"].dt.date

df["route"] = (
    df["origin"].astype(str)
    + " → "
    + df["destination"].astype(str)
)

# Remove invalid fares
df = df[df["total_fare"] > 0].copy()


# ---------------------------------------------------------
# DAILY AIRFARE INDEX
# ---------------------------------------------------------

daily = (
    df.groupby("date")["total_fare"]
    .mean()
    .reset_index()
)

daily["date"] = pd.to_datetime(daily["date"])

base_fare = daily.iloc[0]["total_fare"]

daily["index"] = (
    daily["total_fare"] / base_fare
) * 100


current_index = float(daily.iloc[-1]["index"])
base_index = float(daily.iloc[0]["index"])

change_pct = (
    (current_index / base_index) - 1
) * 100


# ---------------------------------------------------------
# ROUTE IMPACT
# ---------------------------------------------------------

route_summary = (
    df.groupby("route")["total_fare"]
    .agg(["first", "last", "mean"])
    .reset_index()
)

route_summary["movement"] = (
    route_summary["last"] /
    route_summary["first"] - 1
) * 100

route_summary = route_summary.sort_values(
    "movement",
    ascending=False
)


# ---------------------------------------------------------
# BOOKING WINDOW IMPACT
# ---------------------------------------------------------

window_summary = (
    df.groupby("booking_window")["total_fare"]
    .mean()
    .reset_index()
)

window_summary["index"] = (
    window_summary["total_fare"] /
    window_summary["total_fare"].iloc[0]
) * 100


# ---------------------------------------------------------
# AERIS STYLE
# ---------------------------------------------------------

aeris_markdown(
    """
    
<style>
/* AERIS navigation — override Streamlit default page buttons */
[data-testid="stPageLink"] {
    width: auto !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stPageLink"] > div {
    width: auto !important;
}
.aeris-nav [data-testid="stPageLink"],
.aeris-nav [data-testid="stPageLink"] a,
.aeris-nav [data-testid="stPageLink"] a:visited,
.aeris-nav [data-testid="stPageLink"] a:hover,
.aeris-nav [data-testid="stPageLink"] button,
.aeris-nav [data-testid="stPageLink"] button p,
.aeris-nav [data-testid="stPageLink"] a p,
.aeris-nav [data-testid="stPageLink"] span {
    background: transparent !important;
    background-color: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: #706F68 !important;
    font-family: "DM Sans", sans-serif !important;
    font-size: 9px !important;
    font-weight: 700 !important;
    letter-spacing: .14em !important;
    padding: 7px 0 !important;
    min-height: 0 !important;
    height: auto !important;
    text-decoration: none !important;
}

.aeris-nav [data-testid="stPageLink"] a:hover,
.aeris-nav [data-testid="stPageLink"] button:hover,
.aeris-nav [data-testid="stPageLink"] a:hover p {
    color: #17382D !important;
}

[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] button p {
    color: inherit !important;
    font-size: inherit !important;
    font-weight: inherit !important;
    letter-spacing: inherit !important;
}

</style>

<style>

    .stApp {
        background: #F5F4EF;
        color: #292925;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .section-label {
        font-family: Arial, sans-serif;
        font-size: 11px;
        letter-spacing: 2px;
        color: #A74628;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 15px;
    }

    .hero-title {
        font-family: Georgia, serif;
        font-size: 58px;
        line-height: 1.05;
        color: #17382D;
        font-weight: 500;
        margin-bottom: 20px;
    }

    .hero-title em {
        color: #A74628;
    }

    .hero-copy {
        font-family: Arial, sans-serif;
        font-size: 16px;
        line-height: 1.7;
        color: #62615B;
        max-width: 800px;
        margin-bottom: 45px;
    }

    .metric-card {
        background: #FBFAF6;
        border: 1px solid #D9D7CE;
        border-radius: 16px;
        padding: 24px;
        min-height: 135px;
    }

    .metric-label {
        font-family: Arial, sans-serif;
        font-size: 10px;
        letter-spacing: 1.4px;
        color: #77766F;
        font-weight: 700;
        text-transform: uppercase;
    }

    .metric-value {
        font-family: Georgia, serif;
        font-size: 34px;
        color: #17382D;
        margin-top: 10px;
    }

    .metric-change {
        font-family: Arial, sans-serif;
        font-size: 12px;
        color: #A74628;
        font-weight: 700;
        margin-top: 5px;
    }

    .info-box {
        background: #EDE9DF;
        border-left: 4px solid #A74628;
        border-radius: 10px;
        padding: 20px 22px;
        margin: 25px 0 35px 0;
    }

    .info-title {
        font-family: Georgia, serif;
        font-size: 21px;
        color: #17382D;
        margin-bottom: 7px;
    }

    .info-text {
        font-family: Arial, sans-serif;
        font-size: 13px;
        line-height: 1.65;
        color: #62615B;
    }

    .chart-title {
        font-family: Georgia, serif;
        font-size: 29px;
        color: #17382D;
        margin-top: 35px;
        margin-bottom: 7px;
    }

    .chart-description {
        font-family: Arial, sans-serif;
        font-size: 13px;
        line-height: 1.6;
        color: #62615B;
        margin-bottom: 15px;
    }

    .benchmark-card {
        background: #17382D;
        color: #F5F4EF;
        border-radius: 18px;
        padding: 30px;
        margin-top: 40px;
    }

    .benchmark-title {
        font-family: Georgia, serif;
        font-size: 27px;
        margin-bottom: 10px;
    }

    .benchmark-text {
        font-family: Arial, sans-serif;
        font-size: 13px;
        line-height: 1.7;
        color: #E5E3DC;
    }
    /* FINAL AERIS NAV TEXT FIX */

    .aeris-nav,
    .aeris-nav *,
    .aeris-nav p,
    .aeris-nav span,
    .aeris-nav div,
    .aeris-nav a,
    .aeris-nav button {
        color: #706F68 !important;
    }

    .aeris-nav a:hover,
    .aeris-nav button:hover {
        color: #17382D !important;
    }

    .aeris-nav .nav-active,
    .aeris-nav .nav-active * {
        color: #A74628 !important;
    }

    
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

    
/* =========================================================
   AERIS NAVIGATION SYSTEM — CONSISTENT ACROSS ALL PAGES
   ========================================================= */

.aeris-nav {
    border-bottom: 1px solid #D9D7CE !important;
    padding: 4px 0 16px 0 !important;
    margin-bottom: 28px !important;
}

.aeris-nav .brand-name,
.aeris-nav .brand-name *,
.aeris-nav .brand-subtitle,
.aeris-nav .brand-subtitle *,
.aeris-nav .brand-sub {
    font-family: "DM Sans", sans-serif !important;
}

.aeris-nav .brand-name {
    color: #17382D !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
}

.aeris-nav .brand-subtitle,
.aeris-nav .brand-sub {
    color: #8A887F !important;
    font-size: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 1.2px !important;
}

.aeris-nav .brand-mark {
    width: 38px !important;
    height: 38px !important;
    border-radius: 50% !important;
    background: #17382D !important;
    color: #F5F4EF !important;
}

.aeris-nav [data-testid="stPageLink"],
.aeris-nav [data-testid="stPageLink"] a,
.aeris-nav [data-testid="stPageLink"] a *,
.aeris-nav [data-testid="stPageLink"] a p,
.aeris-nav [data-testid="stPageLink"] a span,
.aeris-nav [data-testid="stPageLink"] button,
.aeris-nav [data-testid="stPageLink"] button *,
.aeris-nav [data-testid="stPageLink"] button p,
.aeris-nav [data-testid="stPageLink"] button span {
    font-family: "DM Sans", sans-serif !important;
    font-size: 9px !important;
    font-weight: 700 !important;
    letter-spacing: .13em !important;
    line-height: 1 !important;
    text-transform: uppercase !important;
    color: #706F68 !important;
    -webkit-text-fill-color: #706F68 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    opacity: 1 !important;
}

.aeris-nav [data-testid="stPageLink"] a:hover,
.aeris-nav [data-testid="stPageLink"] a:hover *,
.aeris-nav [data-testid="stPageLink"] button:hover,
.aeris-nav [data-testid="stPageLink"] button:hover * {
    color: #17382D !important;
    -webkit-text-fill-color: #17382D !important;
}

.aeris-nav .nav-active,
.aeris-nav .nav-active *,
.aeris-nav .nav-current,
.aeris-nav .nav-current * {
    color: #A74628 !important;
    -webkit-text-fill-color: #A74628 !important;
    font-family: "DM Sans", sans-serif !important;
    font-size: 9px !important;
    font-weight: 700 !important;
    letter-spacing: .13em !important;
    text-transform: uppercase !important;
}

</style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER / NAVIGATION
# ---------------------------------------------------------

st.markdown('<div class="aeris-nav">', unsafe_allow_html=True)

left, right = st.columns([2.2, 5.8])

with left:
    st.markdown(
        """
        <div class="aeris-brand">
            <div class="brand-mark">✈</div>
            <div>
                <div class="brand-name">AERIS</div>
                <div class="brand-subtitle">AIRFARE INTELLIGENCE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    n1, n2, n3, n4 = st.columns(4)

    with n1:
        st.page_link("app.py", label="NARRATIVE")

    with n2:
        st.page_link(
            "pages/1_Visualizer.py",
            label="VISUALIZER",
        )

    with n3:
        st.page_link(
            "pages/2_Blooms_Taxonomy.py",
            label="TAXONOMY",
        )

    with n4:
        st.markdown(
            '<div class="nav-active">CPI IMPACT</div>',
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

aeris_markdown(
    """
    <div class="section-label">
        SECTION 04 · CPI IMPACT
    </div>

    <div class="hero-title">
        When airfares move,<br>
        <em>what does it mean?</em>
    </div>

    <div class="hero-copy">
        AERIS translates airfare movements into an economic signal
        that can be interpreted alongside India's Consumer Price Index.
        The objective is not to replace the official CPI series, but
        to make airfare pressure more visible, measurable and explainable.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# IMPORTANT METHODOLOGY NOTE
# ---------------------------------------------------------

aeris_markdown(
    """
    <div class="info-box">

        <div class="info-title">
            CPI relevance, not an official CPI replacement
        </div>

        <div class="info-text">
            The AERIS index is an airfare-specific price signal.
            India's official CPI is produced using an established
            consumption basket and official weights. AERIS therefore
            treats CPI impact as an analytical relevance layer until
            official category weights and benchmark data are incorporated.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)
# ---------------------------------------------------------
# CPI INTERPRETATION
# ---------------------------------------------------------

st.html(
    """
    <div class="benchmark-card">
        <div class="benchmark-title">
            How to read the CPI connection
        </div>

        <div class="benchmark-text">
            A rise in the AERIS airfare index indicates that observed
            airfare levels have increased relative to the index base.
            This does not directly represent a percentage-point change
            in India's headline CPI.
        </div>

        <div style="
            display:grid;
            grid-template-columns:repeat(3, 1fr);
            gap:18px;
            margin-top:24px;
        ">
            <div style="
                border:1px solid rgba(245,244,239,.22);
                border-radius:12px;
                padding:18px;
            ">
                <div style="
                    font-family:Arial,sans-serif;
                    font-size:10px;
                    letter-spacing:1.4px;
                    color:#D8A18F;
                    font-weight:700;
                    text-transform:uppercase;
                    margin-bottom:8px;
                ">01 · SIGNAL</div>

                <div style="
                    font-family:Georgia,serif;
                    font-size:19px;
                    color:#F5F4EF;
                ">Airfare movement</div>

                <div style="
                    font-family:Arial,sans-serif;
                    font-size:12px;
                    line-height:1.6;
                    color:#D9D7CE;
                    margin-top:7px;
                ">
                    Measures how observed airfare levels move relative
                    to the AERIS base period.
                </div>
            </div>

            <div style="
                border:1px solid rgba(245,244,239,.22);
                border-radius:12px;
                padding:18px;
            ">
                <div style="
                    font-family:Arial,sans-serif;
                    font-size:10px;
                    letter-spacing:1.4px;
                    color:#D8A18F;
                    font-weight:700;
                    text-transform:uppercase;
                    margin-bottom:8px;
                ">02 · CONTEXT</div>

                <div style="
                    font-family:Georgia,serif;
                    font-size:19px;
                    color:#F5F4EF;
                ">CPI relevance</div>

                <div style="
                    font-family:Arial,sans-serif;
                    font-size:12px;
                    line-height:1.6;
                    color:#D9D7CE;
                    margin-top:7px;
                ">
                    Provides an airfare-specific signal that can be
                    interpreted alongside official CPI information.
                </div>
            </div>

            <div style="
                border:1px solid rgba(245,244,239,.22);
                border-radius:12px;
                padding:18px;
            ">
                <div style="
                    font-family:Arial,sans-serif;
                    font-size:10px;
                    letter-spacing:1.4px;
                    color:#D8A18F;
                    font-weight:700;
                    text-transform:uppercase;
                    margin-bottom:8px;
                ">03 · FUTURE</div>

                <div style="
                    font-family:Georgia,serif;
                    font-size:19px;
                    color:#F5F4EF;
                ">Official weighting</div>

                <div style="
                    font-family:Arial,sans-serif;
                    font-size:12px;
                    line-height:1.6;
                    color:#D9D7CE;
                    margin-top:7px;
                ">
                    Future versions can incorporate official category
                    weights and benchmark data for stronger comparison.
                </div>
            </div>
        </div>
    </div>
    """
)

aeris_markdown(
    """
    <div style="
        border-top:1px solid #D9D7CE;
        margin-top:55px;
        padding-top:20px;
        text-align:center;
        font-family:Arial,sans-serif;
        font-size:10px;
        letter-spacing:1.2px;
        color:#77766F;
    ">
        AERIS · Airfare Economics & Regional Intelligence ·
        Prototype · Synthetic 30-day backtest
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# KEY METRICS
# ---------------------------------------------------------

aeris_markdown(
    '<div class="section-label">CURRENT SIGNAL</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    aeris_markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">AERIS AIRFARE INDEX</div>
            <div class="metric-value">{current_index:.2f}</div>
            <div class="metric-change">Base = 100</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    aeris_markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">30-DAY MOVEMENT</div>
            <div class="metric-value">+{change_pct:.2f}%</div>
            <div class="metric-change">Airfare pressure</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    aeris_markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">ROUTES OBSERVED</div>
            <div class="metric-value">{df["route"].nunique()}</div>
            <div class="metric-change">Representative basket</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    aeris_markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">BOOKING WINDOWS</div>
            <div class="metric-value">{df["booking_window"].nunique()}</div>
            <div class="metric-change">T+1 → T+45</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# AIRFARE PRESSURE
# ---------------------------------------------------------

aeris_markdown(
    """
    <div class="chart-title">
        Airfare pressure over time
    </div>

    <div class="chart-description">
        This series shows the movement of the AERIS airfare signal
        relative to its starting observation. A value of 100 represents
        the base period; values above 100 indicate higher observed
        airfare levels relative to that base.
    </div>
    """,
    unsafe_allow_html=True,
)

import altair as alt

pressure_chart = (
    alt.Chart(daily)
    .mark_line(
        color="#A74628",
        strokeWidth=3,
    )
    .encode(
        x=alt.X(
            "date:T",
            title=None,
            axis=alt.Axis(
                labelColor="#292925",
                labelFontSize=12,
                grid=False,
            ),
        ),
        y=alt.Y(
            "index:Q",
            title="AERIS airfare index",
            scale=alt.Scale(domain=[98, 123], zero=False),
            axis=alt.Axis(
                labelColor="#292925",
                titleColor="#62615B",
                gridColor="#D9D7CE",
            ),
        ),
        tooltip=[
            alt.Tooltip(
                "date:T",
                title="Date",
                format="%d %b %Y",
            ),
            alt.Tooltip(
                "index:Q",
                title="Index",
                format=".2f",
            ),
        ],
    )
    .properties(
        height=360,
        background="transparent",
    )
    .configure_view(
        strokeWidth=0,
    )
)

st.altair_chart(
    pressure_chart,
    width="stretch",
)


# ---------------------------------------------------------
# ROUTE PRESSURE
# ---------------------------------------------------------

aeris_markdown(
    """
    <div class="chart-title">
        Where is the pressure concentrated?
    </div>

    <div class="chart-description">
        Route-level movement helps identify whether a national airfare
        signal is broad-based or driven by a smaller group of city pairs.
        Larger positive movement indicates stronger fare pressure.
    </div>
    """,
    unsafe_allow_html=True,
)

route_chart = (
    alt.Chart(route_summary)
    .mark_bar(
        color="#17382D",
        cornerRadiusTopRight=5,
        cornerRadiusBottomRight=5,
    )
    .encode(
        x=alt.X(
            "movement:Q",
            title="Movement (%)",
            axis=alt.Axis(
                labelColor="#292925",
                titleColor="#62615B",
                gridColor="#D9D7CE",
            ),
        ),
        y=alt.Y(
            "route:N",
            sort="-x",
            title=None,
            axis=alt.Axis(
                labelColor="#292925",
            ),
        ),
        tooltip=[
            alt.Tooltip("route:N", title="Route"),
            alt.Tooltip(
                "movement:Q",
                title="Movement",
                format="+.2f",
            ),
            alt.Tooltip(
                "mean:Q",
                title="Average fare",
                format=",.0f",
            ),
        ],
    )
    .properties(
        height=330,
        background="transparent",
    )
    .configure_view(
        strokeWidth=0,
    )
)

st.altair_chart(
    route_chart,
    width="stretch",
)


# ---------------------------------------------------------
# BOOKING WINDOW
# ---------------------------------------------------------

aeris_markdown(
    """
    <div class="chart-title">
        Booking horizon and airfare pressure
    </div>

    <div class="chart-description">
        Booking windows show how fare levels differ depending on how
        far the departure date is from the observation. This helps
        separate short-lead airfare pressure from longer-horizon movement.
    </div>
    """,
    unsafe_allow_html=True,
)


window_plot = window_summary.copy()

window_plot["booking_window"] = pd.Categorical(
    "T+" + window_plot["booking_window"].astype(str),
    categories=["T+1", "T+7", "T+15", "T+30", "T+45"],
    ordered=True,
)

window_plot = window_plot.sort_values("booking_window")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=window_plot["booking_window"],
        y=window_plot["index"],
        mode="lines+markers",
        line=dict(
            color="#17382D",
            width=3,
        ),
        marker=dict(
            color="#A74628",
            size=9,
            line=dict(
                color="#F7F5EF",
                width=2,
            ),
        ),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Relative index: %{y:.2f}"
            "<extra></extra>"
        ),
    )
)

fig.update_layout(
    height=330,
    margin=dict(l=20, r=20, t=10, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="DM Sans, sans-serif",
        color="#292925",
    ),
    xaxis=dict(
        title=None,
        categoryorder="array",
        categoryarray=["T+1", "T+7", "T+15", "T+30", "T+45"],
        showgrid=False,
        linecolor="#D9D7CE",
        tickfont=dict(color="#62615B"),
    ),
    yaxis=dict(
        title="Relative index",
        range=[98, 124],
        showgrid=True,
        gridcolor="#D9D7CE",
        gridwidth=1,
        zeroline=False,
        title_font=dict(color="#62615B"),
        tickfont=dict(color="#62615B"),
    ),
    hoverlabel=dict(
        bgcolor="#17382D",
        font_color="#F7F5EF",
    ),
)

st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False},
)


# ---------------------------------------------------------
# INTERPRETATION
# ---------------------------------------------------------

aeris_markdown(
    """
    <div class="benchmark-card">

        <div class="benchmark-title">
            How to read the CPI connection
        </div>

        <div class="benchmark-text">
            If the AERIS airfare index rises persistently, airfare-related
            consumer spending may experience stronger price pressure.
            However, the effect on headline CPI depends on the official
            CPI classification, expenditure weight, coverage and methodology.
            AERIS therefore provides the airfare movement signal first,
            while official CPI weights and benchmark series provide the
            next layer of validation.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# FOOTNOTE
# ---------------------------------------------------------

st.caption(
    "AERIS prototype · Airfare-specific analytical indicator · "
    "Not an official Government of India CPI estimate"
)
