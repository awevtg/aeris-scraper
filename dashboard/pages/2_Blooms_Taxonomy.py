import streamlit as st

st.set_page_config(
    page_title="AERIS — Taxonomy Engine",
    page_icon="✈",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}

.tax-hero {
    background: #17382D;
    color: #FBFAF6;
    padding: 46px 52px;
    border-radius: 24px;
    margin-bottom: 28px;
}

.eyebrow {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 700;
    opacity: .72;
    margin-bottom: 12px;
}

.tax-title {
    font-family: "Cormorant Garamond", serif;
    font-size: 54px;
    line-height: .95;
    margin: 0 0 16px 0;
}

.tax-subtitle {
    font-size: 16px;
    line-height: 1.7;
    max-width: 760px;
    opacity: .88;
}

.section-label {
    font-size: 11px;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    font-weight: 700;
    color: #A74628;
    margin: 34px 0 8px 0;
}

.section-title {
    font-family: "Cormorant Garamond", serif;
    font-size: 36px;
    color: #17382D;
    margin: 0 0 18px 0;
}

.tax-card {
    background: #FBFAF6;
    border: 1px solid #D9D7CE;
    border-radius: 18px;
    padding: 22px;
    min-height: 205px;
    margin-bottom: 16px;
}

.tax-number {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #A74628;
    margin-bottom: 8px;
}

.tax-card h3 {
    font-family: "Cormorant Garamond", serif;
    color: #17382D;
    font-size: 27px;
    margin: 0 0 10px 0;
}

.tax-card p {
    color: #55544D;
    font-size: 13px;
    line-height: 1.65;
    margin-bottom: 12px;
}

.tag {
    display: inline-block;
    background: #E7EEE8;
    color: #17382D;
    padding: 5px 9px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    margin: 3px 3px 0 0;
}

.flow {
    background: #F0EDE5;
    border: 1px solid #D9D7CE;
    border-radius: 20px;
    padding: 28px;
    margin-top: 14px;
}

.flow-step {
    text-align: center;
    padding: 12px 8px;
}

.flow-step strong {
    display: block;
    color: #17382D;
    font-size: 14px;
    margin-bottom: 5px;
}

.flow-step span {
    color: #68665F;
    font-size: 11px;
}

.output-card {
    background: #17382D;
    color: #FBFAF6;
    border-radius: 20px;
    padding: 28px;
    min-height: 150px;
}

.output-card h3 {
    font-family: "Cormorant Garamond", serif;
    font-size: 27px;
    margin: 0 0 8px 0;
}

.output-card p {
    font-size: 12px;
    line-height: 1.6;
    opacity: .82;
}

