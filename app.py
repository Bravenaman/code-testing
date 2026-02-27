import streamlit as st
from google import genai
import pandas as pd
import time

# ==========================================
# 1. PAGE CONFIGURATION & VIBRANT CSS
# ==========================================
st.set_page_config(page_title="CoachBot AI | NextGen", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0f2fe 0%, #f3e8ff 100%);
}
h1, h2, h3, h4, h5, h6, p, span, label, li, div {
    color: black !important;
    font-family: 'Helvetica Neue', sans-serif;
}
h1, h2, h3 {
    font-family: 'Arial Black', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #e2e8f0 !important; 
}
.stButton>button {
    background: linear-gradient(90deg, #f97316 0%, #e11d48 100%);
    border-radius: 30px;
    padding: 12px 28px;
    font-weight: 800;
    font-size: 18px;
    border: none;
    box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4);
    transition: all 0.3s ease;
}
.stButton>button:hover { 
    transform: translateY(-2px) scale(1.02);
}
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    border: 2px solid #8b5cf6 !important;
    border-radius: 10px;
    background-color: white !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HEADER & API CONFIGURATION
# ==========================================
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3043/3043888.png", width=80) 
with col_title:
    st.title("⚡ CoachBot AI: NextGen Virtual Coach")
    st.markdown("*Empowering youth athletes with AI-driven, personalized sports science.*")

st.sidebar.header("🔐 Authentication")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
    st.sidebar.success("✅ API Key Loaded Securely")
except KeyError:
    st.sidebar.error("❌ API Key missing! Please configure Streamlit Secrets.")
    api_key = None

st.sidebar.header("⚙️ CoachBot Brain Tuning")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.4, 0.1)
top_p = st.sidebar.slider("Focus (Top P)", 0.0, 1.0, 0.9, 0.1)

# ==========================================
# 3. SPORT & POSITION LOGIC (NEW ADDITION)
# ==========================================

sport_positions = {
    "Football": ["Goalkeeper", "Right Back", "Left Back", "Center Back", "Defensive Midfielder", "Attacking Midfielder", "Winger", "Striker"],
    "Basketball": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
    "Cricket": ["Batsman", "Bowler", "All-Rounder", "Wicketkeeper"],
    "Tennis": ["Singles Player", "Doubles Player"],
    "Swimming": ["Freestyle", "Backstroke", "Breaststroke", "Butterfly"],
}

# ==========================================
# 4. MAIN DASHBOARD UI
# ==========================================
tab1, tab2, tab3 = st.tabs(["📋 Athlete Setup", "🏋️‍♂️ Generate Plan", "📊 Analytics & Diet"])

# --- TAB 1 ---
with tab1:
    st.subheader("Define Your Athlete Profile")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        sport = st.selectbox(
            "Primary Sport 🏀",
            list(sport_positions.keys()),
            key="sport_dropdown"
        )

        position = st.selectbox(
            "Position/Role 🎯",
            sport_positions[sport],
            key="position_dropdown"
        )

    with c2:
        age = st.number_input("Athlete Age 🎂", min_value=8, max_value=25, value=16)
        intensity = st.slider("Target Intensity 🔥 (1-10)", 1, 10, 6)
        training_pref = st.text_input("Training Preference 🏋️")

    with c3:
        goal = st.text_input("Desired Goal 🏆")
        diet = st.text_input("Dietary Needs 🥗")

    st.error("⚠️ Current Problem or Injury Context")
    problem_injury = st.text_area(
        "Describe any current problems, injuries, or pain points:"
    )

# --- TAB 2 ---
with tab2:
    st.subheader("🧠 Request AI Coaching")
    
    feature = st.selectbox("Select Coaching Module 🛠️:", [
        "1. Full-Body Workout Plan",
        "2. Safe Recovery Training Schedule",
        "3. Tactical Coaching Tips",
        "4. Nutrition & Meal Guide",
        "5. Warm-up & Cooldown Routine",
        "6. Pre-Match Mental Visualization",
        "7. Hydration & Electrolyte Strategy",
        "8. Positional Decision-Making Drills",
        "9. Sleep & Recovery Optimization",
        "10. Off-Season Conditioning Plan"
    ])

    if st.button("🚀 Generate My Personalized Plan"):
        if not api_key:
            st.error("Cannot generate plan: API key missing.")
        elif not goal.strip() or not diet.strip() or not training_pref.strip():
            st.warning("Please complete required fields in Athlete Setup.")
        elif not problem_injury.strip():
            st.warning("Please describe your injury or problem.")
        else:
            system_prompt = "You are CoachBot AI, an expert youth sports coach. Prioritize safety."
            user_context = f"Athlete: {age}yo {sport} {position}. Injury: {problem_injury}. Goal: {goal}. Diet: {diet}. Intensity: {intensity}/10. Training Preference: {training_pref}."
            task = f"Task: {feature}. Use markdown formatting and bullet points."

            with st.spinner("Generating your personalized plan..."):
                try:
                    time.sleep(1)
                    response = model.generate_content(
                        f"{system_prompt}\n\n{user_context}\n\n{task}",
                        generation_config=genai.types.GenerationConfig(
                            temperature=temperature,
                            top_p=top_p
                        )
                    )

                    st.success("🎉 Plan Generated Successfully!")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Generation Failed: {e}")

# --- TAB 3 ---
with tab3:
    st.subheader("📊 Athlete Dashboard Trackers")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Readiness Score", "85%", "+5%")
    col2.metric("Hydration Level", "Optimal", "Maintained")
    col3.metric("Injury Risk", "Low", "-10%")

    st.markdown("### Weekly Macro Tracker 🍎")
    macro_data = pd.DataFrame({
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "Protein (g)": [120, 130, 120, 140, 125],
        "Carbs (g)": [250, 300, 250, 320, 280]
    })

    st.dataframe(macro_data, use_container_width=True, hide_index=True)
