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
position = st.text_input("Position (example: defender, striker, goalkeeper)")
age_group = st.selectbox("Age Group", ["13-15", "16-18"])
fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
days = st.slider("Training days per week", 1, 7, 3)
injury = st.selectbox("Injury Risk Area", ["None", "Knee", "Ankle", "Shoulder"])

st.divider()

# -------------------------
# Sport + Position Workout Generator
# -------------------------
def generate_workout():

    workouts = {

        "Football": {
            "attacker": {
                "strength": ["Jump squats", "Lunges", "Core plank"],
                "skills": ["Shooting practice", "Dribbling cones", "Finishing drills"]
            },
            "midfielder": {
                "strength": ["Squats", "Core plank", "Endurance running"],
                "skills": ["Passing drills", "Ball control", "Vision drills"]
            },
            "defender": {
                "strength": ["Heavy squats", "Lunges", "Core stability"],
                "skills": ["Tackling drills", "Marking practice", "Heading practice"]
            },
            "goalkeeper": {
                "strength": ["Core plank", "Medicine ball throws", "Jump squats"],
                "skills": ["Diving drills", "Reaction training", "Catching drills"]
            }
        },

        "Basketball": {
            "default": {
                "strength": ["Box jumps", "Push-ups", "Core twists"],
                "skills": ["Layups", "Dribbling drills", "3-point shooting"]
            }
        },

        "Cricket": {
            "default": {
                "strength": ["Resistance band training", "Core plank", "Lunges"],
                "skills": ["Batting nets", "Bowling practice", "Fielding drills"]
            }
        },

        "Tennis": {
            "default": {
                "strength": ["Lunges", "Squats", "Core plank"],
                "skills": ["Serve practice", "Footwork ladder", "Rally drills"]
            }
        }
    }

    warmups = ["Light jogging", "Skipping rope", "Dynamic stretching"]
    cooldowns = ["Stretching", "Foam rolling", "Breathing exercises"]

    pos = position.lower()

    if sport == "Football":
        if "def" in pos:
            role = "defender"
        elif "mid" in pos:
            role = "midfielder"
        elif "goal" in pos:
            role = "goalkeeper"
        else:
            role = "attacker"
    else:
        role = "default"

    sport_plan = workouts[sport][role]

    injury_tip = ""
    if injury != "None":
        injury_tip = f"⚠ Reduce high-impact drills to protect your {injury.lower()}."

    return f"""
Warm-up: {random.choice(warmups)}
Strength Focus: {random.choice(sport_plan['strength'])}
Skill Drill: {random.choice(sport_plan['skills'])}
Cooldown: {random.choice(cooldowns)}

{injury_tip}
"""

# -------------------------
# Sport-Specific Weekly Schedule
# -------------------------
def generate_schedule():

    schedules = {
        "Football": [
            "Speed & Sprint Training",
            "Strength & Conditioning",
            "Ball Control & Passing",
            "Match Simulation",
            "Recovery & Mobility"
        ],
        "Basketball": [
            "Vertical Jump Training",
            "Ball Handling",
            "Strength Training",
            "Shooting Practice",
            "Recovery & Stretching"
        ],
        "Cricket": [
            "Batting Practice",
            "Bowling & Shoulder Strength",
            "Fielding Drills",
            "Endurance Training",
            "Recovery Session"
        ],
        "Tennis": [
            "Footwork & Agility",
            "Serve Practice",
            "Strength Training",
            "Match Simulation",
            "Mobility & Stretching"
        ]
    }

    chosen = schedules[sport]
    plan = ""
    for i in range(days):
        plan += f"Day {i+1}: {random.choice(chosen)}\n"
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
