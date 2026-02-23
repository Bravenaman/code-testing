import streamlit as st

st.set_page_config(page_title="CoachBot Elite", layout="wide")

st.title("⚽ CoachBot Elite - AI Performance System")

# -----------------------------
# WEEKLY PLAN GENERATOR
# -----------------------------

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


# -----------------------------
# TABS
# -----------------------------

tab_workout, tab_injury, tab_recovery, tab_strategy, tab_assistant = st.tabs([
    "🏋️ Workout Plan",
    "🩺 Injury Assessment",
    "♻️ Recovery",
    "📊 Match Strategy",
    "🤖 AI Assistant"
])


# =============================
# WORKOUT PLAN TAB
# =============================

with tab_workout:

    st.subheader("Generate Your Weekly Plan")

    position = st.selectbox(
        "Playing Position",
        ["Forward", "Midfielder", "Defender", "Goalkeeper"]
    )

    fitness_level = st.selectbox(
        "Fitness Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    injury = st.text_input("Current Injury (optional)")

    if st.button("Generate Weekly Plan"):

        if position and fitness_level:
            plan = generate_weekly_plan(position, injury, fitness_level)
            st.markdown(plan)
        else:
            st.warning("Please complete required fields.")


# =============================
# INJURY ASSESSMENT TAB
# =============================

with tab_injury:

    st.subheader("Injury Assessment")

    injury_description = st.text_input("Describe your injury")

    if st.button("Analyze Injury"):

        if injury_description:
            st.info(f"""
Based on your description:

• Reduce high-intensity load  
• Focus on controlled mobility work  
• Prioritize recovery and rest  
• Seek professional medical advice if pain persists
""")
        else:
            st.warning("Please describe the injury first.")


# =============================
# RECOVERY TAB
# =============================

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


# =============================
# MATCH STRATEGY TAB
# =============================

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


# =============================
# AI ASSISTANT TAB
# =============================

with tab_assistant:

    st.subheader("Ask CoachBot AI")

    question = st.text_input("Ask a performance-related question")

    if st.button("Get Advice"):

        if question:
            st.success("""
AI Guidance:

• Focus on consistency  
• Train with measurable goals  
• Improve weak areas strategically  
• Maintain recovery balance  
""")
        else:
            st.warning("Enter a question first.")
