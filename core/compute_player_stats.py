import json
import numpy as np
import os

INPUT_FILE = "physical_stats.json"
OUTPUT_FILE = "players_metrics_v2.json"

# =========================
# CHARGEMENT DONNÉES
# =========================
with open(INPUT_FILE, "r") as f:
    raw_stats = json.load(f)

player_ids = list(raw_stats.keys())

# =========================
# EXTRACTION POUR MATCH
# =========================
distances = []
efforts = []
accelerations = []

for pid in player_ids:
    p = raw_stats[pid]
    distances.append(p["distance_total_m"])
    efforts.append(p["dynamic_efforts"])
    accelerations.append(p["max_acceleration_m_s2"])

distances = np.array(distances)
efforts = np.array(efforts)
accelerations = np.array(accelerations)

# =========================
# CALCUL SEUILS RELATIFS MATCH
# =========================
effort_dyn_threshold = np.percentile(accelerations, 50)
effort_strong_threshold = np.percentile(accelerations, 80)
effort_explosive_threshold = np.percentile(accelerations, 90)

# =========================
# MOYENNES MATCH
# =========================
mean_distance_per_min = []
mean_efforts_per_min = []

for pid in player_ids:
    p = raw_stats[pid]
    t = max(p["time_played_min"], 0.1)

    mean_distance_per_min.append(p["distance_total_m"] / t)
    mean_efforts_per_min.append(p["dynamic_efforts"] / t)

mean_distance_per_min = np.mean(mean_distance_per_min)
mean_efforts_per_min = np.mean(mean_efforts_per_min)

# =========================
# CALCUL STATS JOUEURS V2
# =========================
players_metrics = {}

for pid in player_ids:
    p = raw_stats[pid]
    time_min = max(p["time_played_min"], 0.1)

    distance_pm = p["distance_total_m"] / time_min
    efforts_pm = p["dynamic_efforts"] / time_min

    # Percentiles match
    dist_percentile = int(np.sum(distances <= p["distance_total_m"]) / len(distances) * 100)
    effort_percentile = int(np.sum(efforts <= p["dynamic_efforts"]) / len(efforts) * 100)
    acc_percentile = int(np.sum(accelerations <= p["max_acceleration_m_s2"]) / len(accelerations) * 100)

    # Indices synthétiques
    mobility_index = round(distance_pm / mean_distance_per_min, 2)
    intensity_index = round(efforts_pm / mean_efforts_per_min, 2)
    explosivity_index = round(
        p["strong_dynamic_efforts"] / max(p["dynamic_efforts"], 1), 2
    )

    players_metrics[pid] = {
        "raw": {
            "distance_total_m": p["distance_total_m"],
            "dynamic_efforts": p["dynamic_efforts"],
            "strong_dynamic_efforts": p["strong_dynamic_efforts"],
            "max_acceleration_m_s2": p["max_acceleration_m_s2"],
            "time_played_min": time_min
        },
        "per_min": {
            "distance_m_per_min": round(distance_pm, 2),
            "efforts_per_min": round(efforts_pm, 2)
        },
        "percentiles": {
            "distance": dist_percentile,
            "efforts": effort_percentile,
            "acceleration": acc_percentile
        },
        "indices": {
            "mobility": mobility_index,
            "intensity": intensity_index,
            "explosivity": explosivity_index
        }
    }

# =========================
# SAUVEGARDE
# =========================
with open(OUTPUT_FILE, "w") as f:
    json.dump(players_metrics, f, indent=2)

print("✅ players_metrics_v2.json généré avec succès")

