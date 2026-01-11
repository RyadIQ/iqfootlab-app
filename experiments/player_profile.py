# ==========================================
# PROFIL JOUEUR – IQ FOOTLAB
# ==========================================

def generate_player_profile(player_stats):
    profile = []

    distance = player_stats["distance_total_m"]
    efforts = player_stats["dynamic_efforts"]
    effort_distance = player_stats["effort_distance_m"]
    max_acc = player_stats["max_acceleration_m_s2"]

    # MOBILITÉ
    if distance > 60:
        profile.append("Joueur très mobile, présent sur de nombreuses phases de jeu.")
    elif distance > 40:
        profile.append("Joueur mobile, impliqué régulièrement dans le jeu.")
    else:
        profile.append("Joueur plutôt statique, impliqué sur des phases ciblées.")

    # INTENSITÉ
    if efforts > 12:
        profile.append("Profil très dynamique avec de nombreux changements de rythme.")
    elif efforts > 6:
        profile.append("Profil dynamique avec une intensité de jeu régulière.")
    else:
        profile.append("Profil calme avec peu de changements de rythme.")

    # TYPE D’EFFORT
    if effort_distance > 15:
        profile.append("Réalise des efforts prolongés dans ses déplacements.")
    else:
        profile.append("Réalise principalement des efforts courts et explosifs.")

    # ACCÉLÉRATION
    if max_acc > 2.0:
        profile.append("Capacité d’accélération élevée pour son âge.")
    elif max_acc > 1.2:
        profile.append("Capacité d’accélération correcte.")
    else:
        profile.append("Capacité d’accélération limitée.")

    return profile

