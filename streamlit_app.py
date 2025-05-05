import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NBA Points Over Time", layout="wide")
st.title("🏀 NBA 2025 Playoffs: Points by Game Over Time")

@st.cache_data
def load_data():
    df = pd.read_csv("final_df.csv", parse_dates=["gameDate"])
    df["Player"] = df["firstName"] + " " + df["lastName"]
    df = df.rename(columns={
        "playerteamName": "Team",
        "opponentteamName": "Opponent"
    })
    df = df.sort_values("gameDate")
    return df

df = load_data()

players = sorted(df["Player"].unique())
default = ["LeBron James"] + [p for p in players if p != "LeBron James"][:2]
selected = st.sidebar.multiselect("Select players", players, default=default)

min_date, max_date = df["gameDate"].dt.date.min(), df["gameDate"].dt.date.max()
date_range = st.sidebar.date_input("Date range", [min_date, max_date])

mask = (
    df["Player"].isin(selected)
    & (df["gameDate"].dt.date >= date_range[0])
    & (df["gameDate"].dt.date <= date_range[1])
)
df_filt = df.loc[mask].sort_values("gameDate")

fig = px.line(
    df_filt,
    x="gameDate",
    y="points",
    color="Player",
    markers=True,
    title="Per-Game Points Over Time",
    labels={"gameDate": "Game Date", "points": "Points"}
)
fig.update_layout(legend_title_text="Player")
st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("### Season‐to‐Date Averages")
stats = (
    df_filt
    .groupby("Player")["points"]
    .agg(Avg="mean", Max="max", Min="min")
    .round(1)
    .rename_axis("")
)
st.sidebar.dataframe(stats)

if st.sidebar.checkbox("Show raw data"):
    st.subheader("Filtered Data")
    st.dataframe(df_filt[["gameDate", "Player", "points", "Team", "Opponent"]])
