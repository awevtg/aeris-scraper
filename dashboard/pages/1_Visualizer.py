import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.index_engine import load_observations


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AERIS — Visualizer",
    page_icon="✈",
    layout="wide",
)


# =========================================================
# DATA
# =========================================================

DATA_PATH = ROOT / "data" / "raw" / "backtest_airfares.json"

observations = load_observations(str(DATA_PATH))
df = pd.DataFrame(observations)

df["date"] = pd.to_datetime(df["collected_at"]).dt.date
df["total_fare"] = pd.to_numeric(df["total_fare"], errors="coerce")
df["base_fare"] = pd.to_numeric(df["base_fare"], errors="coerce")
df["taxes"] = pd.to_numeric(df["taxes"], errors="coerce")
df["fees"] = pd.to_numeric(df["fees"], errors="coerce")

df = df[df["total_fare"] > 0].copy()


# =========================================================
# AERIS STYLE
# =========================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap'
    );

    /* PAGE */

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
    /* GLOBAL TEXT */

    .stApp p,
    .stApp label,
    .stApp span {
        font-family: "DM Sans", sans-serif;
    }

    /* HEADER */

    .eyebrow {
        color: #A74628 !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 1.7px !important;
        text-transform: uppercase !important;
        margin-bottom: 8px !important;
    }

    .main-title {
        color: #17382D !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 58px !important;
        line-height: 0.95 !important;
        font-weight: 600 !important;
        margin: 0 0 12px 0 !important;
    }

    .subtitle {
        color: #706F68 !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 16px !important;
        margin-bottom: 30px !important;
    }

    /* CONTROL LABELS */

    [data-testid="stSelectbox"] label {
        color: #17382D !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }

    [data-testid="stSelectbox"] label p {
        color: #17382D !important;
    }

    /* SELECT BOX */

    [data-baseweb="select"] {
        background: #FBFAF6 !important;
        border: 1px solid #D9D7CE !important;
        border-radius: 10px !important;
    }

    [data-baseweb="select"] div {
        color: #292925 !important;
        background: transparent !important;
    }

    [data-baseweb="select"] span {
        color: #292925 !important;
    }

    /* DROPDOWN */

    [role="listbox"] {
        background: #FBFAF6 !important;
    }

    [role="option"] {
        color: #292925 !important;
        background: #FBFAF6 !important;
    }

    [role="option"]:hover {
        background: #E8E5DB !important;
    }

    /* ROUTE BANNER */

    .route-banner {
        background: #17382D;
        color: #FBFAF6;
        border-radius: 18px;
        padding: 30px 34px;
        margin: 18px 0 26px 0;
    }

    .route-label {
        color: #DCE6DF !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
    }

    .route-name {
        color: #FFFFFF !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 44px !important;
        line-height: 1 !important;
        font-weight: 600 !important;
        margin-top: 7px !important;
    }

    .route-code {
        color: #DCE6DF !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 13px !important;
        margin-top: 8px !important;
    }

    /* KPI CARDS */

    .kpi-card {
        background: #FBFAF6;
        border: 1px solid #D9D7CE;
        border-radius: 15px;
        padding: 20px 21px;
        min-height: 128px;
        box-sizing: border-box;
    }

    .kpi-label {
        color: #706F68 !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
    }

    .kpi-value {
        color: #17382D !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 34px !important;
        line-height: 1 !important;
        font-weight: 600 !important;
        margin-top: 10px !important;
    }

    .kpi-note {
        color: #706F68 !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 11px !important;
        margin-top: 8px !important;
    }

    /* SECTIONS */

    .section-title {
        color: #17382D !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 34px !important;
        font-weight: 600 !important;
        margin-top: 42px !important;
        margin-bottom: 4px !important;
    }

    .section-copy {
        color: #706F68 !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 13px !important;
        margin-bottom: 18px !important;
    }

    .chart-card {
        background: #FBFAF6;
        border: 1px solid #D9D7CE;
        border-radius: 16px;
        padding: 18px 20px 12px 20px;
    }

    .chart-label {
        color: #17382D !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
        margin-bottom: 8px !important;
    }

    .note {
        color: #706F68 !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 11px !important;
        margin-top: 18px !important;
    }
    /* AERIS NAVIGATION */

.aeris-nav {
    border-bottom: 1px solid #D9D7CE;
    padding: 4px 0 16px 0;
    margin-bottom: 28px;
}

.aeris-brand {
    display: flex;
    align-items: center;
    gap: 11px;
}

.brand-mark {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #17382D;
    color: #F5F4EF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
}

.brand-name {
    color: #17382D;
    font-family: "DM Sans", sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 2px;
}

.brand-subtitle {
    color: #8A887F;
    font-family: "DM Sans", sans-serif;
    font-size: 8px;
    font-weight: 600;
    letter-spacing: 1.2px;
    margin-top: 2px;
}

.aeris-nav [data-testid="stPageLink"] {
    margin: 0 !important;
}

.aeris-nav [data-testid="stPageLink"] a {
    color: #706F68 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 7px 2px !important;
    min-height: 0 !important;
    font-family: "DM Sans", sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    text-decoration: none !important;
}

.aeris-nav [data-testid="stPageLink"] a:hover {
    color: #17382D !important;
    background: transparent !important;
}

.nav-active {
    color: #A74628 !important;
    font-family: "DM Sans", sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    padding: 7px 2px 5px 2px !important;
    border-bottom: 2px solid #A74628;
    display: inline-block;
}
    /* FINAL AERIS NAV TEXT FIX */

    .aeris-nav [data-testid="stPageLink"] a,
    .aeris-nav [data-testid="stPageLink"] a *,
    .aeris-nav [data-testid="stPageLink"] a p,
    .aeris-nav [data-testid="stPageLink"] a span {
        color: #706F68 !important;
        -webkit-text-fill-color: #706F68 !important;
        opacity: 1 !important;
    }

    .aeris-nav [data-testid="stPageLink"] a:hover,
    .aeris-nav [data-testid="stPageLink"] a:hover *,
    .aeris-nav [data-testid="stPageLink"] a:hover p,
    .aeris-nav [data-testid="stPageLink"] a:hover span {
        color: #17382D !important;
        -webkit-text-fill-color: #17382D !important;
        opacity: 1 !important;
    }

    .aeris-nav .nav-active,
    .aeris-nav .nav-active * {
        color: #A74628 !important;
        -webkit-text-fill-color: #A74628 !important;
        opacity: 1 !important;
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

    </style>
    """,
    unsafe_allow_html=True,
)
# =========================================================
# AERIS NAVIGATION
# =========================================================

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
        st.markdown('<div class="nav-active">VISUALIZER</div>', unsafe_allow_html=True)

    with n3:
        st.page_link("pages/2_Blooms_Taxonomy.py", label="TAXONOMY")

    with n4:
        st.page_link("pages/3_CPI_Impact.py", label="CPI IMPACT")

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="eyebrow">02 — Data visualisation</div>
    <div class="main-title">The Airfare Visualizer</div>
    <div class="subtitle">
        See how airfare movement changes across routes and booking horizons.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CONTROLS
# =========================================================

routes = (
    df[["origin", "destination"]]
    .drop_duplicates()
    .sort_values(["origin", "destination"])
)

route_options = [
    (row.origin, row.destination)
    for row in routes.itertuples()
]

route_names = {
    ("DEL", "BOM"): "Delhi → Mumbai",
    ("DEL", "BLR"): "Delhi → Bengaluru",
    ("DEL", "HYD"): "Delhi → Hyderabad",
    ("DEL", "CCU"): "Delhi → Kolkata",
    ("BOM", "BLR"): "Mumbai → Bengaluru",
    ("BLR", "HYD"): "Bengaluru → Hyderabad",
    ("MAA", "DEL"): "Chennai → Delhi",
}

c1, c2, c3 = st.columns([1.5, 1.2, 1.2])

with c1:
    route = st.selectbox(
        "Route",
        route_options,
        format_func=lambda x: route_names.get(
            x,
            f"{x[0]} → {x[1]}",
        ),
    )

with c2:
    window = st.selectbox(
        "Booking window",
        [1, 7, 15, 30, 45],
        format_func=lambda x: f"T+{x}",
    )

with c3:
    period = st.selectbox(
        "Trend period",
        ["30 days", "14 days", "7 days"],
    )


origin, destination = route


# =========================================================
# SELECTED DATA
# =========================================================

selected = df[
    (df["origin"] == origin)
    & (df["destination"] == destination)
    & (df["booking_window"] == window)
].copy()

selected = selected.sort_values("date")

number_of_days = {
    "30 days": 30,
    "14 days": 14,
    "7 days": 7,
}[period]

latest = selected["date"].max()
cutoff = latest - pd.Timedelta(days=number_of_days - 1)

selected = selected[selected["date"] >= cutoff].copy()

selected["index"] = (
    selected["total_fare"]
    / selected["total_fare"].iloc[0]
) * 100


# =========================================================
# ROUTE BANNER
# =========================================================

st.markdown(
    f"""
    <div class="route-banner">
        <div class="route-label">Selected route · T+{window}</div>
        <div class="route-name">{route_names.get(route, f"{origin} → {destination}")}</div>
        <div class="route-code">{origin} &nbsp; → &nbsp; {destination}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# KPIs
# =========================================================

current = float(selected.iloc[-1]["total_fare"])
starting = float(selected.iloc[0]["total_fare"])

avg_base = float(selected["base_fare"].mean())

avg_tax_fee = float(
    selected["taxes"].mean()
    + selected["fees"].mean()
)

current_index = float(selected.iloc[-1]["index"])

movement = ((current / starting) - 1) * 100


k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Current fare</div>
            <div class="kpi-value">₹{current:,.0f}</div>
            <div class="kpi-note">Latest observed total fare</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Average base fare</div>
            <div class="kpi-value">₹{avg_base:,.0f}</div>
            <div class="kpi-note">Observed base component</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Taxes + fees</div>
            <div class="kpi-value">₹{avg_tax_fee:,.0f}</div>
            <div class="kpi-note">Average non-base component</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Airfare movement</div>
            <div class="kpi-value">{movement:+.1f}%</div>
            <div class="kpi-note">Across selected trend period</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FARE MOVEMENT
# =========================================================

st.markdown(
    """
    <div class="section-title">Fare movement</div>
    <div class="section-copy">
        How the selected route moved during the chosen observation period.
    </div>
    """,
    unsafe_allow_html=True,
)

fare_chart_df = selected[
    ["date", "total_fare", "index"]
].copy()

fare_chart_df["date"] = pd.to_datetime(fare_chart_df["date"])

fare_chart = (
    alt.Chart(fare_chart_df)
    .mark_line(
        color="#17382D",
        strokeWidth=3,
        point=True,
    )
    .encode(
        x=alt.X(
            "date:T",
            title=None,
            axis=alt.Axis(
                format="%d %b",
                labelColor="#292925",
                labelFont="DM Sans",
                labelFontSize=11,
                tickColor="#D9D7CE",
                domainColor="#D9D7CE",
                grid=False,
            ),
        ),
        y=alt.Y(
            "total_fare:Q",
            title="Fare (₹)",
            axis=alt.Axis(
                labelColor="#292925",
                titleColor="#706F68",
                labelFont="DM Sans",
                titleFont="DM Sans",
                labelFontSize=11,
                titleFontSize=11,
                grid=True,
                gridColor="#D9D7CE",
                gridOpacity=0.5,
            ),
        ),
        tooltip=[
            alt.Tooltip(
                "date:T",
                title="Date",
                format="%d %b %Y",
            ),
            alt.Tooltip(
                "total_fare:Q",
                title="Fare",
                format=",.0f",
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
    .configure_view(strokeWidth=0)
)

st.altair_chart(
    fare_chart,
    use_container_width=True,
)


# =========================================================
# BOOKING HORIZON
# =========================================================

st.markdown(
    """
    <div class="section-title">Booking horizon</div>
    <div class="section-copy">
        Compare the airfare signal across T+1, T+7, T+15, T+30 and T+45.
    </div>
    """,
    unsafe_allow_html=True,
)

horizon = (
    df[
        (df["origin"] == origin)
        & (df["destination"] == destination)
    ]
    .groupby("booking_window", as_index=False)["total_fare"]
    .mean()
    .sort_values("booking_window")
)

horizon["window_label"] = horizon["booking_window"].map(
    lambda x: f"T+{x}"
)

horizon_chart = (
    alt.Chart(horizon)
    .mark_line(
        color="#A74628",
        strokeWidth=3,
        point=alt.OverlayMarkDef(
            filled=True,
            size=75,
        ),
    )
    .encode(
        x=alt.X(
            "window_label:N",
            sort=["T+1", "T+7", "T+15", "T+30", "T+45"],
            title=None,
            axis=alt.Axis(
                labelColor="#292925",
                labelFont="DM Sans",
                labelFontSize=12,
                tickColor="#D9D7CE",
                domainColor="#D9D7CE",
            ),
        ),
        y=alt.Y(
            "total_fare:Q",
            title="Average fare (₹)",
            axis=alt.Axis(
                labelColor="#292925",
                titleColor="#706F68",
                labelFont="DM Sans",
                titleFont="DM Sans",
                labelFontSize=11,
                titleFontSize=11,
                grid=True,
                gridColor="#D9D7CE",
                gridOpacity=0.5,
            ),
        ),
        tooltip=[
            alt.Tooltip(
                "window_label:N",
                title="Booking window",
            ),
            alt.Tooltip(
                "total_fare:Q",
                title="Average fare",
                format=",.0f",
            ),
        ],
    )
    .properties(
        height=330,
        background="transparent",
    )
    .configure_view(strokeWidth=0)
)

st.altair_chart(
    horizon_chart,
    use_container_width=True,
)


# =========================================================
# LEAD-TIME ELASTICITY
# =========================================================

st.markdown(
    """
    <div class="section-title">Lead-time elasticity</div>
    <div class="section-copy">
        The relative fare level across booking horizons. This shows how
        price pressure changes as the departure date approaches.
    </div>
    """,
    unsafe_allow_html=True,
)

elasticity = horizon.copy()

base_horizon_fare = float(
    elasticity.iloc[0]["total_fare"]
)

elasticity["relative_index"] = (
    elasticity["total_fare"]
    / base_horizon_fare
) * 100

elasticity_chart = (
    alt.Chart(elasticity)
    .mark_line(
        color="#17382D",
        strokeWidth=3,
        point=True,
    )
    .encode(
        x=alt.X(
            "window_label:N",
            sort=["T+1", "T+7", "T+15", "T+30", "T+45"],
            title=None,
            axis=alt.Axis(
                labelColor="#292925",
                labelFont="DM Sans",
                labelFontSize=12,
                tickColor="#D9D7CE",
                domainColor="#D9D7CE",
            ),
        ),
        y=alt.Y(
            "relative_index:Q",
            title="Relative fare index",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(
                labelColor="#292925",
                titleColor="#706F68",
                labelFont="DM Sans",
                titleFont="DM Sans",
                grid=True,
                gridColor="#D9D7CE",
                gridOpacity=0.5,
            ),
        ),
        tooltip=[
            alt.Tooltip(
                "window_label:N",
                title="Booking window",
            ),
            alt.Tooltip(
                "relative_index:Q",
                title="Relative index",
                format=".2f",
            ),
        ],
    )
    .properties(
        height=330,
        background="transparent",
    )
    .configure_view(strokeWidth=0)
)

st.altair_chart(
    elasticity_chart,
    use_container_width=True,
)


# =========================================================
# FOOTNOTE
# =========================================================

st.markdown(
    """
    <div class="note">
        AERIS is an aggregate airfare intelligence system. These
        visualisations describe observed market movement and are not
        personalised fare forecasts or booking recommendations.
    </div>
    """,
    unsafe_allow_html=True,
)
