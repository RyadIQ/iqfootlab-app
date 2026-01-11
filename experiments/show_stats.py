import json

# Charger les stats
with open("players_stats.json") as f:
    stats = json.load(f)

for player_id, player_stats in stats.items():
    print(f"Joueur {player_id}:")
    print(f"  Distance parcourue (px) : {player_stats['distance_pixels']}")
    print(f"  Vitesse moyenne (px/s)  : {player_stats['average_speed_px_per_s']}")
    print(f"  Frames suivies           : {player_stats['frames_tracked']}")
    print("-" * 30)

