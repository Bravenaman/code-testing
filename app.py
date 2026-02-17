import streamlit as st
import random

st.set_page_config(page_title="CoachBot AI", page_icon="🏆")

st.title("🏆 CoachBot AI – Virtual Sports Coach")

st.write("Generate personalized training, nutrition and strategy plans.")

# -------------------------
# Athlete Profile
# -------------------------
st.header("Athlete Profile")

sport = st.selectbox("Select Sport", ["Football", "Basketball", "Cricket", "Tennis"])
position = st.text_input("Position")
age_group = st.selectbox("Age Group", ["13-15", "16-18"])
fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
days = st.slider("Training days per week", 1, 7, 3)
injury = st.selectbox("Injury Risk Area", ["None", "Knee", "Ankle", "Shoulder"])

st.divider()

# -------------------------
# Workout Generator
# -------------------------
def generate_workout():
    warmups = ["5 min jogging", "Jump rope", "Dynamic stretching"]
    strength = ["Push-ups", "Squats", "Lunges", "Core plank"]
    cooldown = ["Stretching", "Foam rolling", "Breathing exercises"]

    sport_drills = {
        "Football": ["Sprint drills", "Dribbling cones", "Shooting practice"],
        "Basketball": ["Layup drills", "Ball handling", "3-point shooting"],
        "Cricket": ["Batting nets", "Bowling practice", "Fielding drills"],
        "Tennis": ["Serve practice", "Footwork ladder", "Rally drills"]
    }

    injury_tip = ""
    if injury != "None":
        injury_tip = f"⚠ Reduce high impact exercises to protect your {injury.lower()}."

    return f"""
Warm-up: {random.choice(warmups)}
Strength: {random.choice(strength)}
Skill Drill: {random.choice(sport_drills[sport])}
Cooldown: {random.choice(cooldown)}

{injury_tip}
"""

# -------------------------
# Weekly Plan Generator
# -------------------------
def generate_schedule():
    days_list = ["Speed & Agility", "Strength", "Skill Training", "Match Simulation", "Recovery"]
    plan = ""
    for i in range(days):
        plan += f"Day {i+1}: {random.choice(days_list)}\n"
    return plan

# -------------------------
# Nutrition Generator
# -------------------------
def nutrition_tips():
    tips = [
        "Eat protein after training for muscle recovery.",
        "Drink at least 2–3 litres of water daily.",
        "Include fruits before training for energy.",
        "Eat carbs before matches for stamina.",
        "Avoid junk food before training."
    ]
    return "\n".join(random.sample(tips, 3))

# -------------------------
# Motivation Generator
# -------------------------
def motivation():
    quotes = [
        "Consistency beats talent.",
        "Train hard, play easy.",
        "Small progress every day.",
        "Discipline creates champions.",
        "Push past your limits."
    ]
    return random.choice(quotes)

# -------------------------
# Game Strategy Generator
# -------------------------
def strategy():
    opponent = st.selectbox("Opponent Strength", ["Weak", "Average", "Strong"])
    if opponent == "Weak":
        return "Play aggressively and practice new tactics."
    if opponent == "Average":
        return "Maintain balance between attack and defense."
    if opponent == "Strong":
        return "Focus on defense and counter attacks."

# -------------------------
# Buttons
# -------------------------
st.header("Generate Plans")

if st.button("Generate Workout"):
    st.success(generate_workout())

if st.button("Generate Weekly Schedule"):
    st.info(generate_schedule())

if st.button("Nutrition Tips"):
    st.warning(nutrition_tips())

if st.button("Motivate Me"):
    st.success(motivation())

st.subheader("Game Day Strategy")
st.write(strategy())
