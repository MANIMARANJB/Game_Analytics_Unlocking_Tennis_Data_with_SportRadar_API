import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sports Competition Analytics",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL BUSINESS DASHBOARD THEME
# ============================================================

st.markdown("""
<style>

/* ============================================================
   MAIN APP
   ============================================================ */

.stApp {
    background-color: #f5f7fb;
    color: #172033;
}

.main {
    background-color: #f5f7fb;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] label {
    color: #334155 !important;
    font-weight: 600;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #172033 !important;
}


/* ============================================================
   SELECT BOXES
   ============================================================ */

[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #172033 !important;
    border-radius: 8px;
}

[data-baseweb="select"] span {
    color: #334155 !important;
}

[data-baseweb="select"] input {
    color: #172033 !important;
}


/* ============================================================
   MULTISELECT TAGS
   ============================================================ */

[data-baseweb="tag"] {
    background-color: #2563eb !important;
}

[data-baseweb="tag"] span {
    color: white !important;
}


/* ============================================================
   SLIDERS
   ============================================================ */

[data-testid="stSlider"] {
    color: #2563eb !important;
}

[data-testid="stSlider"] label {
    color: #334155 !important;
}


/* ============================================================
   KPI CARDS
   ============================================================ */

[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #172033 !important;
    font-weight: 750;
}

[data-testid="stMetricDelta"] {
    color: #2563eb !important;
}


/* ============================================================
   HEADINGS
   ============================================================ */

h1 {
    color: #172033 !important;
    font-weight: 800;
}

h2 {
    color: #172033 !important;
    font-weight: 750;
}

h3 {
    color: #334155 !important;
    font-weight: 700;
}


/* ============================================================
   NORMAL TEXT
   ============================================================ */

p {
    color: #475569;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border-color: #e2e8f0 !important;
}


/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
}

[data-testid="stExpander"] summary {
    color: #172033 !important;
    font-weight: 600;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}


/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */

.stDownloadButton > button {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}


/* ============================================================
   INSIGHT BOXES
   ============================================================ */

.insight {
    background-color: #ffffff;
    border-left: 4px solid #2563eb;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    color: #334155;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
}


/* ============================================================
   CAPTION
   ============================================================ */

.stCaption {
    color: #64748b !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# PROFESSIONAL COLORS
# ============================================================

PRIMARY = "#2563EB"
SECONDARY = "#3B82F6"
LIGHT_BLUE = "#60A5FA"
TEAL = "#0F766E"
GREEN = "#16A34A"
ORANGE = "#EA580C"
PURPLE = "#7C3AED"
RED = "#DC2626"

CHART_COLORS = [
    PRIMARY,
    SECONDARY,
    LIGHT_BLUE,
    TEAL,
    GREEN,
    ORANGE,
    PURPLE,
    RED
]


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return pymysql.connect(
        host="localhost",
        user="root",
        password="Mani@123",
        port=3306,
        database="demo_1"
    )


@st.cache_data
def fetch_table(query):

    conn = get_connection()

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    return df


# ============================================================
# FETCH DATA
# ============================================================

categories_df = fetch_table(
    "SELECT * FROM Categories_Table"
)

competitions_df = fetch_table(
    "SELECT * FROM Competitions_Table"
)

complexes_df = fetch_table(
    "SELECT * FROM Complexes_Table"
)

venues_df = fetch_table(
    "SELECT * FROM Venues_Table"
)

competitors_df = fetch_table(
    "SELECT * FROM Competitors_Table"
)

rankings_df = fetch_table(
    "SELECT * FROM Competitor_Rankings_Table"
)


# ============================================================
# DATA PREPARATION
# ============================================================

ranking_data = rankings_df.merge(
    competitors_df,
    on="competitor_id",
    how="left"
)


competition_data = competitions_df.merge(
    categories_df,
    on="category_id",
    how="left"
)


venue_data = venues_df.merge(
    complexes_df,
    on="complex_id",
    how="left"
)


# ============================================================
# NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "rank_position",
    "movement",
    "points",
    "competitions_played"
]

for column in numeric_columns:

    if column in ranking_data.columns:

        ranking_data[column] = pd.to_numeric(
            ranking_data[column],
            errors="coerce"
        ).fillna(0)


# ============================================================
# PLOTLY PROFESSIONAL LIGHT STYLE
# ============================================================

def style_chart(fig, height=450):

    fig.update_layout(

        height=height,

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(
            color="#334155",
            family="Arial"
        ),

        title=dict(
            font=dict(
                color="#172033",
                size=18
            )
        ),

        legend=dict(
            font=dict(
                color="#475569"
            ),
            bgcolor="rgba(255,255,255,0)"
        ),

        margin=dict(
            l=55,
            r=30,
            t=70,
            b=55
        )
    )


    fig.update_xaxes(

        color="#64748b",

        gridcolor="#e2e8f0",

        linecolor="#cbd5e1",

        zerolinecolor="#cbd5e1"
    )


    fig.update_yaxes(

        color="#64748b",

        gridcolor="#e2e8f0",

        linecolor="#cbd5e1",

        zerolinecolor="#cbd5e1"
    )


    return fig


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("ᯓ★ Dashboard Filters")

st.sidebar.markdown("---")


# ============================================================
# COUNTRY FILTER
# ============================================================

countries = sorted(
    competitors_df["country"]
    .dropna()
    .unique()
    .tolist()
)

selected_countries = st.sidebar.multiselect(
    "🌍 Country",
    countries
)


# ============================================================
# GENDER FILTER
# ============================================================

if "gender" in competitions_df.columns:

    genders = sorted(
        competitions_df["gender"]
        .dropna()
        .unique()
        .tolist()
    )

else:

    genders = []


selected_genders = st.sidebar.multiselect(
    "⚧ Gender",
    genders
)


# ============================================================
# COMPETITION TYPE FILTER
# ============================================================

types = sorted(
    competitions_df["type"]
    .dropna()
    .unique()
    .tolist()
)

selected_types = st.sidebar.multiselect(
    "🏆 Competition Type",
    types
)


# ============================================================
# CATEGORY FILTER
# ============================================================

category_names = sorted(
    categories_df["category_name"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "📂 Category",
    category_names
)


# ============================================================
# COMPETITOR FILTER
# ============================================================

competitor_names = sorted(
    competitors_df["name"]
    .dropna()
    .unique()
    .tolist()
)

selected_competitors = st.sidebar.multiselect(
    "👤 Competitor",
    competitor_names
)


# ============================================================
# RANKING FILTERS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Ranking Filters")


# ============================================================
# RANKING POSITION SLIDER
# ============================================================

min_rank = int(
    ranking_data["rank_position"].min()
)

max_rank = int(
    ranking_data["rank_position"].max()
)


if min_rank < max_rank:

    rank_range = st.sidebar.slider(
        "Ranking Position",
        min_rank,
        max_rank,
        (min_rank, max_rank)
    )

else:

    rank_range = (
        min_rank,
        max_rank
    )


# ============================================================
# POINTS SLIDER
# ============================================================

min_points = int(
    ranking_data["points"].min()
)

max_points = int(
    ranking_data["points"].max()
)


if min_points < max_points:

    points_range = st.sidebar.slider(
        "Ranking Points",
        min_points,
        max_points,
        (min_points, max_points)
    )

else:

    points_range = (
        min_points,
        max_points
    )


# ============================================================
# COMPETITIONS PLAYED SLIDER
# ============================================================

min_played = int(
    ranking_data["competitions_played"].min()
)

max_played = int(
    ranking_data["competitions_played"].max()
)


if min_played < max_played:

    played_range = st.sidebar.slider(
        "Competitions Played",
        min_played,
        max_played,
        (min_played, max_played)
    )

else:

    played_range = (
        min_played,
        max_played
    )


# ============================================================
# APPLY RANKING FILTERS
# ============================================================

filtered_rankings = ranking_data.copy()


if selected_countries:

    filtered_rankings = filtered_rankings[
        filtered_rankings["country"].isin(
            selected_countries
        )
    ]


if selected_competitors:

    filtered_rankings = filtered_rankings[
        filtered_rankings["name"].isin(
            selected_competitors
        )
    ]


filtered_rankings = filtered_rankings[
    (
        filtered_rankings["rank_position"]
        >= rank_range[0]
    )
    &
    (
        filtered_rankings["rank_position"]
        <= rank_range[1]
    )
]


filtered_rankings = filtered_rankings[
    (
        filtered_rankings["points"]
        >= points_range[0]
    )
    &
    (
        filtered_rankings["points"]
        <= points_range[1]
    )
]


filtered_rankings = filtered_rankings[
    (
        filtered_rankings["competitions_played"]
        >= played_range[0]
    )
    &
    (
        filtered_rankings["competitions_played"]
        <= played_range[1]
    )
]


# ============================================================
# APPLY COMPETITION FILTERS
# ============================================================

filtered_competitions = competition_data.copy()


if selected_types:

    filtered_competitions = filtered_competitions[
        filtered_competitions["type"].isin(
            selected_types
        )
    ]


if selected_genders:

    filtered_competitions = filtered_competitions[
        filtered_competitions["gender"].isin(
            selected_genders
        )
    ]


if selected_categories:

    filtered_competitions = filtered_competitions[
        filtered_competitions["category_name"].isin(
            selected_categories
        )
    ]


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "🏆 Sports Competition Analytics"
)

st.markdown(
    "### Interactive Competitor • Ranking • Competition • Venue Dashboard"
)

st.markdown("---")


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_competitors = (
    filtered_rankings["competitor_id"]
    .nunique()
)

total_competitions = len(
    filtered_competitions
)

total_points = int(
    filtered_rankings["points"].sum()
)

total_venues = (
    venue_data["venue_id"].nunique()
)

total_categories = (
    filtered_competitions["category_id"]
    .nunique()
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)


k1.metric(
    "👤 Competitors",
    f"{total_competitors:,}"
)


k2.metric(
    "🏆 Competitions",
    f"{total_competitions:,}"
)


k3.metric(
    "⭐ Total Points",
    f"{total_points:,}"
)


k4.metric(
    "🏟️ Venues",
    f"{total_venues:,}"
)


k5.metric(
    "📂 Categories",
    f"{total_categories:,}"
)


st.markdown("---")


# ============================================================
# COMPETITOR PERFORMANCE
# ============================================================

st.subheader(
    "🥇 Competitor Performance"
)


col1, col2 = st.columns(2)


# ============================================================
# TOP 10 COMPETITORS BY POINTS
# ============================================================

top_points = (

    filtered_rankings

    .groupby(
        "name",
        as_index=False
    )["points"]

    .sum()

    .sort_values(
        "points",
        ascending=False
    )

    .head(10)
)


fig = px.bar(

    top_points,

    x="points",

    y="name",

    orientation="h",

    title="Top 10 Competitors by Ranking Points",

    text="points"
)


fig.update_traces(
    marker_color=PRIMARY
)


fig = style_chart(
    fig,
    450
)


fig.update_layout(
    yaxis=dict(
        autorange="reversed"
    )
)


col1.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# TOP 10 COMPETITORS BY COMPETITIONS PLAYED
# ============================================================

top_played = (

    filtered_rankings

    .groupby(
        "name",
        as_index=False
    )["competitions_played"]

    .sum()

    .sort_values(
        "competitions_played",
        ascending=False
    )

    .head(10)
)


fig = px.bar(

    top_played,

    x="name",

    y="competitions_played",

    title="Top 10 Competitors by Competitions Played",

    text="competitions_played"
)


fig.update_traces(
    marker_color=SECONDARY
)


fig = style_chart(
    fig,
    450
)


col2.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# RANKING ANALYSIS
# ============================================================

st.subheader(
    "📈 Ranking Analysis"
)


col1, col2 = st.columns(2)


# ============================================================
# TOP 10 RANKED COMPETITORS
# ============================================================

top_ranked = (

    filtered_rankings[
        [
            "name",
            "rank_position",
            "points",
            "country"
        ]
    ]

    .drop_duplicates(
        "name"
    )

    .sort_values(
        "rank_position"
    )

    .head(10)
)


fig = px.bar(

    top_ranked,

    x="rank_position",

    y="name",

    orientation="h",

    color="points",

    text="rank_position",

    hover_data=[
        "country",
        "points"
    ],

    title="🏆 Top 10 Ranked Competitors"
)


fig = style_chart(
    fig,
    450
)


fig.update_layout(
    yaxis=dict(
        autorange="reversed",
        title="Competitor"
    ),
    xaxis=dict(
        title="Ranking Position"
    )
)


col1.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# POINTS VS COMPETITIONS PLAYED
# ============================================================

fig = px.scatter(

    filtered_rankings,

    x="competitions_played",

    y="points",

    size="points",

    color="country",

    hover_name="name",

    hover_data=[
        "rank_position",
        "competitions_played"
    ],

    title="⭐ Ranking Points vs Competitions Played"
)


fig = style_chart(
    fig,
    450
)


fig.update_layout(
    xaxis_title="Competitions Played",
    yaxis_title="Ranking Points"
)


col2.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# COUNTRY ANALYSIS
# ============================================================

st.subheader(
    "🌍 Country Analysis"
)


col1, col2 = st.columns(2)


# ============================================================
# COUNTRY COMPETITOR COUNT
# ============================================================

country_count = (

    filtered_rankings

    .groupby(
        "country"
    )

    .size()

    .reset_index(
        name="competitors"
    )

    .sort_values(
        "competitors",
        ascending=False
    )
)


fig = px.pie(

    country_count.head(10),

    names="country",

    values="competitors",

    hole=0.5,

    title="Top Countries by Competitor Count"
)


fig.update_traces(
    marker=dict(
        colors=CHART_COLORS
    )
)


fig = style_chart(
    fig,
    450
)


col1.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# COUNTRY RANKING POINTS
# ============================================================

country_points = (

    filtered_rankings

    .groupby(
        "country",
        as_index=False
    )["points"]

    .sum()

    .sort_values(
        "points",
        ascending=False
    )

    .head(10)
)


fig = px.bar(

    country_points,

    x="country",

    y="points",

    title="Top Countries by Ranking Points",

    text="points"
)


fig.update_traces(
    marker_color=TEAL
)


fig = style_chart(
    fig,
    450
)


col2.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# COMPETITION ANALYSIS
# ============================================================

st.subheader(
    "🏆 Competition Analytics"
)


col1, col2 = st.columns(2)


# ============================================================
# COMPETITION TYPE DONUT
# ============================================================

type_count = (

    filtered_competitions

    .groupby(
        "type"
    )

    .size()

    .reset_index(
        name="competitions"
    )
)


if not type_count.empty:

    fig = px.pie(

        type_count,

        names="type",

        values="competitions",

        hole=0.45,

        title="Competition Type Distribution"
    )


    fig.update_traces(
        marker=dict(
            colors=CHART_COLORS
        )
    )


    fig = style_chart(
        fig,
        450
    )


    col1.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# GENDER DISTRIBUTION
# ============================================================

if not filtered_competitions.empty:

    gender_count = (

        filtered_competitions

        .groupby(
            "gender"
        )

        .size()

        .reset_index(
            name="competitions"
        )
    )


    fig = px.bar(

        gender_count,

        x="gender",

        y="competitions",

        title="Competitions by Gender",

        text="competitions"
    )


    fig.update_traces(
        marker_color=PURPLE
    )


    fig = style_chart(
        fig,
        450
    )


    col2.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

st.subheader(
    "📂 Category Analytics"
)


category_count = (

    filtered_competitions

    .groupby(
        "category_name"
    )

    .size()

    .reset_index(
        name="competitions"
    )

    .sort_values(
        "competitions",
        ascending=False
    )
)


if not category_count.empty:

    fig = px.bar(

        category_count,

        x="category_name",

        y="competitions",

        title="Competitions by Category",

        text="competitions"
    )


    fig.update_traces(
        marker_color=PRIMARY
    )


    fig = style_chart(
        fig,
        450
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CATEGORY × COMPETITION TYPE
# ============================================================

category_type = (

    filtered_competitions

    .groupby(
        [
            "category_name",
            "type"
        ]
    )

    .size()

    .reset_index(
        name="count"
    )
)


if not category_type.empty:

    fig = px.bar(

        category_type,

        x="category_name",

        y="count",

        color="type",

        title="Competition Type by Category",

        barmode="stack",

        color_discrete_sequence=CHART_COLORS
    )


    fig = style_chart(
        fig,
        500
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# VENUE ANALYSIS
# ============================================================

st.subheader(
    "🏟️ Venue & Location Analytics"
)


col1, col2 = st.columns(2)


# ============================================================
# TOP CITIES
# ============================================================

city_count = (

    venue_data

    .groupby(
        "city_name"
    )

    .size()

    .reset_index(
        name="venues"
    )

    .sort_values(
        "venues",
        ascending=False
    )

    .head(10)
)


fig = px.bar(

    city_count,

    x="venues",

    y="city_name",

    orientation="h",

    title="Top 10 Cities by Number of Venues",

    text="venues"
)


fig.update_traces(
    marker_color=ORANGE
)


fig = style_chart(
    fig,
    450
)


fig.update_layout(
    yaxis=dict(
        autorange="reversed"
    )
)


col1.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# VENUE COUNTRY DONUT
# ============================================================

country_venues = (

    venue_data

    .groupby(
        "country_name"
    )

    .size()

    .reset_index(
        name="venues"
    )

    .sort_values(
        "venues",
        ascending=False
    )

    .head(10)
)


fig = px.pie(

    country_venues,

    names="country_name",

    values="venues",

    hole=0.45,

    title="Venue Distribution by Country"
)


fig.update_traces(
    marker=dict(
        colors=CHART_COLORS
    )
)


fig = style_chart(
    fig,
    450
)


col2.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# COUNTRY PERFORMANCE HEATMAP
# ============================================================

st.subheader(
    "🔥 Country Performance Heatmap"
)


heatmap_data = (

    filtered_rankings

    .groupby(
        "country"
    )

    .agg(

        competitors=(
            "competitor_id",
            "nunique"
        ),

        points=(
            "points",
            "sum"
        ),

        competitions=(
            "competitions_played",
            "sum"
        )

    )

    .reset_index()
)


if not heatmap_data.empty:

    heatmap_data = (

        heatmap_data

        .sort_values(
            "points",
            ascending=False
        )

        .head(15)
    )


    heatmap_values = heatmap_data[
        [
            "competitors",
            "points",
            "competitions"
        ]
    ].T


    fig = px.imshow(

        heatmap_values,

        labels=dict(
            x="Country",
            y="Metric",
            color="Value"
        ),

        x=heatmap_data["country"],

        title="Country Performance Heatmap",

        aspect="auto",

        color_continuous_scale=[
            "#eff6ff",
            "#bfdbfe",
            "#60a5fa",
            "#2563eb",
            "#1e40af"
        ]
    )


    fig = style_chart(
        fig,
        450
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# RANKING MOVEMENT
# ============================================================

st.subheader(
    "↕️ Ranking Movement"
)


if "movement" in filtered_rankings.columns:

    movement_data = (

        filtered_rankings

        .groupby(
            "name",
            as_index=False
        )["movement"]

        .mean()

        .sort_values(
            "movement"
        )

        .head(15)
    )


    if not movement_data.empty:

        fig = px.bar(

            movement_data,

            x="name",

            y="movement",

            title="Competitor Ranking Movement",

            text_auto=True
        )


        fig.update_traces(
            marker_color=LIGHT_BLUE
        )


        fig = style_chart(
            fig,
            450
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# KEY INSIGHTS
# ============================================================

st.subheader(
    "💡 Key Insights"
)


if not filtered_rankings.empty:

    best_competitor = (

        filtered_rankings

        .sort_values(
            "points",
            ascending=False
        )

        .iloc[0]
    )


    top_country = (

        filtered_rankings[
            "country"
        ]

        .value_counts()

        .idxmax()
    )


    highest_points = (

        filtered_rankings[
            "points"
        ].max()
    )


    avg_points = (

        filtered_rankings[
            "points"
        ].mean()
    )


    st.markdown(

        f"""
        <div class="insight">

        🥇 <b>Top Performer:</b>
        {best_competitor['name']} has the highest ranking
        points with <b>{highest_points:,.0f}</b> points.

        </div>

        <div class="insight">

        🌍 <b>Leading Country:</b>
        {top_country} has the largest number of competitors
        in the current filtered dataset.

        </div>

        <div class="insight">

        📊 <b>Average Points:</b>
        The average ranking points per record is
        <b>{avg_points:,.1f}</b>.

        </div>

        <div class="insight">

        👥 <b>Active Competitors:</b>
        There are <b>{total_competitors:,}</b>
        competitors matching the current filters.

        </div>
        """,

        unsafe_allow_html=True
    )


else:

    st.warning(
        "No data matches the selected filters. "
        "Please change the sidebar filters."
    )


# ============================================================
# FILTERED RANKING DATA
# ============================================================

st.markdown("---")


with st.expander(
    "📋 View Filtered Ranking Data"
):

    st.dataframe(
        filtered_rankings,
        use_container_width=True,
        height=400
    )


    csv = (

        filtered_rankings

        .to_csv(
            index=False
        )

        .encode("utf-8")
    )


    st.download_button(

        label="📥 Download Filtered Ranking Data",

        data=csv,

        file_name="filtered_ranking_data.csv",

        mime="text/csv"
    )


# ============================================================
# FILTERED COMPETITION DATA
# ============================================================

with st.expander(
    "📋 View Competition Data"
):

    st.dataframe(
        filtered_competitions,
        use_container_width=True,
        height=350
    )


    competition_csv = (

        filtered_competitions

        .to_csv(
            index=False
        )

        .encode("utf-8")
    )


    st.download_button(

        label="📥 Download Competition Data",

        data=competition_csv,

        file_name="filtered_competition_data.csv",

        mime="text/csv"
    )


# ============================================================
# VENUE DATA
# ============================================================

with st.expander(
    "📋 View Venue Data"
):

    st.dataframe(
        venue_data,
        use_container_width=True,
        height=350
    )


    venue_csv = (

        venue_data

        .to_csv(
            index=False
        )

        .encode("utf-8")
    )


    st.download_button(

        label="📥 Download Venue Data",

        data=venue_csv,

        file_name="venue_data.csv",

        mime="text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🏆 Sports Competition Analytics | "
    "MySQL • Python • Streamlit • Plotly"
)