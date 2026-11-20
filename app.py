import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Air Scope India",
    page_icon="AQ",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    data = pd.read_csv("clean_air_quality.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    return data


df = load_data()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #FFF8FB;
}

.block-container {
    padding-top: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
    padding-bottom: 3rem;
}


/* HEADER */

.header-box {
    background: linear-gradient(
        135deg,
        #FCE4EC,
        #F8BBD0,
        #E8D5F5
    );

    padding: 30px 35px;
    border-radius: 24px;
    margin-bottom: 30px;

    border: 1px solid #F1C5D8;
}

.header-title {
    font-size: 42px;
    font-weight: 800;
    color: #6A1B4D;
    letter-spacing: 1px;
}

.header-subtitle {
    font-size: 16px;
    color: #7A5268;
    margin-top: 8px;
}


/* SECTION TITLES */

.section-title {
    font-size: 23px;
    font-weight: 700;
    color: #7B1E5A;
    margin-top: 28px;
    margin-bottom: 14px;
}


/* FILTERS */

div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #E7B6CC !important;
    border-radius: 10px !important;
}


/* KPI CARDS */

.metric-card {
    background-color: #FFFFFF;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #F0D6E2;
    box-shadow: 0px 5px 18px rgba(122, 43, 86, 0.07);
    min-height: 105px;
}

.metric-label {
    font-size: 13px;
    color: #8D687B;
    font-weight: 600;
}

.metric-value {
    font-size: 29px;
    font-weight: 800;
    color: #B52B73;
    margin-top: 5px;
}


/* INFORMATION BOX */

.info-card {
    background-color: #F7EEF8;
    border-left: 5px solid #C85A91;
    padding: 18px 22px;
    border-radius: 12px;
    color: #65445A;
    line-height: 1.6;
}


/* DIVIDER */

hr {
    border: none;
    border-top: 1px solid #EBCDDC;
}


/* FOOTER */

.footer {
    text-align: center;
    color: #9A7187;
    font-size: 13px;
    padding: 25px 0 10px 0;
}


/* HIDE STREAMLIT FOOTER */

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="header-box">
<div class="header-title">AIR SCOPE</div>
<div class="header-subtitle">Indian Air Quality | Exploring pollution patterns, AQI trends and seasonal variations</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FILTERS
# ============================================================

st.markdown(
    '<div class="section-title">Explore the Data</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    city_options = ["All Cities"] + sorted(
        df["City"].unique().tolist()
    )

    selected_city = st.selectbox(
        "City",
        city_options
    )


