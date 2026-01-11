from ultralytics import YOLO
import cv2
import json
import os

# =========================
# CONFIG
# =========================
VIDEO_PATH = "match.mp4"          # ta vidéo
MODEL_PATH = "yolov8n.pt"         # modèle YOLO
OUTPUT_FILE = "players_positions.json"

CONF_THRESHOLD = 0.3
PLAYER_CLASS_ID = 0  # "person" dans COCO

# =========================
# INIT
# =========================
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_PATH)

players_positions = {}

frame_id = 0

print("🚀 Analyse vidéo démarrée")

# =========================
# LECTURE VIDÉO
# =========================
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    # Tracking YOLO + ByteTrack (clé)
    results = model.track(
        frame,
        persist=True,
        conf=CONF_THRESHOLD,
        classes=[PLAYER_CLASS_ID],
        tracker="bytetrack.yaml"
    )

    if results[0].boxes.id is None:
        continue

    boxes = results[0].boxes.xyxy.cpu().numpy()
    track_ids = results[0].boxes.id.cpu().numpy()

    for box, track_id in zip(boxes, track_ids):
        x1, y1, x2, y2 = box

        # Position "pieds" (centre bas bbox)
        x = int((x1 + x2) / 2)
        y = int(y2)

        pid = f"player_{int(track_id)}"

        if pid not in players_positions:
            players_positions[pid] = []

        players_positions[pid].append([x, y])

    if frame_id % 50 == 0:
        print(f"⏱️ Frame {frame_id}")

cap.release()

# =========================
# SAUVEGARDE
# =========================
with open(OUTPUT_FILE, "w") as f:
    json.dump(players_positions, f)

print("✅ Extraction terminée")
print(f"📂 Fichier généré : {OUTPUT_FILE}")
print(f"👥 Joueurs détectés : {len(players_positions)}")

