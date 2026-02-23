import streamlit as st

st.set_page_config(page_title="CoachBot Elite", layout="wide")

st.title("⚽ CoachBot Elite - AI Performance System")

# ======================================================
# SIDEBAR (GLOBAL PLAYER PROFILE)
# ======================================================

with st.sidebar:

    st.header("⚙ Player Profile")

    sidebar_position = st.selectbox(
        "Primary Position",
        ["Forward", "Midfielder", "Defender", "Goalkeeper"]
    )

    sidebar_fitness = st.selectbox(
        "Fitness Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    sidebar_age = st.number_input(
        "Age",
        min_value=10,
        max_value=45,
        step=1
    )

    sidebar_injury = st.text_input("Current Injury (optional)")

    st.markdown("---")
    st.caption("CoachBot Elite v2.0")


# ======================================================
# WEEKLY PLAN GENERATOR FUNCTION
# ======================================================

def generate_weekly_plan(position, injury, fitness_level):

    intensity_map = {
        "Beginner": "Low–Moderate",
        "Intermediate": "Moderate–High",
        "Advanced": "High Intensity"
    }

    intensity = intensity_map.get(fitness_level, "Moderate")
    injury_note = f"Avoid overload due to {injury}." if injury else "No injury restrictions."

    return f"""
## 📅 Weekly Training Plan

---

### Day 1: Finishing & Acceleration
• 10–20m explosive sprints  
• First-step acceleration drills  
• Position-specific finishing for {position}  
Intensity: {intensity}

---

### Day 2: Speed & Agility
• Ladder drills  
• Cone direction changes  
• Reaction-based sprint starts  
Note: {injury_note}

---

### Day 3: Tactical Awareness
• Small-sided game scenarios  
• Decision-making under pressure  
• Movement analysis for {position}

---

### Day 4: Recovery & Mobility
• Light jog  
• Dynamic stretching  
• Foam rolling  
• Joint mobility routine  

---

### Day 5: Strength & Conditioning
• Bodyweight circuits  
• Core stability training  
• Controlled plyometrics (if injury-free)

---

### Day 6: Match Simulation
• High-intensity drills  
• Timed performance challenges  
• Tactical transitions  

---

### Day 7: Rest & Mental Training
• Active recovery or full rest  
• Visualization practice  
• Weekly performance reflection  
"""


# ======================================================
# TABS
# ======================================================

tab_workout, tab_injury, tab_recovery, tab_strategy, tab_assistant = st.tabs([
    "🏋️ Workout Plan",
    "🩺 Injury Assessment",
    "♻️ Recovery",
    "📊 Match Strategy",
    "🤖 AI Assistant"
])


# ======================================================
# WORKOUT PLAN TAB
# ======================================================

with tab_workout:

    st.subheader("Generate Your Weekly Plan")

    if st.button("Generate Weekly Plan"):

        if sidebar_position and sidebar_fitness:
            plan = generate_weekly_plan(
                sidebar_position,
                sidebar_injury,
                sidebar_fitness
            )
            st.markdown(plan)
        else:
            st.warning("Please complete your Player Profile in the sidebar.")


# ======================================================
# INJURY ASSESSMENT TAB
# ======================================================

with tab_injury:

    st.subheader("Injury Assessment")

    if st.button("Analyze Injury"):

        if sidebar_injury:
            st.info(f"""
Based on your input:

• Reduce high-intensity load  
• Focus on controlled mobility work  
• Avoid stress on injured area  
• Seek professional medical advice if pain persists  
""")
        else:
            st.warning("No injury reported in sidebar.")


# ======================================================
# RECOVERY TAB
# ======================================================

with tab_recovery:

    st.subheader("Recovery Protocol Generator")

    recovery_focus = st.selectbox(
        "Recovery Focus",
        ["General Fatigue", "Muscle Soreness", "Post-Match Recovery"]
    )

    if st.button("Generate Recovery Plan"):

        st.markdown(f"""
### Recovery Plan: {recovery_focus}

• Hydration optimization  
• 8+ hours sleep target  
• Light mobility exercises  
• Nutrient timing emphasis  
• Gradual return to intensity
""")


# ======================================================
# MATCH STRATEGY TAB
# ======================================================

with tab_strategy:

    st.subheader("Match Strategy Builder")

    opponent_style = st.selectbox(
        "Opponent Style",
        ["High Press", "Low Block", "Counter Attack"]
    )

    if st.button("Generate Strategy"):

        st.markdown(f"""
### Strategy vs {opponent_style}

• Maintain tactical discipline  
• Quick transitions  
• Exploit positional gaps  
• Structured defensive shape  
• Communication under pressure
""")


# ======================================================
# AI ASSISTANT TAB
# ======================================================

with tab_assistant:

    st.subheader("Ask CoachBot AI")

    question = st.text_input("Ask a performance-related question")

    if st.button("Get Advice"):

        if question:
            st.success("""
AI Guidance:

• Train with measurable goals  
• Improve weak areas strategically  
• Maintain recovery balance  
• Focus on consistency and discipline
""")
        else:
            st.warning("Enter a question first.")