with col2:

    year_options = ["All Years"] + sorted(
        df["Year"].unique().tolist()
    )

    selected_year = st.selectbox(
        "Year",
        year_options
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()


if selected_city != "All Cities":

    filtered_df = filtered_df[
        filtered_df["City"] == selected_city
    ]


if selected_year != "All Years":

    filtered_df = filtered_df[
        filtered_df["Year"] == selected_year
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

average_aqi = filtered_df["AQI"].mean()

maximum_aqi = filtered_df["AQI"].max()

minimum_aqi = filtered_df["AQI"].min()

record_count = len(filtered_df)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">Air Quality Snapshot</div>',
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">AVERAGE AQI</div>
            <div class="metric-value">{average_aqi:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">HIGHEST AQI</div>
            <div class="metric-value">{maximum_aqi:.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">LOWEST AQI</div>
            <div class="metric-value">{minimum_aqi:.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">DATA RECORDS</div>
            <div class="metric-value">{record_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AQI TREND
# ============================================================

st.markdown(
    '<div class="section-title">AQI Trend</div>',
    unsafe_allow_html=True
)

trend = (
    filtered_df
    .groupby("Year", as_index=False)["AQI"]
    .mean()
)


fig_trend = px.line(
    trend,
    x="Year",
    y="AQI",
    markers=True
)


fig_trend.update_traces(
    line=dict(
        color="#C2185B",
        width=3
    ),
    marker=dict(
        color="#8E5AA8",
        size=9
    )
)


fig_trend.update_layout(
    height=400,
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(
        color="#65445A"
    ),
    xaxis=dict(
        title="Year",
        showgrid=False
    ),
    yaxis=dict(
        title="Average AQI",
        showgrid=True,
        gridcolor="#F3E3EC"
    ),
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)


st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# ============================================================
# AQI CATEGORY AND SEASONAL ANALYSIS
# ============================================================

left_col, right_col = st.columns(2)


# ============================================================
# AQI CATEGORY
# ============================================================

with left_col:

    st.markdown(
        '<div class="section-title">AQI Categories</div>',
        unsafe_allow_html=True
    )

    category_counts = (
        filtered_df["AQI_Bucket"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "Category",
        "Count"
    ]

    fig_category = px.bar(
        category_counts,
        x="Category",
        y="Count"
    )

    fig_category.update_traces(
        marker_color="#D85C91"
    )

    fig_category.update_layout(
        height=400,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(
            color="#65445A"
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F3E3EC"
        ),
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ============================================================
# SEASONAL AQI
# ============================================================

with right_col:

    st.markdown(
        '<div class="section-title">Seasonal AQI</div>',
        unsafe_allow_html=True
    )

    season_order = [
        "Winter",
        "Summer",
        "Monsoon",
        "Post-Monsoon"
    ]

    seasonal_aqi = (
        filtered_df
        .groupby("Season", as_index=False)["AQI"]
        .mean()
    )

    seasonal_aqi["Season"] = pd.Categorical(
        seasonal_aqi["Season"],
        categories=season_order,
        ordered=True
    )

    seasonal_aqi = seasonal_aqi.sort_values(
        "Season"
    )

    fig_season = px.bar(
        seasonal_aqi,
        x="Season",
        y="AQI"
    )

    fig_season.update_traces(
        marker_color="#9B6BB3"
    )

    fig_season.update_layout(
        height=400,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(
            color="#65445A"
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F3E3EC"
        ),
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_season,
        use_container_width=True
    )


# ============================================================
# CITY-WISE AQI
# ============================================================

st.markdown(
    '<div class="section-title">City-wise Air Quality</div>',
    unsafe_allow_html=True
)

city_aqi = (
    filtered_df
    .groupby("City", as_index=False)["AQI"]
    .mean()
    .sort_values(
        "AQI",
        ascending=False
    )
)


fig_city = px.bar(
    city_aqi,
    x="City",
    y="AQI"
)


fig_city.update_traces(
    marker_color="#C94F86"
)


fig_city.update_layout(
    height=500,
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(
        color="#65445A"
    ),
    xaxis=dict(
        showgrid=False,
        tickangle=-45
    ),
    yaxis=dict(
        title="Average AQI",
        showgrid=True,
        gridcolor="#F3E3EC"
    ),
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=80
    )
)


st.plotly_chart(
    fig_city,
    use_container_width=True
)


# ============================================================
# POLLUTANT ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Pollutant Concentration</div>',
    unsafe_allow_html=True
)


pollutants = [
    "PM2.5",
    "PM10",
    "NO",
    "NO2",
    "NOx",
    "NH3",
    "CO",
    "SO2",
    "O3",
    "Benzene",
    "Toluene"
]


pollutant_avg = (
    filtered_df[pollutants]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)


pollutant_avg.columns = [
    "Pollutant",
    "Average"
]


fig_pollutant = px.bar(
    pollutant_avg,
    x="Pollutant",
    y="Average"
)


fig_pollutant.update_traces(
    marker_color="#D8A1C4"
)


fig_pollutant.update_layout(
    height=450,
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(
        color="#65445A"
    ),
    xaxis=dict(
        showgrid=False
    ),
    yaxis=dict(
        title="Average Concentration",
        showgrid=True,
        gridcolor="#F3E3EC"
    ),
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)


st.plotly_chart(
    fig_pollutant,
    use_container_width=True
)


# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.markdown(
    '<div class="section-title">Pollutant and AQI Relationships</div>',
    unsafe_allow_html=True
)


corr_columns = pollutants + ["AQI"]


corr_matrix = (
    filtered_df[corr_columns]
    .corr()
)


fig_corr = px.imshow(
    corr_matrix,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale=[
        "#FFF8FB",
        "#F8D7E5",
        "#E8B6D0",
        "#C85A91",
        "#7B1E5A"
    ]
)


fig_corr.update_layout(
    height=600,
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font=dict(
        color="#65445A"
    ),
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)


st.plotly_chart(
    fig_corr,
    use_container_width=True
)


# ============================================================
# ABOUT DASHBOARD
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">About the Dashboard</div>',
    unsafe_allow_html=True
)


st.markdown("""
<div class="info-card">

<b>Air Scope - India</b> analyzes air quality data collected
from cities across India. The dashboard explores AQI trends,
pollution levels, seasonal patterns and relationships between
different air pollutants.

<br><br>

The dataset was cleaned and analyzed using Python and Pandas.
Plotly was used for visualization and Streamlit was used to
build the interactive dashboard.

</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
Air Scope - India | Data Analysis and Visualization Practical
</div>
""", unsafe_allow_html=True)