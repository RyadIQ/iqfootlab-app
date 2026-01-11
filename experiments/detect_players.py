from ultralytics import YOLO
import cv2
import json
import os
import time

print("🚀 Script lancé")

# Charger le modèle YOLO
model = YOLO("yolov8n.pt")
print("✅ Modèle YOLO chargé")

# Ouvrir la vidéo
cap = cv2.VideoCapture("match.mp4")
if not cap.isOpened():
    print("❌ Impossible d'ouvrir la vidéo")
    exit()

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Créer dossier output
os.makedirs("output", exist_ok=True)

# Vidéo de sortie compatible Mac
out = cv2.VideoWriter(
    "output/output_tracking.mov",
    cv2.VideoWriter_fourcc(*"avc1"),  # codec H264 compatible Mac
    fps,
    (width, height)
)

players_data = {}
frame_id = 0
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("⛔ Fin de la vidéo")
        break

    # Détection + tracking
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=0.4,
        classes=[0]  # 0 = personne
    )

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy()

        for box, track_id in zip(boxes, ids):
            x1, y1, x2, y2 = box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            track_id = int(track_id)
            if track_id not in players_data:
                players_data[track_id] = []

            players_data[track_id].append({
                "frame": frame_id,
                "x": cx,
                "y": cy
            })

            # Dessiner les boîtes sur la frame
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {track_id}", (int(x1), int(y1)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Écrire la frame dans la vidéo de sortie
    out.write(frame)

    frame_id += 1
    # Progression
    if frame_id % 10 == 0:
        progress = (frame_id / total_frames) * 100
        elapsed = time.time() - start_time
        print(f"⏳ Frame {frame_id}/{total_frames} | {progress:.1f}% | {elapsed:.1f}s écoulées", end="\r")

cap.release()
out.release()

# Sauvegarde JSON
with open("players_data.json", "w") as f:
    json.dump(players_data, f, indent=2)

print("\n✅ Tracking terminé")
print("📁 Fichiers générés : output/output_tracking.mov / players_data.json")