.note {
    background: #F5E8E2;
    border-left: 4px solid #A74628;
    padding: 18px 20px;
    border-radius: 10px;
    color: #4A3027;
    font-size: 13px;
    line-height: 1.65;
    margin-top: 26px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tax-hero">
    <div class="eyebrow">AERIS · INTELLIGENCE ARCHITECTURE</div>
    <div class="tax-title">The Taxonomy Engine</div>
    <div class="tax-subtitle">
        AERIS moves from raw airfare observations to measurable signals,
        then turns those signals into explanations of how and why airfares move.
        The system is broader than any single event, season or market factor.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">01 · How AERIS thinks</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">From data to intelligence</div>', unsafe_allow_html=True)

cols = st.columns(6)

stages = [
    ("01", "Remember", "Collect the facts", "DATA"),
    ("02", "Understand", "Interpret the market", "UNDERSTANDING"),
    ("03", "Apply", "Standardize observations", "MEASUREMENT"),
    ("04", "Analyse", "Find movement & relationships", "ANALYSIS"),
    ("05", "Evaluate", "Test signals & robustness", "EVALUATION"),
    ("06", "Create", "Produce actionable intelligence", "INTELLIGENCE"),
]

for col, (num, title, desc, output) in zip(cols, stages):
    with col:
        st.markdown(f"""
        <div class="tax-card" style="min-height:170px;">
            <div class="tax-number">{num}</div>
            <h3>{title}</h3>
            <p>{desc}</p>
            <span class="tag">{output}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-label">02 · AERIS parameter taxonomy</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">What the system observes</div>', unsafe_allow_html=True)

categories = [
    (
        "01",
        "Price & Flight",
        "The core airfare observation and flight-quality layer.",
        ["Total fare", "Base fare", "Taxes & fees", "Airline", "Route", "Departure date", "Stops", "Journey duration", "Fare class"]
    ),
    (
        "02",
        "Booking & Lead Time",
        "Measures how fare behaviour changes as departure approaches.",
        ["Booking timestamp", "T+1", "T+7", "T+15", "T+30", "T+45", "Days before departure", "Last-minute"]
    ),
    (
        "03",
        "Supply & Capacity",
        "Describes the amount and structure of available air transport.",
        ["Flights/day", "Airlines", "Frequency", "Route capacity", "Availability", "Cancellations", "Route changes"]
    ),
    (
        "04",
        "Demand & Market Activity",
        "Uses aggregate market activity and passenger data as demand proxies.",
        ["City-pair traffic", "Airport traffic", "Historical volume", "Availability signals", "Booking pressure"]
    ),
    (
        "05",
        "Calendar & Regional",
        "Captures predictable regional and seasonal variation.",
        ["Festivals", "Regional holidays", "School holidays", "Tourism seasons", "Major events", "Origin region", "Destination region"]
    ),
    (
        "06",
        "External & Disruption",
        "Captures shocks originating outside normal fare dynamics.",
        ["Weather", "Fog", "Storms", "Airport disruption", "Strikes", "Airspace", "ATF prices", "Economic indicators"]
    ),
]

for start in range(0, len(categories), 3):
    row = categories[start:start+3]
    cols = st.columns(3)
    for col, (num, title, desc, tags) in zip(cols, row):
        with col:
            tags_html = "".join(f'<span class="tag">{x}</span>' for x in tags)
            st.markdown(f"""
            <div class="tax-card">
                <div class="tax-number">{num}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
                {tags_html}
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div class="section-label">03 · Intelligence outputs</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">What AERIS derives from the data</div>', unsafe_allow_html=True)

outputs = [
    ("Airfare Volatility Index", "Measures instability and abnormal movement in airfare prices."),
    ("Booking Pressure Index", "Measures how strongly fares respond as departure approaches."),
    ("Regional Airfare Inflation", "Tracks airfare movement across defined regional baskets."),
    ("Festival Surge Index", "Measures event-related airfare pressure when a meaningful signal exists."),
    ("Route Competition Index", "Describes competitive intensity using airlines, frequency and capacity."),
    ("Supply-Demand Pressure", "Combines observable market pressure signals without treating them as official statistics."),
]

cols = st.columns(3)
for col, (title, desc) in zip(cols, outputs):
    with col:
        st.markdown(f"""
        <div class="output-card">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-label">04 · The AERIS intelligence pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">From observation to signal</div>', unsafe_allow_html=True)

st.markdown("""
<div class="flow">
    <div class="flow-step">
        <strong>RAW DATA</strong>
        <span>Airline + OTA observations</span>
    </div>
    <div class="flow-step">
        <strong>CLEAN</strong>
        <span>Validation + normalization</span>
    </div>
    <div class="flow-step">
        <strong>STANDARDIZE</strong>
        <span>Route × booking window</span>
    </div>
    <div class="flow-step">
        <strong>MEASURE</strong>
        <span>Price relatives + Jevons</span>
    </div>
    <div class="flow-step">
        <strong>EXPLAIN</strong>
        <span>Supply + demand + events + external factors</span>
    </div>
    <div class="flow-step">
        <strong>INTELLIGENCE</strong>
        <span>Index + derived signals</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="note">
<strong>Methodological principle:</strong>
not every parameter above enters the core airfare index.
The index is constructed primarily from standardized airfare observations,
while supply, demand, calendar, regional and external variables are used
to explain and contextualize movements. Derived metrics are analytical
indicators and are not automatically official CPI statistics.
</div>
""", unsafe_allow_html=True)
