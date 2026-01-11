st.markdown("""
<style>
body {
    background-color: #f7f8fa;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.big {
    font-size: 28px;
    font-weight: 700;
}

.small {
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# CONFIG UI
# =========================
st.set_page_config(
    page_title="IQ FootLab",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .metric-box { text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("⚽ IQ FootLab — Analyse Match")

# =========================
# CHARGEMENT MATCHS
# =========================
MATCHES_DIR = "data/matches"
matches = sorted(os.listdir(MATCHES_DIR), reverse=True)

selected_match = st.sidebar.selectbox(
    "📅 Sélection du match",
    matches
)

match_path = os.path.join(MATCHES_DIR, selected_match)

with open(os.path.join(match_path, "match_stats.json")) as f:
    match_stats = json.load(f)

with open(os.path.join(match_path, "players_positions.json")) as f:
    positions = json.load(f)

teams = match_stats["teams"]
players_vs_team = match_stats["players_vs_team"]
reading = match_stats["match_reading"]

df_players = pd.DataFrame.from_dict(players_vs_team, orient="index")
df_players["distance_vs_team"] = df_players["distance_vs_team"].astype(float)

# =========================
# NAVIGATION
# =========================
page = st.sidebar.radio(
    "Navigation",
    ["📌 Vue Match", "🔵 Équipes", "👥 Joueurs", "🔥 Heatmap"]
)

# =====================================================
# PAGE 1 — MATCH
# =====================================================
if page == "📌 Vue Match":
    st.subheader("📌 Synthèse du match")

    col1, col2, col3 = st.columns(3)
    col1.metric("Équipe dominante", reading["dominant_mobility_team"])
    col2.metric("Écart d’intensité", reading["mobility_gap"])
    col3.metric("Joueurs analysés", 22)

    st.divider()

    st.subheader("🧠 Lecture coach automatique")

    if reading["mobility_gap"] > 5:
        st.success(f"{reading['dominant_mobility_team']} a dominé physiquement le match.")
    else:
        st.info("Match globalement équilibré sur le plan physique.")

# =====================================================
# PAGE 2 — ÉQUIPES
# =====================================================
elif page == "🔵 Équipes":
    st.subheader("🔵 Comparaison des équipes")

    df_teams = pd.DataFrame.from_dict(teams, orient="index")
    st.dataframe(df_teams, use_container_width=True)

# =====================================================
# PAGE 3 — JOUEURS
# =====================================================
elif page == "👥 Joueurs":
    st.subheader("👥 Analyse joueurs")

    st.dataframe(
        df_players.sort_values("distance_vs_team", ascending=False),
        use_container_width=True
    )

# =====================================================
# PAGE 4 — HEATMAP
# =====================================================
elif page == "🔥 Heatmap":
    st.subheader("🔥 Heatmap joueur")

    selected_player = st.selectbox(
        "Choisir un joueur",
        list(positions.keys())
    )

    coords = np.array(positions[selected_player])

    fig, ax = plt.subplots(figsize=(6, 10))
    ax.hist2d(coords[:, 0], coords[:, 1], bins=40, cmap="hot")
    ax.invert_yaxis()
    ax.set_title(f"Heatmap — {selected_player}")
    ax.axis("off")

    st.pyplot(fig)
