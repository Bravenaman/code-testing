import streamlit as st

st.set_page_config(page_title="CoachBot Elite", layout="wide")
st.title("🏆 CoachBot Elite")

# -----------------------
# SIDEBAR
# -----------------------

st.sidebar.header("Athlete Profile")

sport = st.sidebar.selectbox("Sport", ["Football", "Basketball", "Athletics"])
position = st.sidebar.selectbox("Position", ["Forward", "Midfielder", "Defender", "Goalkeeper"])
injury_status = st.sidebar.selectbox(
    "Injury Status",
    ["No Injury", "Minor Injury", "Moderate Injury", "Severe Injury"]
)
training_days = st.sidebar.selectbox("Training Days", [3,4,5,6,7])

generate = st.sidebar.button("🚀 Generate Performance Plan")

# -----------------------
# TABS
# -----------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Injury Assessment", "Recovery", "Workout Plan", "Match Strategy", "CoachBot Assistant"]
)

# -----------------------
# IF BUTTON NOT CLICKED
# -----------------------

if not generate:
    st.info("Complete athlete profile and click 'Generate Performance Plan' to begin.")
else:

    # TRAINING LOAD
    base_load = training_days * 12
    injury_modifier = {
        "No Injury": 0,
        "Minor Injury": -10,
        "Moderate Injury": -20,
        "Severe Injury": -35
    }

    training_load = max(0, base_load + injury_modifier[injury_status])

    if training_load > 75:
        risk = "High ⚠️"
    elif training_load > 50:
        risk = "Moderate ⚠️"
    else:
        risk = "Low ✅"

    # -----------------------
    # TAB 1: INJURY
    # -----------------------

    with tab1:
        st.subheader("⚕ Injury Assessment")

        if injury_status == "No Injury":
            st.success("Athlete is fully fit and cleared for training.")

        elif injury_status == "Minor Injury":
            st.warning("Minor strain detected. Reduce intensity and monitor symptoms.")

        elif injury_status == "Moderate Injury":
            st.warning("Moderate injury. Avoid high-impact drills and focus on mobility.")

        else:
            st.error("Severe injury. Training suspension recommended. Seek medical clearance.")

    # -----------------------
    # TAB 2: RECOVERY
    # -----------------------

    with tab2:
        st.subheader("🔄 Recovery System")

        if injury_status == "No Injury":
            st.write("Hydration, 8+ hours sleep, post-training stretching.")

        elif injury_status == "Minor Injury":
            st.write("Ice therapy, light stretching, reduced workload.")

        elif injury_status == "Moderate Injury":
            st.write("Mobility drills, physiotherapy exercises, no impact training.")

        else:
            st.write("Rest phase. Rehabilitation plan required before return.")

    # -----------------------
    # TAB 3: WORKOUT
    # -----------------------

    with tab3:
        st.subheader("📊 Performance Overview")

        col1, col2 = st.columns(2)
        col1.metric("Training Load Score", f"{training_load}/100")
        col2.metric("Overtraining Risk", risk)

        st.divider()
        st.subheader("📅 Weekly Plan")

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
            st.markdown(f"### Day {i+1}: {workout_structure[i]}")

    # -----------------------
    # TAB 4: MATCH STRATEGY
    # -----------------------

    with tab4:
        st.subheader("🎯 Match Strategy")

        if position == "Forward":
            st.write("Focus on off-ball movement and quick finishing.")

        elif position == "Defender":
            st.write("Maintain compact positioning and strong aerial presence.")

        elif position == "Midfielder":
            st.write("Control tempo and maintain high passing accuracy.")

        else:
            st.write("Improve reflexes and command defensive structure.")

    # -----------------------
    # TAB 5: ASSISTANT
    # -----------------------

    with tab5:
        st.subheader("🤖 CoachBot Assistant")

        st.write(
            f"As a {position} in {sport}, your focus this week is balanced development "
            f"while managing injury status: {injury_status}. "
            "Train smart and prioritize recovery."
        )
