import json

INPUT = "players_tracked.json"
OUTPUT = "players_22.json"
NB_PLAYERS = 22

with open(INPUT) as f:
    data = json.load(f)

# Trier par nombre de positions (frames)
sorted_players = sorted(
    data.items(),
    key=lambda item: len(item[1]),
    reverse=True
)

# Garder les 22 plus persistants
top_players = dict(sorted_players[:NB_PLAYERS])

with open(OUTPUT, "w") as f:
    json.dump(top_players, f, indent=2)

print(f"✅ {NB_PLAYERS} joueurs sélectionnés")
for pid, pos in top_players.items():
    print(f"Joueur {pid} → {len(pos)} frames")

