# Calibration terrain simple

# === À MODIFIER ===
REAL_FIELD_WIDTH_M = 68      # mètres
PIXEL_FIELD_WIDTH = 1420     # pixels (mesure vidéo)

PIXEL_TO_M = REAL_FIELD_WIDTH_M / PIXEL_FIELD_WIDTH

print("✅ CALIBRATION TERMINÉE")
print(f"1 pixel = {PIXEL_TO_M:.5f} m")

