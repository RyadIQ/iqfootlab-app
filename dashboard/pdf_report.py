from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import json
import os

from player_profile import generate_player_profile

# =========================
# CONFIG
# =========================
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# GÉNÉRATION PDF
# =========================
def generate_pdf(player_id):
    # Charger les stats
    with open("physical_stats.json", "r") as f:
        stats = json.load(f)

    player = stats[player_id]

    # Profil joueur
    profile = generate_player_profile(player)

    heatmap_path = f"heatmaps_22/heatmap_player_{player_id}.png"
    output_path = f"{OUTPUT_DIR}/rapport_joueur_{player_id}.pdf"

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # TITRE
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, height - 2 * cm, "IQ FootLab – Rapport Joueur")

    # INFOS
    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, height - 3 * cm, f"Joueur ID : {player_id}")
    c.drawString(2 * cm, height - 3.8 * cm, "Analyse vidéo – Formation")

    # STATS
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 5.2 * cm, "Statistiques physiques")

    c.setFont("Helvetica", 11)
    y = height - 6.2 * cm

    lines = [
        f"Distance totale : {player['distance_total_m']} m",
        f"Efforts dynamiques : {player['dynamic_efforts']}",
        f"Efforts forts : {player['strong_dynamic_efforts']}",
        f"Distance en effort : {player['effort_distance_m']} m",
        f"Accélération max : {player['max_acceleration_m_s2']} m/s²",
        f"Temps joué : {player['time_played_min']} min"
    ]

    for line in lines:
        c.drawString(2 * cm, y, line)
        y -= 0.6 * cm

    # PROFIL JOUEUR
    y -= 0.6 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Profil joueur – Lecture coach")

    c.setFont("Helvetica", 11)
    y -= 0.8 * cm

    for sentence in profile:
        c.drawString(2.5 * cm, y, f"- {sentence}")
        y -= 0.6 * cm

    # HEATMAP
    if os.path.exists(heatmap_path):
        y -= 0.8 * cm
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, y, "Heatmap du joueur")

        img = ImageReader(heatmap_path)
        c.drawImage(
            img,
            2 * cm,
            y - 10 * cm,
            width=16 * cm,
            preserveAspectRatio=True
        )

    # FOOTER
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        2 * cm,
        1.5 * cm,
        "IQ FootLab – données adaptées à l’âge et au contexte vidéo"
    )

    c.save()
    return output_path


# =========================
# TEST TERMINAL
# =========================
if __name__ == "__main__":
    print("TEST PDF EN COURS...")
    path = generate_pdf(list(json.load(open("physical_stats.json")).keys())[0])
    print("PDF généré :", path)

