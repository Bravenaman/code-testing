import streamlit as st

st.set_page_config(page_title="CoachBot Elite", layout="wide")
st.title("🏆 CoachBot Elite")

# -----------------------
# SIDEBAR
# -----------------------

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

generate = st.sidebar.button("🚀 Generate Performance Plan")

# -----------------------
# TABS
# -----------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Injury Assessment", "Recovery", "Workout Plan", "Match Strategy", "CoachBot Assistant"]
)

# -----------------------
# WAIT FOR BUTTON
# -----------------------

if not generate:
    st.info("Complete athlete profile and click 'Generate Performance Plan' to begin.")

else:

    # -----------------------
    # SMART TRAINING LOAD
    # -----------------------

    intensity_factor = {
        "Football": 1.2,
        "Basketball": 1.1,
        "Athletics": 1.3
    }

    sport_multiplier = intensity_factor.get(sport, 1)

    base_load = training_days * 12 * sport_multiplier

    injury_modifier = {
        "No Injury": 0,
        "Minor Injury": -10,
        "Moderate Injury": -25,
        "Severe Injury": -40
    }

    training_load = max(0, int(base_load + injury_modifier[injury_status]))

    if training_load > 80:
        risk = "High ⚠️"
    elif training_load > 55:
        risk = "Moderate ⚠️"
    else:
        risk = "Low ✅"

    # -----------------------
    # TAB 1: INJURY
    # -----------------------

    with tab1:
        st.subheader("⚕ Injury Assessment")

        if injury_status == "No Injury":
            st.success("Athlete is fully fit and cleared for structured performance training.")

        elif injury_status == "Minor Injury":
            st.warning("Minor strain detected. Reduce intensity by 20% and monitor discomfort.")

        elif injury_status == "Moderate Injury":
            st.warning("Moderate injury. Avoid high-impact drills and emphasize mobility.")

        else:
            st.error("Severe injury detected. Training suspension and medical clearance required.")

    # -----------------------
    # TAB 2: RECOVERY
    # -----------------------

    with tab2:
        st.subheader("🔄 Recovery System")

        if injury_status == "No Injury":
            st.write("Hydration protocol, 8+ hours sleep, post-session stretching.")

        elif injury_status == "Minor Injury":
            st.write("Ice therapy, reduced volume training, controlled mobility work.")

        elif injury_status == "Moderate Injury":
            st.write("Mobility drills, physiotherapy-style exercises, no impact loading.")

        else:
            st.write("Full rest phase. Focus on rehabilitation and structured recovery plan.")

    # -----------------------
    # TAB 3: WORKOUT PLAN
    # -----------------------

    with tab3:
        st.subheader("📊 Performance Overview")

        col1, col2 = st.columns(2)
        col1.metric("Training Load Score", f"{training_load} / 100")
        col2.metric("Overtraining Risk", risk)

        st.divider()
        st.subheader("📅 Weekly Plan")

        def generate_week_plan(sport, position, injury_status, training_days):

            base_structure = [
                "Strength & Power",
                "Speed & Agility",
                "Tactical Awareness",
                "Recovery & Mobility",
                "Conditioning",
                "Explosive Training",
                "Active Recovery"
            ]

            plan = base_structure[:training_days]

            # Position-based emphasis
            if position == "Forward":
                plan[0] = "Finishing & Acceleration"
            elif position == "Defender":
                plan[0] = "Strength & Defensive Positioning"
            elif position == "Midfielder":
                plan[0] = "Endurance & Ball Control"
            elif position == "Goalkeeper":
                plan[0] = "Reflex & Reaction Training"

            # Injury logic
            if injury_status == "Moderate Injury":
                plan[-1] = "Extended Mobility & Controlled Rehab"

            if injury_status == "Severe Injury":
                plan = ["Rehabilitation & Rest Focus"] * training_days

            return plan

        weekly_plan = generate_week_plan(
            sport, position, injury_status, training_days
        )

        for i, session in enumerate(weekly_plan):
            st.markdown(f"### Day {i+1}: {session}")
            st.markdown("---")

    # -----------------------
    # TAB 4: MATCH STRATEGY
    # -----------------------

    with tab4:
        st.subheader("🎯 Match Strategy")

        if position == "Forward":
            st.write("Exploit defensive gaps, prioritize quick finishing and off-ball runs.")

        elif position == "Defender":
            st.write("Maintain compact structure, strong aerial duels, and positional discipline.")

        elif position == "Midfielder":
            st.write("Control tempo, maintain passing accuracy, transition play efficiently.")

        else:
            st.write("Enhance reflex speed and command defensive organization.")

    # -----------------------
    # TAB 5: COACHBOT
    # -----------------------

    with tab5:
        st.subheader("🤖 CoachBot Assistant")

        st.write(
            f"As a {position} in {sport}, your weekly structure balances "
            f"performance development with injury status: {injury_status}. "
            "Maintain consistency, manage workload intelligently, and prioritize long-term growth."
        )
