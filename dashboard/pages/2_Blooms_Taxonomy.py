import streamlit as st

st.set_page_config(
    page_title="AERIS — Taxonomy Engine",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# AERIS DESIGN SYSTEM
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

    :root {
        --green: #17382D;
        --green-soft: #E7EEE8;
        --ivory: #FBFAF6;
        --paper: #F2EFE7;
        --line: #D9D7CE;
        --muted: #68665F;
        --rust: #A74628;
        --rust-soft: #F5E8E2;
    }

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }

    .stApp {
        background: var(--ivory);
    }

    /* Hide Streamlit chrome */
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 5rem;
        max-width: 1320px;
    }

    /* =====================================================
       NAVIGATION
       ===================================================== */

    .aeris-nav {
        border-bottom: 1px solid var(--line);
        padding: 8px 0 18px 0;
        margin-bottom: 34px;
    }

    .brand-mark {
        color: var(--green);
        font-size: 28px;
        line-height: 1;
        margin-bottom: 2px;
    }

    .brand-name {
        color: var(--green);
        font-family: "Cormorant Garamond", serif;
        font-size: 31px;
        line-height: .85;
        font-weight: 700;
        letter-spacing: .02em;
    }

    .brand-sub {
        color: var(--muted);
        font-size: 7px;
        font-weight: 700;
        letter-spacing: .16em;
        margin-top: 7px;
        white-space: nowrap;
    }

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
    padding: 9px 0 !important;
    min-height: 0 !important;
    height: auto !important;
    text-decoration: none !important;
}

