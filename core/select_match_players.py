import json
import numpy as np

INPUT_FILE = "real_players.json"
OUTPUT_FILE = "match_players.json"
MAX_PLAYERS = 22

print("🚀 Sélection des 22 joueurs du match")

with open(INPUT_FILE, "r") as f:
    players = json.load(f)

player_scores = []

for pid, coords in players.items():
    coords = np.array(coords)

    # temps de présence
    presence = len(coords)

    # distance parcourue
    if len(coords) < 2:
        distance = 0
    else:
        diffs = np.diff(coords, axis=0)
        distance = np.sum(np.linalg.norm(diffs, axis=1))

    score = presence * 0.6 + distance * 0.4
    player_scores.append((pid, score))

# tri décroissant
player_scores.sort(key=lambda x: x[1], reverse=True)

selected = dict(
    (pid, players[pid])
    for pid, _ in player_scores[:MAX_PLAYERS]
)

with open(OUTPUT_FILE, "w") as f:
    json.dump(selected, f, indent=2)

print(f"✅ Joueurs retenus : {len(selected)}")
print("🎯 Liste finale prête pour l’analyse match")

