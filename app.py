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
# STYLE GLOBAL — DARK PREMIUM
# =========================
st.markdown("""
<style>
body {
    background-color: #0B0B0B;
    color: white;
}

.block-container {
    padding-top: 1.5rem;
}

.card {
    background: #141414;
    padding: 24px;
    border-radius: 20px;
    margin-bottom: 20px;
}

.title {
    font-size: 30px;
    font-weight: 800;
}

.subtitle {
    color: #A1A1A1;
    font-size: 14px;
}

.metric {
    font-size: 34px;
    font-weight: 800;
}

.label {
    color: #A1A1A1;
    font-size: 13px;
}

hr {
    border: none;
    border-top: 1px solid #222;
    margin: 30px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("IQ FootLab")
st.sidebar.markdown("Analyse intelligente du match")

# =========================
# LOAD DATA
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
# TOP BAR
# =========================
logo = Image.open("assets/logo.png")

col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image(logo, width=80)
with col_title:
    st.markdown(f"""
    <div class="title">Analyse Match</div>
    <div class="subtitle">{selected_match.replace("_", " ")}</div>
    """, unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# =========================
# HERO METRICS
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="label">Équipe dominante</div>
        <div class="metric">{reading["dominant_mobility_team"]}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="label">Écart d’intensité</div>
        <div class="metric">{reading["mobility_gap"]}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <div class="label">Joueurs analysés</div>
        <div class="metric">22</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# LECTURE COACH
# =========================
st.markdown("<div class='card'>", unsafe_allow_html=True)

if reading["mobility_gap"] > 5:
    st.markdown(
        f"🧠 **Lecture automatique** — {reading['dominant_mobility_team']} a imposé un rythme supérieur sur l’ensemble du match."
    )
else:
    st.markdown("🧠 **Lecture automatique** — Match équilibré sur le plan de l’intensité.")

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# JOUEURS CLÉS
# =========================
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<div class='title'>Joueurs à fort impact</div>", unsafe_allow_html=True)

top_players = df_players.sort_values("distance_vs_team", ascending=False).head(5)

for pid, row in top_players.iterrows():
    st.markdown(f"""
    <div class="card">
        <strong>{pid}</strong><br/>
        <span class="subtitle">Indice d’activité</span><br/>
        <span class="metric">{round(row["distance_vs_team"], 2)}</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# HEATMAP
# =========================
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<div class='title'>Heatmap joueur</div>", unsafe_allow_html=True)

selected_player = st.selectbox("Sélectionner un joueur", list(positions.keys()))
coords = np.array(positions[selected_player])

fig, ax = plt.subplots(figsize=(6, 10))
ax.hist2d(coords[:, 0], coords[:, 1], bins=45, cmap="hot")
ax.invert_yaxis()
ax.axis("off")
fig.patch.set_facecolor("#0B0B0B")

st.pyplot(fig)
