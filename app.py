import streamlit as st
import random

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="CoachBot AI", page_icon="🏆", layout="wide")

st.title("🏆 CoachBot AI – Virtual Sports Performance System")
st.markdown("Your intelligent sports training assistant for young athletes.")

# -------------------------------
# SIDEBAR – ATHLETE PROFILE
# -------------------------------
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

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏋️ Training Plan", "⚠️ Injury Assessment", "🧘 Recovery System", "🎯 Match Strategy"]
)

# =====================================================
# TAB 1 – TRAINING PLAN
# =====================================================
with tab1:
    st.header("Personalized Weekly Training Plan")

    if st.button("Generate Full Training Plan"):
        football_position_workouts = {
            "Striker": "Finishing drills, explosive sprint training, shooting accuracy circuits",
            "Midfielder": "Endurance runs, passing drills, vision & ball control sessions",
            "Defender": "Strength training, tackling drills, positional awareness practice",
            "Goalkeeper": "Reaction drills, diving technique, reflex & agility work"
        }

        general_workouts = {
            "Basketball": "Ball handling, vertical jump training, shooting under pressure",
            "Cricket": "Net practice, strength conditioning, match simulation drills",
            "Tennis": "Serve accuracy, lateral movement drills, match endurance sets"
        }

        weekly_days = {
            "Football": ["Speed Training", "Strength & Conditioning", "Ball Control", "Match Simulation", "Recovery Session"],
            "Basketball": ["Dribbling Skills", "Shooting Practice", "Defensive Drills", "Scrimmage Game", "Agility Training"],
            "Cricket": ["Batting Nets", "Bowling Accuracy", "Fielding Drills", "Strength Training", "Match Practice"],
            "Tennis": ["Serve Practice", "Baseline Rally", "Net Play", "Footwork Drills", "Endurance Match"]
        }

        st.subheader("Core Focus")

        if sport == "Football":
            st.success(football_position_workouts[position])
        else:
            st.success(general_workouts[sport])

        st.subheader("Weekly Structure")

        selected_days = random.sample(weekly_days[sport], min(training_days, len(weekly_days[sport])))
        for day in selected_days:
            st.write(f"• {day}")

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

        st.subheader("Risk Evaluation")
        st.warning(f"Status: {risk_status}")

        advice = {
            "Knee": "Reduce jumping and sharp direction changes.",
            "Ankle": "Limit sprinting and add balance work.",
            "Shoulder": "Avoid overhead loading exercises.",
            "Hamstring": "Focus on controlled stretching and avoid max sprints.",
            "Groin": "Reduce lateral explosive movements.",
            "Lower Back": "Avoid heavy spinal loading.",
            "Wrist / Forearm": "Reduce repetitive impact drills.",
            "Shin Splints": "Lower running volume temporarily.",
            "Achilles": "Avoid explosive take-offs."
        }

        if pain_area != "None":
            st.info(advice[pain_area])

# =====================================================
# TAB 3 – RECOVERY SYSTEM
# =====================================================
with tab3:
    st.header("Recovery & Regeneration")

    if st.button("Generate Recovery Plan"):
        recovery_protocols = {
            "Football": "Ice bath (10 min), light jog cooldown, hamstring stretch routine.",
            "Basketball": "Foam rolling, quad & calf stretches, hydration focus.",
            "Cricket": "Shoulder mobility routine, light cardio recovery, hydration.",
            "Tennis": "Forearm stretching, hip mobility work, protein intake post-session."
        }

        st.subheader("Recovery Protocol")
        st.success(recovery_protocols[sport])

        st.subheader("Sleep Recommendation")
        if age_group == "13–15":
            st.write("8–10 hours per night recommended.")
        else:
            st.write("8–9 hours per night recommended.")

        st.subheader("Hydration Target")
        st.write("2–3 Liters daily (increase on intense training days).")

# =====================================================
# TAB 4 – MATCH STRATEGY
# =====================================================
with tab4:
    st.header("Game Strategy Generator")

    opponent_strength = st.selectbox("Opponent Strength", ["Weak", "Average", "Strong"])

    if st.button("Generate Strategy"):
        if opponent_strength == "Weak":
            strategy = "Play aggressively. Press high and control possession."
        elif opponent_strength == "Average":
            strategy = "Balanced play. Maintain structure and exploit gaps."
        else:
            strategy = "Defensive setup with counter-attack focus."

        st.subheader("Tactical Advice")
        st.success(strategy)

        st.subheader("Mental Preparation")
        st.info("Stay composed. Focus on execution, not outcome.")
        
