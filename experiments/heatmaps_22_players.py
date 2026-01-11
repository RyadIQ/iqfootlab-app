import json
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

INPUT = "players_22.json"
TERRAIN = "terrain.png"
OUT_DIR = "heatmaps_22"

os.makedirs(OUT_DIR, exist_ok=True)

with open(INPUT) as f:
    players = json.load(f)

terrain = mpimg.imread(TERRAIN)

# ================
# Heatmaps individuelles
# ================
for pid, positions in players.items():
    x = [p["x"] for p in positions]
    y = [p["y"] for p in positions]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.imshow(terrain)

    hb = ax.hexbin(
        x, y,
        gridsize=50,
        cmap="Reds",
        alpha=0.65,
        mincnt=1
    )

    ax.invert_yaxis()
    ax.set_title(f"Heatmap Joueur {pid}")
    ax.axis("off")

    plt.colorbar(hb, ax=ax, label="Présence")
    plt.savefig(f"{OUT_DIR}/heatmap_player_{pid}.png", bbox_inches="tight")
    plt.close()

# ================
# Heatmap globale
# ================
all_x, all_y = [], []

for positions in players.values():
    all_x += [p["x"] for p in positions]
    all_y += [p["y"] for p in positions]

fig, ax = plt.subplots(figsize=(12, 7))
ax.imshow(terrain)

hb = ax.hexbin(
    all_x, all_y,
    gridsize=60,
    cmap="Reds",
    alpha=0.6,
    mincnt=1
)

ax.invert_yaxis()
ax.set_title("Heatmap globale – 22 joueurs")
ax.axis("off")
plt.colorbar(hb, ax=ax, label="Présence")

plt.savefig(f"{OUT_DIR}/heatmap_globale.png", bbox_inches="tight")
plt.close()

print("🔥 Heatmaps propres générées pour les 22 joueurs")

