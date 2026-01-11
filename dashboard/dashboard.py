import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="IQ FootLab – Analyse Match",
    layout="wide"
)

st.title("⚽ IQ FootLab – Analyse Match (Vue Staff)")

# =========================
# CHARGEMENT DONNÉES
# =========================
with open("match_stats.json", "r") as f:
    match_stats = json.load(f)

teams = match_stats["teams"]
players_vs_team = match_stats["players_vs_team"]
reading = match_stats["match_reading"]

# =========================
# SYNTHÈSE MATCH
# =========================
st.subheader("📌 Synthèse du match")

col1, col2, col3 = st.columns(3)

dominant_team = reading["dominant_mobility_team"]
gap = reading["mobility_gap"]

with col1:
    st.metric("Équipe la plus mobile", dominant_team)

with col2:
    st.metric("Écart de mobilité", gap)

with col3:
    st.metric("Équipes analysées", "2")

st.divider()

# =========================
# COMPARAISON ÉQUIPES
# =========================
st.subheader("🔵 Comparaison des équipes")

df_teams = pd.DataFrame.from_dict(teams, orient="index")
df_teams.index.name = "Équipe"
st.dataframe(df_teams, use_container_width=True)

st.divider()

# =========================
# JOUEURS VS ÉQUIPE
# =========================
st.subheader("👥 Joueurs vs leur équipe")

df_players = pd.DataFrame.from_dict(players_vs_team, orient="index")
df_players.index.name = "Joueur"

df_players["distance_vs_team"] = df_players["distance_vs_team"].astype(float)

st.dataframe(
    df_players.sort_values("distance_vs_team", ascending=False),
    use_container_width=True
)

st.caption("Indice > 1 = joueur au-dessus de la moyenne de son équipe")

st.divider()

# =========================
# LECTURE COACH AUTOMATIQUE
# =========================
st.subheader("🧠 Lecture coach automatique")

comments = []

if gap > 5:
    comments.append(
        f"L’écart de mobilité est important : {dominant_team} a physiquement dominé le match."
    )
else:
    comments.append(
        "Les deux équipes présentent une intensité physique assez équilibrée."
    )

for team, stats in teams.items():
    if stats["distance_px_per_min_std"] > 10:
        comments.append(
            f"{team} montre une forte disparité d’efforts entre les joueurs."
        )

for c in comments:
    st.write("•", c)

st.caption("Analyse générée automatiquement par IQ FootLab")

