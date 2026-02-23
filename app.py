import streamlit as st

st.set_page_config(page_title="CoachBot Elite", layout="wide")

st.title("⚽ CoachBot Elite - AI Performance System")

# ======================================================
# SIDEBAR (GLOBAL PLAYER PROFILE)
# ======================================================

with st.sidebar:

    st.header("⚙ Player Profile")

    # NEW: Sport Selector
    sidebar_sport = st.selectbox(
        "Select Sport",
        ["Football", "Basketball", "Cricket", "Tennis"]
    )

    # Position only needed for Football
    if sidebar_sport == "Football":
        sidebar_position = st.selectbox(
            "Primary Position",
            ["Forward", "Midfielder", "Defender", "Goalkeeper"]
        )
    else:
        sidebar_position = "N/A"

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
    st.caption("CoachBot Elite v2.1")


# ======================================================
# UPDATED WEEKLY PLAN GENERATOR (Multi-Sport)
# ======================================================

def generate_weekly_plan(sport, position, injury, fitness_level):

    intensity_map = {
        "Beginner": "Low–Moderate",
        "Intermediate": "Moderate–High",
        "Advanced": "High Intensity"
    }

    intensity = intensity_map.get(fitness_level, "Moderate")
    injury_note = f"Avoid overload due to {injury}." if injury else "No injury restrictions."

    if sport == "Football":
        sport_focus = f"Position-specific drills for {position}"
    elif sport == "Basketball":
        sport_focus = "Shooting accuracy, vertical jump, defensive footwork"
    elif sport == "Cricket":
        sport_focus = "Batting reflex, bowling control, agility drills"
    elif sport == "Tennis":
        sport_focus = "Serve precision, lateral speed, endurance rallies"
    else:
        sport_focus = "General athletic conditioning"

    return f"""
## 📅 Weekly Training Plan – {sport}

---

### Day 1: Skill Development
• {sport_focus}  
• Acceleration drills  
Intensity: {intensity}

---

### Day 2: Speed & Agility
• Ladder drills  
• Reaction training  
Note: {injury_note}

---

### Day 3: Tactical Awareness
• Game scenario simulations  
• Decision-making under pressure  

---

### Day 4: Recovery & Mobility
• Dynamic stretching  
• Light aerobic session  

---

### Day 5: Strength & Conditioning
• Core stability  
• Plyometrics (if injury-free)

---

### Day 6: Competitive Simulation
• High-intensity drills  
• Performance challenges  

---

### Day 7: Rest & Mental Conditioning
• Visualization  
• Match review  
"""


# ======================================================
# TABS (UNCHANGED STRUCTURE)
# ======================================================

tab_workout, tab_injury, tab_recovery, tab_strategy, tab_assistant = st.tabs([
    "🏋️ Workout Plan",
    "🩺 Injury Assessment",
    "♻️ Recovery",
    "📊 Match Strategy",
    "🤖 AI Assistant"
])


# ======================================================
# WORKOUT TAB (ONLY FUNCTION CALL UPDATED)
# ======================================================

with tab_workout:

    st.subheader("Generate Your Weekly Plan")

    if st.button("Generate Weekly Plan"):

        if sidebar_sport and sidebar_fitness:
            plan = generate_weekly_plan(
                sidebar_sport,
                sidebar_position,
                sidebar_injury,
                sidebar_fitness
            )
            st.markdown(plan)
        else:
            st.warning("Please complete your Player Profile in the sidebar.")


# ======================================================
# REMAINING TABS (UNCHANGED)
# ======================================================

with tab_injury:

    st.subheader("Injury Assessment")

    if st.button("Analyze Injury"):

        if sidebar_injury:
            st.info("""
• Reduce high-intensity load  
• Focus on controlled mobility work  
• Avoid stress on injured area  
• Seek professional medical advice if pain persists  
""")
        else:
            st.warning("No injury reported in sidebar.")


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


with tab_assistant:

    st.subheader("Ask CoachBot AI")

    question = st.text_input("Ask a performance-related question")

    if st.button("Get Advice"):

        if question:
            st.success("""
• Train with measurable goals  
• Improve weak areas strategically  
• Maintain recovery balance  
• Focus on consistency and discipline
""")
        else:
            st.warning("Enter a question first.")
