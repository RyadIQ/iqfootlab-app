print("🔥 TRACKING 22 JOUEURS DÉMARRÉ 🔥")

from ultralytics import YOLO
import cv2
import json

VIDEO_PATH = "match.mp4"
OUTPUT_JSON = "players_tracked.json"

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("❌ Vidéo introuvable")
    exit()

players = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO + ByteTrack
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0],     # class 0 = person
        conf=0.4,
        iou=0.5
    )

    if results[0].boxes.id is None:
        continue

    boxes = results[0].boxes.xyxy.cpu().numpy()
    ids = results[0].boxes.id.cpu().numpy()

    for box, track_id in zip(boxes, ids):
        x1, y1, x2, y2 = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        pid = str(int(track_id))
        players.setdefault(pid, []).append({"x": cx, "y": cy})

cap.release()

with open(OUTPUT_JSON, "w") as f:
    json.dump(players, f, indent=2)

print(f"✅ Tracking terminé — {len(players)} joueurs suivis")
print(f"📁 Données sauvegardées dans {OUTPUT_JSON}")

