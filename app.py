import streamlit as st
from auth import authenticate
import dashboard_app

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="IQ FootLab", layout="wide")

# =========================
# SESSION STATE
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# LANDING PAGE (MARKETING)
# =========================
def home_page():
    st.markdown("## ⚽ IQ FootLab")
    st.markdown("### Analyse intelligente du football à partir de la vidéo")

    st.markdown("""
    **IQ FootLab** transforme une simple vidéo de match en  
    **analyses physiques et tactiques compréhensibles pour les coachs**.

    - 📊 Statistiques match & joueurs  
    - 🔥 Heatmaps automatiques  
    - 🧠 Lecture du jeu assistée  
    - 🎥 100 % basé sur la vidéo  
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Se connecter"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        st.info("Version beta — accès réservé aux coachs")

# =========================
# LOGIN PAGE
# =========================
def login_page():
    st.markdown("## 🔐 Connexion")
    st.markdown("Accès coach")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if authenticate(email, password):
            st.session_state.authenticated = True
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Email ou mot de passe incorrect")

    if st.button("⬅️ Retour"):
        st.session_state.page = "home"
        st.rerun()

# =========================
# LOGOUT
# =========================
def logout_button():
    if st.sidebar.button("🔓 Déconnexion"):
        st.session_state.authenticated = False
        st.session_state.page = "home"
        st.rerun()

# =========================
# ROUTING GLOBAL
# =========================
if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "login":
    login_page()

elif st.session_state.page == "dashboard":
    if not st.session_state.authenticated:
        st.session_state.page = "login"
        st.rerun()
    else:
        logout_button()
        dashboard_app.run()

