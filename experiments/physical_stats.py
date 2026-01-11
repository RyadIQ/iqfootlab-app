import json
import math

# =========================
# CONFIGURATION
# =========================
INPUT_FILE = "players_22.json"
OUTPUT_FILE = "physical_stats.json"

FPS = 25
PIXEL_TO_M = 68 / 6000  # calibration réelle terrain

# Seuils U13 vidéo
ACC_THRESHOLD = 0.6        # m/s²
STRONG_ACC_THRESHOLD = 1.2 # m/s²

MIN_FRAMES_BETWEEN_EFFORTS = int(0.8 * FPS)  # 0.8 seconde
SMOOTH_WINDOW = 3

# =========================
# FONCTION DE LISSAGE
# =========================
def smooth(values, window):
    smoothed = []
    for i in range(len(values)):
        start = max(0, i - window)
        end = min(len(values), i + window + 1)
        smoothed.append(sum(values[start:end]) / (end - start))
    return smoothed

# =========================
# CHARGEMENT DONNÉES
# =========================
with open(INPUT_FILE, "r") as f:
    players = json.load(f)

stats = {}

# =========================
# CALCUL STATS
# =========================
for pid, positions in players.items():
    if len(positions) < 5:
        continue

    speeds = []
    total_distance = 0.0

    # Calcul des vitesses
    for i in range(1, len(positions)):
        dx = positions[i]["x"] - positions[i - 1]["x"]
        dy = positions[i]["y"] - positions[i - 1]["y"]

        d_pixels = math.hypot(dx, dy)
        d_m = d_pixels * PIXEL_TO_M
        speed = d_m * FPS

        speeds.append(speed)
        total_distance += d_m

    # Lissage des vitesses
    speeds = smooth(speeds, SMOOTH_WINDOW)

    effort_count = 0
    strong_effort_count = 0
    effort_distance = 0.0
    max_acc = 0.0

    last_effort_frame = -MIN_FRAMES_BETWEEN_EFFORTS

    # Calcul des efforts dynamiques
    for i in range(1, len(speeds)):
        acc = (speeds[i] - speeds[i - 1]) * FPS
        max_acc = max(max_acc, acc)

        if acc >= ACC_THRESHOLD and (i - last_effort_frame) >= MIN_FRAMES_BETWEEN_EFFORTS:
            effort_count += 1
            effort_distance += speeds[i] / FPS
            last_effort_frame = i

            if acc >= STRONG_ACC_THRESHOLD:
                strong_effort_count += 1

    duration_sec = len(positions) / FPS

    stats[pid] = {
        "distance_total_m": round(total_distance, 1),
        "dynamic_efforts": effort_count,
        "strong_dynamic_efforts": strong_effort_count,
        "effort_distance_m": round(effort_distance, 1),
        "max_acceleration_m_s2": round(max_acc, 2),
        "time_played_min": round(duration_sec / 60, 2)
    }

# =========================
# SAUVEGARDE JSON
# =========================
with open(OUTPUT_FILE, "w") as f:
    json.dump(stats, f, indent=2)

# =========================
# AFFICHAGE TERMINAL
# =========================
print("STATS – EFFORTS DYNAMIQUES (U13)\n")

for pid, s in stats.items():
    print("Joueur", pid)
    print(" Distance totale      :", s["distance_total_m"], "m")
    print(" Efforts dynamiques   :", s["dynamic_efforts"])
    print(" Efforts forts        :", s["strong_dynamic_efforts"])
    print(" Distance effort      :", s["effort_distance_m"], "m")
    print(" Accélération max     :", s["max_acceleration_m_s2"], "m/s²")
    print(" Temps joué           :", s["time_played_min"], "min")
    print("-" * 40)

print("\nFichier généré :", OUTPUT_FILE)
