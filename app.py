import streamlit as st
import random

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="CoachBot AI", page_icon="🏆", layout="wide")

st.title("🏆 CoachBot AI – Virtual Sports Performance System")
st.markdown("Elite-level personalized training for young athletes (13–18).")

# -------------------------------------------------
# SIDEBAR – ATHLETE PROFILE
# -------------------------------------------------
st.sidebar.header("Athlete Profile")

sport = st.sidebar.selectbox(
    "Select Sport",
    ["Football", "Basketball", "Cricket", "Tennis"]
)

positions_dict = {
    "Football": ["Striker", "Midfielder", "Defender", "Goalkeeper"],
    "Basketball": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
    "Cricket": ["Batsman", "Bowler", "All-Rounder", "Wicket Keeper", "Fielder"],
    "Tennis": ["Singles Player", "Doubles Player", "Baseline Player", "Serve-and-Volley Player"]
}

position = st.sidebar.selectbox("Position", positions_dict[sport])
age_group = st.sidebar.selectbox("Age Group", ["13–15", "16–18"])
fitness_level = st.sidebar.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
training_days = st.sidebar.slider("Training Days Per Week", 1, 7, 3)

# -------------------------------------------------
# SCALING FUNCTIONS (Deep Logic)
# -------------------------------------------------
def scale_sets(base):
    if fitness_level == "Beginner":
        return base
    elif fitness_level == "Intermediate":
        return base + 1
    else:
        return base + 2

def scale_reps(base):
    if fitness_level == "Beginner":
        return base
    elif fitness_level == "Intermediate":
        return int(base * 1.2)
    else:
        return int(base * 1.4)

def conditioning_block():
    if fitness_level == "Beginner":
        return "3 x 200m tempo runs (70% effort)"
    elif fitness_level == "Intermediate":
        return "4 x 200m tempo runs (75% effort)"
    else:
        return "5 x 200m tempo runs (80% effort)"

# -------------------------------------------------
# TABS
# -------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏋️ Deep Training Plan", "⚠️ Injury Assessment", "🧘 Recovery System", "🎯 Match Strategy"]
)

# =====================================================
# TAB 1 – DEEP TRAINING PLAN
# =====================================================
with tab1:

    st.header("Advanced Performance Session Generator")

    if st.button("Generate Deep Training Plan"):

        st.subheader("Day 1 – High Performance Session")

        # Warmup
        st.markdown("### 🔹 Warm-Up")
        st.write("- 5–8 min dynamic mobility")
        st.write("- 3 x 20m progressive acceleration runs")
        st.write("- Movement prep (hips, hamstrings, calves)")

        # Position Block
        st.markdown("### 🔹 Position-Specific Performance Block")

        if sport == "Football":

            if position == "Striker":
                sets = scale_sets(3)
                reps = scale_reps(8)

                st.write(f"- Finishing drills: {sets} sets x {reps} shots")
                st.write(f"- 20m explosive sprints: {sets} x 5 reps")
                st.write(f"- Weak-foot shooting: {sets} x {reps} reps")

            elif position == "Midfielder":
                sets = scale_sets(4)
                reps = scale_reps(10)

                st.write(f"- Passing circuits: {sets} x {reps} reps")
                st.write(f"- 400m endurance runs: {sets} rounds")
                st.write(f"- Ball retention drill: {sets} x 5 minutes")

            elif position == "Defender":
                sets = scale_sets(4)
                reps = scale_reps(6)

                st.write(f"- Strength squats: {sets} x {reps}")
                st.write(f"- Tackling drill: {sets} x 8 reps")
                st.write(f"- Backpedal sprints: {sets} x 20m")

            elif position == "Goalkeeper":
                sets = scale_sets(3)
                reps = scale_reps(5)

                st.write(f"- Reaction saves: {sets} x {reps}")
                st.write(f"- Diving drills: {sets} x {reps}")
                st.write(f"- Lateral shuffles: {sets} x 30 seconds")

        else:
            sets = scale_sets(3)
            reps = scale_reps(10)
            st.write(f"- Core skill drills: {sets} x {reps}")
            st.write(f"- Agility circuits: {sets} rounds")
            st.write(f"- Strength block: {sets} x {reps}")

        # Conditioning
        st.markdown("### 🔹 Conditioning Block")
        st.write(conditioning_block())

        # Cooldown
        st.markdown("### 🔹 Cooldown")
        st.write("- Static stretching (major muscle groups)")
        st.write("- 3–5 min breathing reset")
        st.write("- Light mobility flow")

        # Age Adjustment Notice
        if age_group == "13–15":
            st.info("Volume slightly moderated for developmental safety.")
        else:
            st.info("Higher intensity suitable for older athletes.")

        st.success("Session scaled to fitness level and position.")

# =====================================================
# TAB 2 – INJURY ASSESSMENT
# =====================================================
with tab2:

    st.header("Injury Risk Analysis")

    pain_area = st.selectbox(
        "Pain Area",
        ["None", "Knee", "Ankle", "Shoulder", "Hamstring", "Groin", "Lower Back", "Wrist / Forearm", "Shin Splints", "Achilles"]
    )

    pain_level = st.slider("Pain Level (1–10)", 1, 10, 3)
    training_load = st.slider("Weekly Training Intensity (1–10)", 1, 10, 5)
    previous_injury = st.selectbox("Previous Injury?", ["No", "Yes"])

    if st.button("Assess Risk"):

        risk_score = pain_level + training_load
        if previous_injury == "Yes":
            risk_score += 3

        if risk_score < 8:
            risk_status = "Low Risk"
        elif risk_score < 14:
            risk_status = "Moderate Risk"
        else:
            risk_status = "High Risk"

        st.warning(f"Risk Status: {risk_status}")

# =====================================================
# TAB 3 – RECOVERY SYSTEM
# =====================================================
with tab3:

    st.header("Recovery Protocol Generator")

    if st.button("Generate Recovery Plan"):

        st.success("Foam rolling + mobility work (10–15 min)")
        st.write("Hydration target: 2–3 Liters")
        st.write("Sleep target: 8–10 hours")
        st.write("Post-training protein intake recommended")

# =====================================================
# TAB 4 – MATCH STRATEGY
# =====================================================
with tab4:

    st.header("Match Strategy Generator")

    opponent_strength = st.selectbox("Opponent Strength", ["Weak", "Average", "Strong"])

    if st.button("Generate Strategy"):

        if opponent_strength == "Weak":
            st.success("Play aggressively. High press and control possession.")
        elif opponent_strength == "Average":
            st.success("Balanced tactical approach. Stay structured.")
        else:
            st.success("Defensive compact shape. Counter-attack focus.")

        st.info("Mental cue: Focus on execution, not outcome.")
