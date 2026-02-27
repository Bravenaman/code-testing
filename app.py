import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="CoachBot Elite", page_icon="🏆", layout="wide")

st.title("🏆 CoachBot Elite – Youth Performance AI")
st.markdown("⚠️ AI-generated advice. This does NOT replace professional medical clearance.")

# ---------------- GEMINI SETUP ----------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

MODEL = "gemini-1.5-pro"

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- SIDEBAR ----------------
st.sidebar.header("👤 Athlete Profile")

sport_positions = {
    "Football": ["Goalkeeper", "Defender", "Midfielder", "Striker"],
    "Basketball": ["Guard", "Forward", "Center"],
    "Cricket": ["Batsman", "Bowler", "All-Rounder"],
    "Tennis": ["Singles", "Doubles"],
}

sport = st.sidebar.selectbox("Sport", list(sport_positions.keys()), key="sport")
position = st.sidebar.selectbox("Position", sport_positions[sport], key="position")

age = st.sidebar.slider("Age", 10, 25, 15, key="age")
experience = st.sidebar.selectbox(
    "Experience Level",
    ["Beginner", "Intermediate", "Advanced"],
    key="experience"
)

training_intensity = st.sidebar.slider(
    "Training Intensity (1-10)",
    1, 10, 5,
    key="intensity"
)

injury_type = st.sidebar.selectbox(
    "Injury Type",
    ["None", "Minor", "Moderate", "Severe"],
    key="injury"
)

upcoming_match = st.sidebar.toggle("Upcoming Match?", key="match")

# ---------------- RISK CALCULATION ----------------
risk_score = 0

if injury_type == "Severe":
    risk_score += 3
elif injury_type == "Moderate":
    risk_score += 2
elif injury_type == "Minor":
    risk_score += 1

if training_intensity > 7:
    risk_score += 2

if age < 14:
    risk_score += 1

if risk_score <= 2:
    risk_level = "🟢 Low Risk"
elif risk_score <= 4:
    risk_level = "🟡 Moderate Risk"
else:
    risk_level = "🔴 High Risk"

st.sidebar.markdown(f"### Injury Risk Level: {risk_level}")

# ---------------- HELPER FUNCTION ----------------
def generate_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.35,
                top_p=0.9,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🩺 Injury Assessment",
    "🔄 Recovery Plan",
    "🏋️ Weekly Training Plan",
    "🧠 Match Strategy",
    "🤖 Assistant"
])

# ---------------- INJURY TAB ----------------
with tab1:
    st.subheader("Injury Risk Assessment")

    if st.button("Generate Injury Assessment", key="injury_btn"):
        prompt = f"""
        Athlete Profile:
        Sport: {sport}
        Position: {position}
        Age: {age}
        Experience: {experience}
        Injury: {injury_type}
        Training Intensity: {training_intensity}/10

        Provide:
        1. Risk Explanation
        2. Training Modifications
        3. What To Avoid
        4. Medical Disclaimer
        """

        st.markdown(generate_ai_response(prompt))

# ---------------- RECOVERY TAB ----------------
with tab2:
    st.subheader("Recovery Optimization Plan")

    if st.button("Generate Recovery Plan", key="recovery_btn"):
        prompt = f"""
        Athlete Profile:
        Sport: {sport}
        Position: {position}
        Injury: {injury_type}
        Age: {age}

        Provide structured recovery plan including:
        - Immediate Actions
        - 1-Week Plan
        - Hydration Guidance
        - Sleep Recommendation
        - Gradual Return Strategy
        """

        st.markdown(generate_ai_response(prompt))

# ---------------- WEEKLY PLAN TAB ----------------
with tab3:
    st.subheader("Adaptive Weekly Training Plan")

    if st.button("Generate Weekly Plan", key="weekly_btn"):
        prompt = f"""
        Athlete Profile:
        Sport: {sport}
        Position: {position}
        Age: {age}
        Experience: {experience}
        Injury: {injury_type}
        Training Intensity: {training_intensity}/10

        Create a 7-day structured training plan.
        For each day include:
        - Focus Area
        - Intensity Level
        - Short Explanation
        Ensure safety if injury exists.
        """

        st.markdown(generate_ai_response(prompt))

# ---------------- STRATEGY TAB ----------------
with tab4:
    st.subheader("Match Strategy Generator")

    if st.button("Generate Strategy", key="strategy_btn"):
        prompt = f"""
        Athlete Profile:
        Sport: {sport}
        Position: {position}
        Experience: {experience}
        Upcoming Match: {upcoming_match}

        Provide:
        - Tactical Role Advice
        - Key Strength Focus
        - Energy Management Tip
        - Mental Preparation Cue
        """

        st.markdown(generate_ai_response(prompt))

# ---------------- ASSISTANT TAB ----------------
with tab5:
    st.subheader("AI Performance Assistant")

    user_question = st.text_input("Ask your question:", key="assistant_input")

    if st.button("Ask Assistant", key="assistant_btn"):
        if user_question.strip() != "":
            full_prompt = f"""
            Athlete Profile:
            Sport: {sport}
            Position: {position}
            Age: {age}
            Experience: {experience}
            Injury: {injury_type}
            Training Intensity: {training_intensity}/10

            User Question:
            {user_question}
            """

            answer = generate_ai_response(full_prompt)

            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("CoachBot", answer))

    for sender, message in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {message}")
