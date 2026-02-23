import streamlit as st

st.set_page_config(page_title="CoachBot Elite", layout="wide")

st.title("🏆 CoachBot Elite")

# ------------------------
# SIDEBAR INPUTS
# ------------------------
st.sidebar.header("Athlete Profile")

sport = st.sidebar.selectbox(
    "Sport",
    ["Football", "Basketball", "Athletics"]
)

position = st.sidebar.selectbox(
    "Position",
    ["Forward", "Midfielder", "Defender", "Goalkeeper"]
)

injury_status = st.sidebar.selectbox(
    "Injury Status",
    ["No Injury", "Minor Injury", "Moderate Injury", "Severe Injury"]
)

training_days = st.sidebar.selectbox(
    "Training Days",
    [3, 4, 5, 6, 7]
)

# ------------------------
# TRAINING LOAD LOGIC
# ------------------------

base_load = training_days * 12

injury_modifier = {
    "No Injury": 0,
    "Minor Injury": -10,
    "Moderate Injury": -20,
    "Severe Injury": -35
}

training_load_score = max(0, base_load + injury_modifier[injury_status])

if training_load_score > 75:
    risk = "High ⚠️"
elif training_load_score > 50:
    risk = "Moderate ⚠️"
else:
    risk = "Low ✅"

# ------------------------
# TABS
# ------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Injury Assessment", "Recovery", "Workout Plan", "Match Strategy", "CoachBot Assistant"]
)

# ------------------------
# WORKOUT PLAN TAB
# ------------------------

with tab3:

    st.subheader("📊 Performance Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Training Load Score", f"{training_load_score} / 100")

    with col2:
        st.metric("Overtraining Risk", risk)

    with col3:
        if position == "Forward":
            focus = "Speed & Finishing"
        elif position == "Defender":
            focus = "Strength & Positioning"
        else:
            focus = "Balanced Development"

        st.metric("Focus Area", focus)

    st.divider()
    st.subheader("📅 Weekly Workout Schedule")

    workout_structure = [
        "Strength & Power",
        "Speed & Agility",
        "Tactical Awareness",
        "Recovery & Mobility",
        "Conditioning",
        "Explosive Training",
        "Active Recovery"
    ]

    for i in range(training_days):
        day_title = workout_structure[i]
        st.markdown(f"### Day {i+1}: {day_title}")

        if day_title == "Strength & Power":
            st.write("Squats, Deadlifts, Core Stability Work")

        elif day_title == "Speed & Agility":
            st.write("Sprint Drills, Ladder Work, Acceleration Runs")

        elif day_title == "Tactical Awareness":
            st.write("Positional Drills, Game Simulation")

        elif day_title == "Recovery & Mobility":
            st.write("Light Stretching, Mobility Exercises")

        elif day_title == "Conditioning":
            st.write("Interval Runs, Endurance Training")

        elif day_title == "Explosive Training":
            st.write("Plyometrics, Jump Training")

        elif day_title == "Active Recovery":
            st.write("Low Intensity Jog, Flexibility Work")

        st.markdown("---")

    # Injury Adjustments
    st.subheader("⚕ Injury Adjustment")

    if injury_status == "Moderate Injury":
        st.warning("Avoid high-impact exercises. Focus on mobility and gradual progression.")

    elif injury_status == "Severe Injury":
        st.error("Training should prioritize recovery only. Medical clearance recommended.")

    elif injury_status == "Minor Injury":
        st.info("Reduce intensity by 20% and monitor discomfort.")

    else:
        st.success("No restrictions. Train at full capacity.")

    st.subheader("📈 Estimated Progress")

    st.write("- Speed ↑")
    st.write("- Strength ↑↑")
    st.write("- Tactical Awareness ↑")

    st.info("Stay consistent and listen to your body. Smart training prevents setbacks.")
