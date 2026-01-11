import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# CONFIG GLOBALE
# =========================
st.set_page_config(
    page_title="IQ FootLab",
    layout="wide"
)

# =========================
# STYLE GLOBAL (EYEBALL-LIKE)
# =========================
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.title {
    font-size: 32px;
    font-weight: 800;
}

.subtitle {
    color: #6b7280;
    font-size: 15px;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
}

.metric-label {
    color: #6b7280;
    font-size: 14px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin: 20px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CHARGEMENT MATCHS
# =========================
MATCHES_DIR = "data/matches"
matches = sorted(os.listdir(MATCHES_DIR), reverse=True)

selected_match = st.sidebar.selectbox(
    "📅 Match",
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
# HEADER MATCH
# =========================
st.markdown(f"""
<div class="card">
    <div class="title">⚽ Analyse du match</div>
    <div class="subtitle">{selected_match.replace("_", " ")}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# NAVIGATION
# =========================
page = st.sidebar.radio(
    "Navigation",
    ["📌 Match", "👥 Joueurs", "🔥 Heatmap"]
)

# =====================================================
# PAGE MATCH
# =====================================================
if page == "📌 Match":

    st.markdown('<div class="section-title">📊 Match en un regard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">Équipe dominante</div>
            <div class="metric-value">{reading["dominant_mobility_team"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">Écart d’intensité</div>
            <div class="metric-value">{reading["mobility_gap"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">Joueurs analysés</div>
            <div class="metric-value">22</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🧠 Lecture coach</div>', unsafe_allow_html=True)

    if reading["mobility_gap"] > 5:
        st.success(
            f"{reading['dominant_mobility_team']} a montré une intensité supérieure sur l’ensemble du match."
        )
    else:
        st.info("Match équilibré sur le plan physique.")

# =====================================================
# PAGE JOUEURS
# =====================================================
elif page == "👥 Joueurs":

    st.markdown('<div class="section-title">👥 Joueurs clés</div>', unsafe_allow_html=True)

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
# PAGE HEATMAP
# =====================================================
elif page == "🔥 Heatmap":

    st.markdown('<div class="section-title">🔥 Heatmap joueur</div>', unsafe_allow_html=True)

    selected_player = st.selectbox(
        "Choisir un joueur",
        list(positions.keys())
    )

    coords = np.array(positions[selected_player])

    fig, ax = plt.subplots(figsize=(6, 10))
    ax.hist2d(coords[:, 0], coords[:, 1], bins=40, cmap="hot")
    ax.invert_yaxis()
    ax.axis("off")

    st.pyplot(fig)

