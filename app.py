import streamlit as st
from google import genai
import pandas as pd
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="CoachBot AI | NextGen", page_icon="⚡", layout="wide")

# ==========================================
# API SETUP (NEW SDK)
# ==========================================
st.sidebar.header("🔐 Authentication")

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    st.sidebar.success("✅ API Key Loaded Securely")
except Exception:
    st.sidebar.error("❌ API Key missing! Configure in Streamlit Secrets.")
    client = None

st.sidebar.header("⚙️ CoachBot Brain Tuning")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.4, 0.1)
top_p = st.sidebar.slider("Focus (Top P)", 0.0, 1.0, 0.9, 0.1)

# ==========================================
# SPORT & POSITION LOGIC
# ==========================================
sport_positions = {
    "Football": ["Goalkeeper", "Right Back", "Left Back", "Center Back", "Defensive Midfielder", "Attacking Midfielder", "Winger", "Striker"],
    "Basketball": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
    "Cricket": ["Batsman", "Bowler", "All-Rounder", "Wicketkeeper"],
    "Tennis": ["Singles Player", "Doubles Player"],
    "Swimming": ["Freestyle", "Backstroke", "Breaststroke", "Butterfly"],
}

# ==========================================
# TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(["📋 Athlete Setup", "🏋️ Generate Plan", "📊 Analytics"])

# =========================
# TAB 1 — ATHLETE SETUP
# =========================
with tab1:
    st.subheader("Define Athlete Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        sport = st.selectbox("Primary Sport 🏀", list(sport_positions.keys()))
        position = st.selectbox("Position 🎯", sport_positions[sport])

    with col2:
        age = st.number_input("Age 🎂", 8, 25, 16)
        intensity = st.slider("Intensity 🔥 (1-10)", 1, 10, 6)
        training_pref = st.text_input("Training Preference")

    with col3:
        goal = st.text_input("Goal 🏆")
        diet = st.text_input("Diet Needs 🥗")

    st.error("⚠️ Injury / Problem Context")
    problem_injury = st.text_area("Describe current issue:")

# =========================
# TAB 2 — AI GENERATION
# =========================
with tab2:
    st.subheader("AI Coaching Engine")

    feature = st.selectbox("Select Module:", [
        "Workout Plan",
        "Recovery Plan",
        "Match Strategy",
        "Nutrition Guide",
        "Warmup Routine",
        "Mental Preparation",
        "Hydration Strategy",
        "Decision-Making Drills",
        "Sleep Optimization",
        "Off-Season Plan"
    ])

    if st.button("🚀 Generate Plan"):

        if not client:
            st.error("API not configured.")
        elif not goal or not training_pref or not problem_injury:
            st.warning("Complete all required fields in Athlete Setup.")
        else:

            system_prompt = "You are an elite youth sports performance coach. Prioritize safety and clarity."

            user_context = f"""
            Athlete Profile:
            Age: {age}
            Sport: {sport}
            Position: {position}
            Injury/Issue: {problem_injury}
            Goal: {goal}
            Diet: {diet}
            Intensity: {intensity}/10
            Training Preference: {training_pref}
            """

            task = f"Generate a structured {feature}. Use headings and bullet points."

            with st.spinner("Generating..."):
                try:
                    time.sleep(1)

                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=f"{system_prompt}\n\n{user_context}\n\n{task}",
                        config={
                            "temperature": temperature,
                            "top_p": top_p,
                        }
                    )

                    st.success("Plan Generated ✅")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Error: {e}")

# =========================
# TAB 3 — ANALYTICS
# =========================
with tab3:
    st.subheader("Athlete Performance Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Readiness", "85%", "+4%")
    col2.metric("Hydration", "Optimal")
    col3.metric("Injury Risk", "Low")

    st.markdown("### Weekly Nutrition Tracker")

    df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Protein (g)": [120, 130, 115, 140, 125],
        "Carbs (g)": [250, 280, 260, 300, 275]
    })

    st.dataframe(df, use_container_width=True)
