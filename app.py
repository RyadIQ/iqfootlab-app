import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="IQ FootLab",
    layout="wide"
)

# =========================
# STYLE SOBRE & PRO
# =========================
st.markdown("""
<style>
body {
    background-color: #f7f8fa;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.title {
    font-size: 26px;
    font-weight: 700;
}

.subtitle {
    color: #6b7280;
    font-size: 14px;
}

.metric {
    font-size: 24px;
    font-weight: 700;
}

.label {
    color: #6b7280;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (RESTAURÉE)
# =========================
logo_path = "assets/logo.png"

with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)

    st.markdown("### IQ FootLab")
    st.markdown("Analyse intelligente du match")

    page = st.radio(
        "Navigation",
        ["📌 Vue Match", "👥 Joueurs", "🔥 Heatmap"]
    )

# =========================
# LOAD DATA
# =========================
MATCHES_DIR = "data/matches"
matches = sorted(os.listdir(MATCHES_DIR), reverse=True)

selected_match = st.sidebar.selectbox("📅 Match", matches)
match_path = os.path.join(MATCHES_DIR, selected_match)

with open(os.path.join(match_path, "match_stats.json")) as f:
    match_stats = json.load(f)

with open(os.path.join(match_path, "players_positions.json")) as f:
    positions = json.load(f)

reading = match_stats["match_reading"]
players_vs_team = match_stats["players_vs_team"]

df_players = pd.DataFrame.from_dict(players_vs_team, orient="index")
df_players["distance_vs_team"] = df_players["distance_vs_team"].astype(float)

# =========================
# HEADER
# =========================
st.markdown(f"""
<div class="card">
    <div class="title">Analyse du match</div>
    <div class="subtitle">{selected_match.replace("_", " ")}</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# PAGE — MATCH
# =====================================================
if page == "📌 Vue Match":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="label">Équipe dominante</div>
            <div class="metric">{reading["dominant_mobility_team"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="label">Écart d’intensité</div>
            <div class="metric">{reading["mobility_gap"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="label">Joueurs analysés</div>
            <div class="metric">22</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Lecture coach")

    if reading["mobility_gap"] > 5:
        st.success(f"{reading['dominant_mobility_team']} a dominé physiquement le match.")
    else:
        st.info("Match équilibré sur le plan physique.")

# =====================================================
# PAGE — JOUEURS
# =====================================================
elif page == "👥 Joueurs":

    st.markdown("### 👥 Joueurs clés")

    top_players = df_players.sort_values("distance_vs_team", ascending=False).head(5)

    for pid, row in top_players.iterrows():
        st.markdown(f"""
        <div class="card">
            <strong>{pid}</strong><br/>
            Indice d’activité : <strong>{round(row["distance_vs_team"], 2)}</strong>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Voir tous les joueurs"):
        st.dataframe(
            df_players.sort_values("distance_vs_team", ascending=False),
            use_container_width=True
        )

# =====================================================
# PAGE — HEATMAP
# =====================================================
elif page == "🔥 Heatmap":

    selected_player = st.selectbox(
        "Sélectionner un joueur",
        list(positions.keys())
    )

    coords = np.array(positions[selected_player])

    fig, ax = plt.subplots(figsize=(6, 10))
    ax.hist2d(coords[:, 0], coords[:, 1], bins=40, cmap="hot")
    ax.invert_yaxis()
    ax.axis("off")

    st.pyplot(fig)
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
