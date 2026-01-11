import streamlit as st
from auth import authenticate
import dashboard_app

st.set_page_config(page_title="IQ FootLab", layout="wide")

# =========================
# SESSION
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# =========================
# LOGIN PAGE
# =========================
def login_page():
    st.markdown("## ⚽ IQ FootLab")
    st.markdown("### Connexion")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if authenticate(email, password):
            st.session_state.authenticated = True
            st.rerun()  # ✅ rerun officiel Streamlit
        else:
            st.error("Email ou mot de passe incorrect")

# =========================
# LOGOUT
# =========================
def logout_button():
    if st.sidebar.button("🔓 Déconnexion"):
        st.session_state.authenticated = False
        st.rerun()

# =========================
# ROUTING
# =========================
if not st.session_state.authenticated:
    login_page()
else:
    logout_button()
    dashboard_app.run()

