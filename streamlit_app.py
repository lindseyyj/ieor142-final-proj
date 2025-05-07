import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="NBA Points Over Time", layout="wide")
st.title("🏀 NBA 2025 Playoffs Performance Dashboard")
st.markdown("""
The NBA 2025 Playoffs Performance Dashboard features two interactive visualizations that explore player performance.

The first visualization is a line chart that plots each selected player’s points in every 2024–25 playoff game. The horizontal axis displays game dates, and the vertical axis shows points scored. Each player’s scoring trajectory is rendered in a distinct color, allowing you to compare, for example, LeBron James against a high-variance shooter. A sidebar lets you choose which players to include and narrow the date range, and hovering over any marker reveals the exact game date, player name, and point total. Directly beneath these controls, season-to-date averages, maxima, and minima for points update dynamically based on your selections.

Additionally, the sidebar also includes a Playoff GIFs selector powered by the Giphy API. A dropdown menu lists all available players, and when you choose one and click Load GIF, it displays an GIF from the current playoffs.

The second visualization is an interactive correlation heatmap showing coefficients among six core per-game metrics: assists, total rebounds, minutes played, turnovers, and plus/minus points. The heatmap shows relationships from strong negative to strong positive by recalculating for only the players and date range you’ve selected in the sidebar. Every cell is annotated with its correlation value to two decimal places, and you can hover to reveal the exact stat pair and r-value.
""")
st.subheader("🔍 Per-Game Points Over Time")

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

#GIFS 
def fetch_gif_url(player_name: str) -> str | None:
    params = {
        "api_key": st.secrets["GIPHY_API_KEY"],
        "q": f"{player_name} playoffs nba",
        "limit": 1,
        "rating": "pg"
    }
    resp = requests.get("https://api.giphy.com/v1/gifs/search", params=params)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return data[0]["images"]["downsized"]["url"] if data else None

st.sidebar.header("🏆 Playoff GIFs")
gif_player = st.sidebar.selectbox("Choose a player for GIF", options=players, index=players.index("LeBron James"))
if st.sidebar.button("Load GIF"):
    gif_url = fetch_gif_url(gif_player)
    if gif_url:
        gif_bytes = requests.get(gif_url).content
        st.sidebar.image(gif_bytes, caption=gif_player, width=300)
        st.image(
            gif_bytes,
            caption=gif_player,
            use_container_width=True
        )
    else:
        st.sidebar.write("No GIF found.")
        
if st.sidebar.checkbox("Display Raw Filtered Data"):
    st.subheader("Raw Filtered Data")
    st.dataframe(df_filt[["gameDate", "Player", "points", "Team", "Opponent"]])

# Correlation Heatmap 
st.subheader("🔍 Correlation Matrix of Key Player Stats")

features = [
    "points",
    "assists",
    "reboundsTotal",
    "numMinutes",
    "turnovers",
    "plusMinusPoints",
]

corr = df_filt[features].corr()

# Build Plotly Heatmap
fig_corr = px.imshow(
    corr,
    x=features,
    y=features,
    text_auto=".2f", 
    zmin=-1,
    zmax=1,
    labels={"color": "Correlation (r)"},
    title="Correlation Matrix of Key Player Stats"
)
fig_corr.update_layout(
    width=600,
    height=600,
    margin=dict(l=40, r=40, t=50, b=40)
)

st.plotly_chart(fig_corr, use_container_width=True)
