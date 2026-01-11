import json
import numpy as np
from sklearn.cluster import KMeans

INPUT_FILE = "players_positions.json"
OUTPUT_FILE = "teams_auto.json"

print("🚀 Assignation automatique des équipes")

# =========================
# CHARGEMENT POSITIONS
# =========================
with open(INPUT_FILE, "r") as f:
    positions = json.load(f)

player_ids = list(positions.keys())

# =========================
# FEATURES : POSITION MOYENNE
# =========================
features = []

for pid in player_ids:
    coords = np.array(positions[pid])

    if len(coords) < 10:
        # joueur trop peu vu → on l’ignore
        features.append([0, 0])
        continue

    mean_x = np.mean(coords[:, 0])
    mean_y = np.mean(coords[:, 1])

    features.append([mean_x, mean_y])

features = np.array(features)

# =========================
# CLUSTERING (2 ÉQUIPES)
# =========================
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
labels = kmeans.fit_predict(features)

teams = {}

for pid, label in zip(player_ids, labels):
    teams[pid] = f"team_{label}"

# =========================
# SAUVEGARDE
# =========================
with open(OUTPUT_FILE, "w") as f:
    json.dump(teams, f, indent=2)

print("✅ Assignation terminée")
print(f"📂 Fichier généré : {OUTPUT_FILE}")
print(f"👥 Joueurs traités : {len(teams)}")

