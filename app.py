import streamlit as st
from datetime import datetime
import random
import pandas as pd
from PIL import Image, ImageDraw

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="MedTimer - Daily Medicine Companion",
    layout="wide"
)

st.title("💊 MedTimer – Daily Medicine Companion")
st.write("A calm, friendly app to help you stay consistent with your medicines.")

# -----------------------------
# Session State
# -----------------------------
if "medicines" not in st.session_state:
    st.session_state.medicines = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "badges" not in st.session_state:
    st.session_state.badges = set()

# -----------------------------
# Utility Functions
# -----------------------------
def get_status(med_time, taken):
    now = datetime.now().time()
    if taken:
        return "Taken"
    elif now < med_time:
        return "Upcoming"
    else:
        return "Missed"

def calculate_adherence():
    if not st.session_state.medicines:
        return 0
    taken = sum(1 for m in st.session_state.medicines if m["taken"])
    return int((taken / len(st.session_state.medicines)) * 100)

def update_streak(medicines):
    if not medicines:
        return

    all_taken = all(med["taken"] for med in medicines)

    if all_taken:
        st.session_state.streak += 1
    else:
        if st.session_state.streak > 0:
            st.warning("⚠️ Streak reset. No worries — tomorrow is a fresh start!")
        st.session_state.streak = 0

def check_badges(score):
    streak = st.session_state.streak

    if streak >= 1:
        st.session_state.badges.add("🥉 First Step – All medicines taken today")

    if streak >= 3:
        st.session_state.badges.add("🥈 3-Day Streak – Consistency is building")

    if streak >= 7:
        st.session_state.badges.add("🥇 7-Day Champion – Perfect weekly streak")

    if score == 100:
        st.session_state.badges.add("💯 Perfect Day – 100% adherence")

    if score >= 90:
        st.session_state.badges.add("🔥 Consistency King – Above 90% adherence")

def generate_csv():
    data = []
    for med in st.session_state.medicines:
        data.append({
            "Medicine Name": med["name"],
            "Scheduled Time": med["time"].strftime("%H:%M"),
            "Taken": "Yes" if med["taken"] else "No"
        })
    return pd.DataFrame(data)

def draw_reward_image():
    img = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(img)

    draw.ellipse((50, 50, 250, 250), outline="green", width=6)
    draw.ellipse((110, 120, 130, 140), fill="black")
    draw.ellipse((170, 120, 190, 140), fill="black")
    draw.arc((110, 150, 190, 220), start=0, end=180, fill="green", width=5)

    return img

# -----------------------------
# Tips & Motivation
# -----------------------------
health_tips = [
    "💡 Keep medicines near your toothbrush to remember morning doses.",
    "💡 Set alarms along with this app for better consistency.",
    "💡 Taking medicines at the same time daily builds a strong habit.",
    "💡 Never skip doses unless advised by a doctor.",
    "💡 Small habits today lead to better health tomorrow."
]

def get_motivation(score):
    if score == 100:
        return "🏆 Perfect adherence! Outstanding discipline."
    elif score >= 80:
        return "🌟 Great job! You’re taking excellent care of yourself."
    elif score >= 50:
        return "💪 Keep pushing. Consistency is key."
    else:
        return "🌱 Every day is a new chance to do better."

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("🌈 Daily Companion")
st.sidebar.info(random.choice(health_tips))
st.sidebar.write("🌙 You can switch to Dark Mode from app settings for night use.")

# -----------------------------
# Add Medicine
# -----------------------------
st.header("➕ Add Medicine")

with st.form("medicine_form"):
    name = st.text_input("Medicine Name")
    med_time = st.time_input("Scheduled Time")
    add = st.form_submit_button("Add Medicine")

    if add and name:
        st.session_state.medicines.append({
            "name": name,
            "time": med_time,
            "taken": False
        })
        st.success("Medicine added successfully!")

# -----------------------------
# Medicine Checklist
# -----------------------------
st.header("📋 Today's Medicine Checklist")

if not st.session_state.medicines:
    st.info("No medicines added yet.")
else:
    for i, med in enumerate(st.session_state.medicines):
        status = get_status(med["time"], med["taken"])

        c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
        c1.write(f"**{med['name']}**")
        c2.write(med["time"].strftime("%H:%M"))

        if status == "Taken":
            c3.success("🟢 Taken")
        elif status == "Upcoming":
            c3.warning("🟡 Upcoming")
        else:
            c3.error("🔴 Missed")

        if c4.button("Mark as Taken", key=f"taken_{i}"):
            st.session_state.medicines[i]["taken"] = True
            st.rerun()

# -----------------------------
# Adherence & Streak
# -----------------------------
st.header("📊 Adherence & Streak")

score = calculate_adherence()
update_streak(st.session_state.medicines)
check_badges(score)

st.progress(score)
st.write(f"**Adherence: {score}%**")
st.write(f"🔥 **Current Streak:** {st.session_state.streak} day(s)")

st.write(get_motivation(score))

if score >= 80:
    st.image(draw_reward_image(), caption="🎉 Keep up the great work!")

if st.session_state.streak == 7:
    st.balloons()

# -----------------------------
# Badges
# -----------------------------
st.header("🏆 Achievements & Badges")

if st.session_state.badges:
    for badge in st.session_state.badges:
        st.success(badge)
else:
    st.info("No badges yet. Stay consistent to unlock rewards!")

# -----------------------------
# Download Report
# -----------------------------
st.header("⬇️ Download Medicine Report")

if st.session_state.medicines:
    df = generate_csv()
    st.download_button(
        label="Download CSV Report",
        data=df.to_csv(index=False),
        file_name="medtimer_report.csv",
        mime="text/csv"
    )

# -----------------------------
# Feedback
# -----------------------------
st.header("📝 User Feedback")

with st.form("feedback_form"):
    feedback = st.text_area("Share your thoughts or suggestions")
    submit = st.form_submit_button("Submit Feedback")

    if submit and feedback:
        st.success("Thank you for your feedback! 💙")
