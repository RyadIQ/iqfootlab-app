import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def run():
    # =========================
    # STYLE
    # =========================
    st.markdown("""
    <style>
    body { background-color: #f7f8fa; }
    .card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.markdown("### IQ FootLab")
    page = st.sidebar.radio(
        "Navigation",
        ["📌 Vue Match", "👥 Joueurs", "🔥 Heatmap"]
    )

    # =========================
    # DATA
    # =========================
    MATCHES_DIR = "data/matches"
    matches = sorted(os.listdir(MATCHES_DIR), reverse=True)
    selected_match = st.sidebar.selectbox("Match", matches)

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
        <h2>Analyse du match</h2>
        <p>{selected_match}</p>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # PAGES
    # =========================
    if page == "📌 Vue Match":
        st.markdown(f"<div class='card'>Équipe dominante : <b>{reading['dominant_mobility_team']}</b></div>", unsafe_allow_html=True)

    elif page == "👥 Joueurs":
        st.dataframe(df_players, use_container_width=True)

    elif page == "🔥 Heatmap":
        player = st.selectbox("Joueur", list(positions.keys()))
        coords = np.array(positions[player])
        fig, ax = plt.subplots()
        ax.hist2d(coords[:, 0], coords[:, 1], bins=40)
        ax.invert_yaxis()
        ax.axis("off")
        st.pyplot(fig)
