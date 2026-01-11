import json
import math

FPS = 25  # à ajuster selon ta vidéo

with open("players_data.json") as f:
    data = json.load(f)

stats = {}

for player_id, positions in data.items():
    distance = 0
    for i in range(1, len(positions)):
        x1, y1 = positions[i-1]["x"], positions[i-1]["y"]
        x2, y2 = positions[i]["x"], positions[i]["y"]
        distance += math.dist((x1, y1), (x2, y2))
    time_sec = len(positions) / FPS
    speed = distance / time_sec if time_sec > 0 else 0
    stats[player_id] = {
        "distance_pixels": round(distance, 2),
        "average_speed_px_per_s": round(speed, 2),
        "frames_tracked": len(positions)
    }

with open("players_stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("📊 Stats calculées avec succès !")
print("📁 Fichier généré : players_stats.json")

