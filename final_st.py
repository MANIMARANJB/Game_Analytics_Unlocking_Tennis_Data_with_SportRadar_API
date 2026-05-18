import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Mani@123',
        port=3306,
        database='demo_1'
    )

@st.cache_data
def fetch_table(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---------------- FETCH DATA ----------------
categories_df = fetch_table("SELECT * FROM Categories_Table")
competitions_df = fetch_table("SELECT * FROM Competitions_Table")
complexes_df = fetch_table("SELECT * FROM Complexes_Table")
venues_df = fetch_table("SELECT * FROM Venues_Table")
competitors_df = fetch_table("SELECT * FROM Competitors_Table")
rankings_df = fetch_table("SELECT * FROM Competitor_Rankings_Table")

# ---------------- STREAMLIT UI ----------------
#st.set_page_config(page_title="Tennis Dashboard", layout="wide")

st.sidebar.title("🎾 TENNIS INSIGHTS MENU")
menu = st.sidebar.radio(
    "Navigate",
    ("Home",
     "Categories Analysis",
     "Competitions Analysis",
     "Competitors & Rankings",
     "Complexes & Venues")
)

st.title("🏆 **TENNIS INSIGHTS DASHBOARD**")

# ---------------- HOME PAGE ----------------
if menu == "Home":
    st.subheader("Welcome to the Tennis Analysis Dashboard")
    st.write("Use this dashboard to analyze categories, competitions, competitors and venues worldwide.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Categories", len(categories_df))
    col2.metric("Competitions", len(competitions_df))
    col3.metric("Competitors", len(competitors_df))
    col4.metric("Venues", len(venues_df))

    st.write("### Sample Data Preview")
    st.dataframe(categories_df)

# ---------------- CATEGORIES ----------------
elif menu == "Categories Analysis":
    st.header("📂 Categories Overview")

    st.dataframe(categories_df)

    st.subheader("Category Count Visualization")
    fig, ax = plt.subplots()
    ax.bar(categories_df["category_name"], categories_df["category_id"].count())
    st.pyplot(fig)

# ---------------- COMPETITIONS ----------------
elif menu == "Competitions Analysis":
    st.header("🏅 Competitions Overview")

    st.dataframe(competitions_df)

    st.subheader("Filter by Category")
    category_filter = st.selectbox("Select Category", categories_df["category_name"].unique())
    selected_category_id = categories_df[categories_df["category_name"] == category_filter]["category_id"].iloc[0]

    filtered_comp = competitions_df[competitions_df["category_id"] == selected_category_id]
    st.dataframe(filtered_comp)

    st.write(f"Total Competitions: **{len(filtered_comp)}**")

# ---------------- COMPETITORS & RANKINGS ----------------
elif menu == "Competitors & Rankings":
    st.header("⭐ Competitors & Rankings")

    rankings_joined = rankings_df.merge(competitors_df, on="competitor_id", how="left")

    st.dataframe(rankings_joined)

    st.subheader("Ranking by Points")
    top10 = rankings_joined.sort_values(by="points", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.bar(top10["name"], top10["points"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.write("Best Competitor:", top10.iloc[0]["name"])

# ---------------- VENUES & COMPLEXES ----------------
elif menu == "Complexes & Venues":
    st.header("🏟 Venues & Complexes Overview")

    venues_joined = venues_df.merge(complexes_df, on="complex_id", how="left")
    st.dataframe(venues_joined)

    st.subheader("Filter by Country")
    country_select = st.selectbox("Select Country", sorted(venues_df["country_name"].unique()))
    filtered_venues = venues_joined[venues_joined["country_name"] == country_select]
    st.dataframe(filtered_venues)

    st.metric("Venues in Country", len(filtered_venues))

    fig, ax = plt.subplots()
    ax.bar(filtered_venues["venue_name"], filtered_venues["city_name"])
    plt.xticks(rotation=45)
    st.pyplot(fig)