.aeris-nav [data-testid="stPageLink"] a:hover,
.aeris-nav [data-testid="stPageLink"] button:hover,
.aeris-nav [data-testid="stPageLink"] a:hover p {
    color: var(--green) !important;
}

    [data-testid="stPageLink"] a p,
    [data-testid="stPageLink"] button p {
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
        letter-spacing: inherit !important;
    }

    .nav-active {
        color: var(--green);
        font-size: 9px;
        font-weight: 700;
        letter-spacing: .14em;
        padding: 9px 0 7px 0;
        border-bottom: 2px solid var(--rust);
        white-space: nowrap;
    }

    /* =====================================================
       HERO
       ===================================================== */

    .tax-hero {
        background: var(--green);
        color: var(--ivory);
        padding: 48px 54px 52px 54px;
        border-radius: 10px;
        margin-bottom: 58px;
    }

    .eyebrow {
        font-size: 10px;
        letter-spacing: .2em;
        text-transform: uppercase;
        font-weight: 700;
        color: #D7E1D9;
        margin-bottom: 15px;
    }

    .tax-title {
        font-family: "Cormorant Garamond", serif;
        font-size: 62px;
        line-height: .92;
        font-weight: 600;
        margin: 0 0 18px 0;
        letter-spacing: -.02em;
    }

    .tax-subtitle {
        font-size: 14px;
        line-height: 1.75;
        max-width: 820px;
        color: #E8EEE9;
    }

    /* =====================================================
       SECTION HEADERS
       ===================================================== */

    .section-label {
        font-size: 9px;
        letter-spacing: .2em;
        text-transform: uppercase;
        font-weight: 700;
        color: var(--rust);
        margin: 0 0 8px 0;
    }

    .section-title {
        font-family: "Cormorant Garamond", serif;
        font-size: 40px;
        line-height: 1;
        font-weight: 600;
        color: var(--green);
        margin: 0 0 25px 0;
        letter-spacing: -.015em;
    }

    .section-intro {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.7;
        max-width: 760px;
        margin: -8px 0 26px 0;
    }

    /* =====================================================
       BLOOM CARDS
       ===================================================== */

  
    .bloom-card {
        background: #F8F6F0;
        border: 1px solid var(--line);
        border-top: 3px solid var(--green);
        border-radius: 10px;
        padding: 26px 28px 24px 28px;
        min-height: 230px;
        height: 230px;
        box-sizing: border-box;
        margin-bottom: 22px;
}

    .bloom-number {
        color: var(--rust);
        font-size: 9px;
        font-weight: 700;
        letter-spacing: .18em;
        margin-bottom: 15px;
    }

    .bloom-card h3 {
        color: var(--green);
        font-family: "Cormorant Garamond", serif;
        font-size: 29px;
        line-height: 1;
        font-weight: 600;
        margin: 0 0 13px 0;
    }

    .bloom-card p {
        color: #5E5C55;
        font-size: 12px;
        line-height: 1.65;
        margin: 0 0 17px 0;
    }

    .tag {
        display: inline-block;
        background: var(--green-soft);
        color: var(--green);
        padding: 5px 9px;
        border-radius: 3px;
        font-size: 8px;
        font-weight: 700;
        letter-spacing: .08em;
        margin: 2px 3px 2px 0;
    }

    /* =====================================================
       PARAMETER CARDS
       ===================================================== */

    .parameter-card {
        background: #F8F6F0;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 25px;
        min-height: 235px;
        margin-bottom: 18px;
    }

    .parameter-card h3 {
        color: var(--green);
        font-family: "Cormorant Garamond", serif;
        font-size: 27px;
        line-height: 1.05;
        font-weight: 600;
        margin: 0 0 11px 0;
    }

    .parameter-card p {
        color: #5E5C55;
        font-size: 12px;
        line-height: 1.65;
        margin-bottom: 14px;
    }

    /* =====================================================
       OUTPUTS
       ===================================================== */

    .output-card {
        background: var(--green);
        color: var(--ivory);
        border-radius: 8px;
        padding: 27px;
        min-height: 165px;
        margin-bottom: 18px;
    }

    .output-card h3 {
        font-family: "Cormorant Garamond", serif;
        font-size: 28px;
        line-height: 1;
        font-weight: 600;
        margin: 0 0 12px 0;
    }

    .output-card p {
        color: #DCE5DE;
        font-size: 11px;
        line-height: 1.7;
        margin: 0;
    }

    /* =====================================================
       PIPELINE
       ===================================================== */

    .pipeline {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 30px 25px;
        margin-top: 10px;
    }

    .pipeline-step {
        padding: 10px 8px;
        text-align: center;
    }

    .pipeline-number {
        color: var(--rust);
        font-size: 8px;
        font-weight: 700;
        letter-spacing: .15em;
        margin-bottom: 7px;
    }

    .pipeline-step strong {
        display: block;
        color: var(--green);
        font-size: 11px;
        letter-spacing: .08em;
        margin-bottom: 7px;
    }

    .pipeline-step span {
        display: block;
        color: #77746B;
        font-size: 10px;
        line-height: 1.45;
    }

    /* =====================================================
       EXPLANATION / NOTE
       ===================================================== */

    .reasoning-note {
        background: var(--rust-soft);
        border-left: 3px solid var(--rust);
        padding: 21px 23px;
        border-radius: 5px;
        margin-top: 28px;
        color: #51372F;
        font-size: 12px;
        line-height: 1.7;
    }

    .reasoning-note strong {
        color: var(--rust);
    }

    /* =====================================================
       SPACING
       ===================================================== */

    .section-block {
        margin-bottom: 62px;
    }

    /* Thin scrollbar */
    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: var(--ivory);
    }

    ::-webkit-scrollbar-thumb {
        background: #B9B6AD;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--green);
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

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HEADER / NAVIGATION
# =========================================================

st.markdown('<div class="aeris-nav">', unsafe_allow_html=True)

left, right = st.columns([1.7, 3.3])

with left:
    st.markdown(
        """
        <div class="brand-mark">✈</div>
        <div class="brand-name">AERIS</div>
        <div class="brand-sub">AIRFARE ECONOMICS & REGIONAL INTELLIGENCE</div>
        """,
        unsafe_allow_html=True,
    )

with right:
    n1, n2, n3, n4 = st.columns(4)

    with n1:
        st.page_link("app.py", label="NARRATIVE")

    with n2:
        st.page_link("pages/1_Visualizer.py", label="VISUALIZER")

    with n3:
        st.markdown(
            '<div class="nav-active">TAXONOMY</div>',
            unsafe_allow_html=True,
        )

    with n4:
        st.page_link("pages/3_CPI_Impact.py", label="CPI IMPACT")

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.html(
    """
    <div class="tax-hero">
        <div class="eyebrow">AERIS · INTELLIGENCE ARCHITECTURE</div>

        <div class="tax-title">The Taxonomy Engine</div>

        <div class="tax-subtitle">
            AERIS moves from raw airfare observations to measurable signals,
            then turns those signals into explanations of how and why airfares move.
            Bloom's Taxonomy provides the reasoning structure behind that progression.
        </div>
    </div>
    """
)
# =========================================================
# 01 — HOW AERIS THINKS
# =========================================================

st.markdown('<div class="section-block">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">01 · How AERIS thinks</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">From data to intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-intro">
        The six Bloom levels are mapped to an operational reasoning chain.
        Each stage answers a different question: what was observed, what it means,
        how it can be measured, what patterns emerge, whether those signals are
        robust, and what intelligence can finally be produced.
    </div>
    """,
    unsafe_allow_html=True,
)

stages = [
    (
        "01",
        "Remember",
        "Collect the factual airfare observations that establish the evidence base.",
        "DATA",
    ),
    (
        "02",
        "Understand",
        "Interpret what the observations represent across routes, airlines and booking horizons.",
        "UNDERSTANDING",
    ),
    (
        "03",
        "Apply",
        "Standardize observations into comparable fare measures and route × booking-window strata.",
        "MEASUREMENT",
    ),
    (
        "04",
        "Analyse",
        "Identify movement, relationships and changes across routes, horizons and market conditions.",
        "ANALYSIS",
    ),
    (
        "05",
        "Evaluate",
        "Test signals against data quality, consistency, anomalies and methodological assumptions.",
        "EVALUATION",
    ),
    (
        "06",
        "Create",
        "Turn validated signals into an index, explanations and policy-oriented intelligence.",
        "INTELLIGENCE",
    ),
]

for start in range(0, 6, 3):
    cols = st.columns(3)

    for col, (num, title, desc, output) in zip(cols, stages[start:start + 3]):
        with col:
            st.markdown(
                f"""
                <div class="bloom-card">
                    <div class="bloom-number">{num}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <span class="tag">{output}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 02 — PARAMETER TAXONOMY
# =========================================================

st.markdown('<div class="section-block">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">02 · AERIS parameter taxonomy</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">What the system observes</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-intro">
        AERIS does not treat airfare as a single number. It separates the
        observation into price, flight, timing, supply, demand, regional,
        calendar and external factors so that later analysis has context.
    </div>
    """,
    unsafe_allow_html=True,
)

categories = [
    (
        "01",
        "Price & Flight",
        "The core airfare observation and flight-quality layer.",
        [
            "Total fare", "Base fare", "Taxes & fees", "Airline",
            "Route", "Departure date", "Stops", "Journey duration", "Fare class"
        ],
    ),
    (
        "02",
        "Booking & Lead Time",
        "Captures how fare behaviour changes as departure approaches.",
        [
            "Booking timestamp", "T+1", "T+7", "T+15",
            "T+30", "T+45", "Days before departure", "Last-minute"
        ],
    ),
    (
        "03",
        "Supply & Capacity",
        "Describes the amount and structure of available air transport.",
        [
            "Flights/day", "Airlines", "Frequency", "Route capacity",
            "Availability", "Cancellations", "Route changes"
        ],
    ),
    (
        "04",
        "Demand & Market Activity",
        "Uses aggregate market activity and passenger data as demand proxies.",
        [
            "City-pair traffic", "Airport traffic", "Historical volume",
            "Availability signals", "Booking pressure"
        ],
    ),
    (
        "05",
        "Calendar & Regional",
        "Captures predictable regional and seasonal variation.",
        [
            "Festivals", "Regional holidays", "School holidays",
            "Tourism seasons", "Major events", "Origin region", "Destination region"
        ],
    ),
    (
        "06",
        "External & Disruption",
        "Captures shocks originating outside normal fare dynamics.",
        [
            "Weather", "Fog", "Storms", "Airport disruption",
            "Strikes", "Airspace", "ATF prices", "Economic indicators"
        ],
    ),
]

for start in range(0, 6, 3):
    cols = st.columns(3)

    for col, (num, title, desc, tags) in zip(
        cols,
        categories[start:start + 3],
    ):
        with col:
            tags_html = "".join(
                f'<span class="tag">{tag}</span>'
                for tag in tags
            )

            st.markdown(
                f"""
                <div class="parameter-card">
                    <div class="bloom-number">{num}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    {tags_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 03 — INTELLIGENCE OUTPUTS
# =========================================================

st.markdown('<div class="section-block">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">03 · Intelligence outputs</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">What AERIS derives from the data</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-intro">
        These outputs sit above the core Airfare Price Index. They provide
        analytical context around movement without being presented as
        replacements for official statistics.
    </div>
    """,
    unsafe_allow_html=True,
)

outputs = [
    (
        "Airfare Volatility Index",
        "Measures instability and abnormal movement in airfare prices across the observed basket.",
    ),
    (
        "Booking Pressure Index",
        "Measures how strongly observed fares respond as departure approaches.",
    ),
    (
        "Regional Airfare Inflation",
        "Tracks airfare movement across defined regional route baskets.",
    ),
    (
        "Festival Surge Index",
        "Measures event-related airfare pressure when a meaningful signal is present.",
    ),
    (
        "Route Competition Index",
        "Describes competitive intensity using observable airlines, frequency and capacity.",
    ),
    (
        "Supply-Demand Pressure",
        "Combines observable market-pressure signals without treating them as official statistics.",
    ),
]

for start in range(0, 6, 3):
    cols = st.columns(3)

    for col, (title, desc) in zip(cols, outputs[start:start + 3]):
        with col:
            st.markdown(
                f"""
                <div class="output-card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 04 — PIPELINE
# =========================================================

st.markdown('<div class="section-block">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">04 · The AERIS intelligence pipeline</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">From observation to signal</div>',
    unsafe_allow_html=True,
)

pipeline = [
    ("01", "RAW DATA", "Airline + OTA observations"),
    ("02", "CLEAN", "Validation + normalization"),
    ("03", "STANDARDIZE", "Route × booking window"),
    ("04", "MEASURE", "Price relatives + Jevons"),
    ("05", "EXPLAIN", "Supply + demand + events"),
    ("06", "INTELLIGENCE", "Index + derived signals"),
]

st.markdown('<div class="pipeline">', unsafe_allow_html=True)

cols = st.columns(6)

for col, (num, title, desc) in zip(cols, pipeline):
    with col:
        st.markdown(
            f"""
            <div class="pipeline-step">
                <div class="pipeline-number">{num}</div>
                <strong>{title}</strong>
                <span>{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="reasoning-note">
        <strong>Why this matters:</strong>
        AERIS separates observation from interpretation.
        The airfare index is produced from standardized price observations,
        while the surrounding intelligence layers explain the conditions
        associated with movement. This keeps the measurement layer
        transparent and the analytical layer traceable.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        border-top:1px solid #D9D7CE;
        margin-top:20px;
        padding-top:18px;
        color:#77746B;
        font-size:9px;
        letter-spacing:.08em;
    ">
        AERIS · AIRFARE ECONOMICS & REGIONAL INTELLIGENCE · PROTOTYPE
    </div>
    """,
    unsafe_allow_html=True,
)
