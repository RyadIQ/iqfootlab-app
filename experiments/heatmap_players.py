import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Charger l'image du terrain
terrain_img = mpimg.imread("terrain.png")

# Charger les positions des joueurs
with open("players_data.json") as f:
    data = json.load(f)

# --- Heatmap par joueur ---
for player_id, positions in data.items():
    pid = int(player_id)
    if pid > 21:            # ignorer les IDs > 21
        continue
    if len(positions) < 30:  # ignorer les joueurs suivis très peu de frames
        continue

    x_coords = [p["x"] for p in positions]
    y_coords = [p["y"] for p in positions]

    fig, ax = plt.subplots(figsize=(12,7))
    ax.imshow(terrain_img)
    hb = ax.hexbin(
        x_coords, y_coords,
        gridsize=50,
        cmap='Reds',
        alpha=0.6,
        mincnt=1
    )
    ax.invert_yaxis()
    ax.set_title(f"Heatmap Joueur {player_id}")
    plt.colorbar(hb, ax=ax, label='Présence / Intensité')
    plt.axis('off')

    plt.savefig(f"heatmap_player_{player_id}.png", bbox_inches='tight')
    plt.close()

# --- Heatmap globale tous joueurs ---
all_x = []
all_y = []

for player_id, positions in data.items():
    pid = int(player_id)
    if pid > 21 or len(positions) < 30:
        continue
    all_x += [p["x"] for p in positions]
    all_y += [p["y"] for p in positions]

fig, ax = plt.subplots(figsize=(12,7))
ax.imshow(terrain_img)
hb = ax.hexbin(
    all_x, all_y,
    gridsize=50,
    cmap='Reds',
    alpha=0.6,
    mincnt=1
)
ax.invert_yaxis()
ax.set_title("Heatmap globale des 22 joueurs")
plt.colorbar(hb, ax=ax, label='Présence / Intensité')
plt.axis('off')
plt.savefig("heatmap_tous_joueurs.png", bbox_inches='tight')
plt.close()

print("📊 Heatmaps individuelles et globale générées avec succès !")

