print("🔥 SCRIPT ALL_IN_ONE DÉMARRÉ 🔥")

from ultralytics import YOLO
import cv2
import json
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# =========================
# CONFIG
# =========================
VIDEO_PATH = "match.mp4"
TERRAIN_PATH = "terrain.png"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# CHARGEMENT MODÈLE
# =========================
print("⏳ Chargement YOLO...")
model = YOLO("yolov8n.pt")
print("✅ YOLO chargé")

# =========================
# OUVERTURE VIDÉO
# =========================
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("❌ Vidéo introuvable")
    exit()

print("🎥 Vidéo ouverte")

players = {}

# =========================
# LECTURE VIDÉO
# =========================
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    print(f"🧠 Frame {frame_count}")

    results = model(frame)

    for box in results[0].boxes.xyxy.cpu().numpy():
        x1, y1, x2, y2 = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        pid = "player"
        players.setdefault(pid, []).append((cx, cy))

cap.release()
print("⛔ Fin vidéo")

# =========================
# SAUVEGARDE POSITIONS
# =========================
with open(f"{OUTPUT_DIR}/positions.json", "w") as f:
    json.dump(players, f)

print("💾 Positions sauvegardées")

# =========================
# HEATMAP
# =========================
print("🔥 Génération heatmap")

terrain = mpimg.imread(TERRAIN_PATH)

x = [p[0] for p in players["player"]]
y = [p[1] for p in players["player"]]

plt.figure(figsize=(12, 7))
plt.imshow(terrain)
plt.hexbin(x, y, gridsize=50, cmap="Reds", alpha=0.6)
plt.gca().invert_yaxis()
plt.title("Heatmap joueurs")
plt.axis("off")

plt.savefig(f"{OUTPUT_DIR}/heatmap_test.png")
plt.close()

print("✅ Heatmap générée")

print("🏁 SCRIPT TERMINÉ AVEC SUCCÈS")
