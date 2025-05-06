# IEOR142A Final Project - NBA 2025 Playoffs Performance Dashboard 🏀

The NBA 2025 Playoffs Performance Dashboard features two interactive visualizations that explore player performance. 

The first visualization is a line chart that plots each selected player’s points in every 2024–25 playoff game. The horizontal axis displays game dates, and the vertical axis shows points scored. Each player’s scoring trajectory is rendered in a distinct color, allowing you to compare, for example, LeBron James against a high-variance shooter. A sidebar lets you choose which players to include and narrow the date range, and hovering over any marker reveals the exact game date, player name, and point total. Directly beneath these controls, season-to-date averages, maxima, and minima for points update dynamically based on your selections.

Additionally, the sidebar also includes a Playoff GIFs selector powered by the Giphy API. A dropdown menu lists all available players, and when you choose one and click Load GIF, it displays an GIF from the current playoffs. 

The second visualization is an interactive correlation heatmap showing Pearson coefficients among six core per-game metrics—points, assists, total rebounds, minutes played, turnovers, and plus/minus points. The heatmap shows relationships from strong negative to strong positive by recalculating for only the players and date range you’ve selected in the sidebar. Every cell is annotated with its correlation value to two decimal places, and you can hover to reveal the exact stat pair and r-value. 

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://app-starter-kit.streamlit.app/)

## GitHub Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/app-starter-kit?quickstart=1)

## Section Heading

This is filler text, please replace this with text for this section.

## Further Reading

This is filler text, please replace this with a explanatory text about further relevant resources for this repo
- Resource 1
- Resource 2
- Resource 3
