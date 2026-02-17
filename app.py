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
# NEW Sport-Specific Workout Generator
# -------------------------
def generate_workout():

    workouts = {

        "Football": {
            "warmup": ["Light jogging", "High knees", "Dynamic leg swings"],
            "strength": ["Squats", "Lunges", "Core plank", "Calf raises"],
            "skills": ["Sprint intervals", "Dribbling cone drills", "Shooting practice"],
            "cooldown": ["Hamstring stretch", "Quad stretch", "Foam rolling"]
        },

        "Basketball": {
            "warmup": ["Skipping rope", "Arm circles", "Dynamic stretches"],
            "strength": ["Jump squats", "Push-ups", "Core twists", "Box jumps"],
            "skills": ["Layup drills", "Ball handling drills", "3-point shooting"],
            "cooldown": ["Shoulder stretch", "Hip stretch", "Breathing exercises"]
        },

        "Cricket": {
            "warmup": ["Jogging laps", "Shoulder rotations", "Dynamic stretches"],
            "strength": ["Resistance band training", "Core plank", "Lunges", "Push-ups"],
            "skills": ["Batting nets", "Bowling accuracy drills", "Fielding practice"],
            "cooldown": ["Shoulder stretch", "Hamstring stretch", "Light walking"]
        },

        "Tennis": {
            "warmup": ["Skipping rope", "Side shuffles", "Dynamic stretches"],
            "strength": ["Core plank", "Lunges", "Medicine ball throws", "Squats"],
            "skills": ["Serve practice", "Footwork ladder", "Rally drills"],
            "cooldown": ["Forearm stretch", "Leg stretch", "Deep breathing"]
        }
    }

    sport_plan = workouts[sport]

    injury_tip = ""
    if injury != "None":
        injury_tip = f"⚠ Reduce high-impact drills to protect your {injury.lower()}."

    return f"""
Warm-up: {random.choice(sport_plan['warmup'])}
Strength: {random.choice(sport_plan['strength'])}
Skill Drill: {random.choice(sport_plan['skills'])}
Cooldown: {random.choice(sport_plan['cooldown'])}

{injury_tip}
"""

# -------------------------
# Weekly Schedule Generator
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
def strategy(opponent):
    if opponent == "Weak":
        return "Play aggressively and experiment with new tactics."
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
opponent = st.selectbox("Opponent Strength", ["Weak", "Average", "Strong"])
st.write(strategy(opponent))
