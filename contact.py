import streamlit as st
import gspread
from datetime import datetime

def save_contact(name, email, club, message):
    gc = gspread.service_account_from_dict(
        st.secrets["gcp_service_account"]
    )

    sheet = gc.open_by_url(
        st.secrets["sheet"]["url"]
    ).sheet1

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        name,
        email,
        club,
        message
    ])

