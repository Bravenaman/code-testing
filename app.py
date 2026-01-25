import streamlit as st
from datetime import datetime
import random
import pandas as pd
from PIL import Image, ImageDraw

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="MedTimer – Daily Medicine Companion",
    layout="wide"
)

st.title("💊 MedTimer – Daily Medicine Companion")
st.write("A friendly app that helps you stay consistent with your daily medicines.")

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
if "medicines" not in st.session_state:
    st.session_state.medicines = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "badges" not in st.session_state:
    st.session_state.badges = set()

# -------------------------------------------------
# Utility Functions
# -------------------------------------------------
def get_status(med_time, taken):
    now = datetime.now().time()
    if taken:
        return "Taken"
    elif now < med_time:
        return "Upcoming"
    else:
        return "Missed"

def calculate_adherence():
    if not st.session_state.medicines:
        return 0
    taken = sum(1 for m in st.session_state.medicines if m["taken"])
    return int((taken / len(st.session_state.medicines)) * 100)

def update_streak():
    if not st.session_state.medicines:
        return

    all_taken = all(m["taken"] for m in st.session_state.medicines)

    if all_taken:
        st.session_state.streak += 1
    else:
        if st.session_state.streak > 0:
            st.warning("⚠️ Streak reset. Tomorrow is a fresh start!")
        st.session_state.stre_
