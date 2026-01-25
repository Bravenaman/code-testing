import streamlit as st
from datetime import datetime
import random
import pandas as pd
from PIL import Image, ImageDraw

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="MedTimer – Daily Medicine Companion",
    layout="wide"
)

st.title("💊 MedTimer – Daily Medicine Companion")
st.write("A friendly app that helps you stay consistent with your daily medicines.")

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
if "medicines" not in st.session_state:
    st.session_state.medicines = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "badges" not in st.session_state:
    st.session_state.badges = set()

# -------------------------------------------------
# Utility Functions
# -------------------------------------------------
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

def update_streak():
    if not st.session_state.medicines:
        return

    all_taken = all(m["taken"] for m in st.session_state.medicines)

    if all_taken:
        st.session_state.streak += 1
    else:
        if st.session_state.streak > 0:
            st.warning("⚠️ Streak reset. Tomorrow is a fresh start!")
        st.session_state.streak = 0

def check_badges(score):
    streak = st.session_state.streak
    badges = st.session_state.badges

    if streak >= 1:
        badges.add("🥉 First Step – All medicines taken today")
    if streak >= 3:
        badges.add("🥈 3-Day Streak – Consistency is building")
    if streak >= 7:
        badges.add("🥇 7-Day Champion – Perfect weekly streak")
    if score == 100:
        badges.add("💯 Perfect Day – 100% adherence")
    if score >= 90:
        badges.add("🔥 Consistency King – Above 90% adherence")

def draw_reward_image():
    img = Image.new("RGB", (250, 250), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((40, 40, 210, 210), outline="green", width=6)
    draw.ellipse((90, 100, 110, 120), fill="black")
    draw.ellipse((140, 100, 160, 120), fill="black")
    draw.arc((90, 130, 160, 190), 0, 180, fill="green", width=5)
    return img

# -------------------------------------------------
# Sidebar (Tips)
# -------------------------------------------------
tips = [
    "💡 Keep medicines near your toothbrush to remember morning doses.",
    "💡 Use alarms along with this app for better reminders.",
    "💡 Consistency builds habits faster than motivation.",
    "💡 Never skip medicines unless advised by a doctor."
]

st.sidebar.header("🌈 Daily Companion")
st.sidebar.info(random.choice(tips))
st.sidebar.info("🌙 Switch to Dark Mode from app settings for night use.")

# -------------------------------------------------
# Add Medicine
# -------------------------------------------------
st.header("➕ Add Medicine")

with st.form("add_medicine_form"):
    name = st.text_input("Medicine Name")
    time = st.time_input("Scheduled Time")
    submit = st.form_submit_button("Add Medicine")

    if submit and name:
        st.session_state.medicines.append({
            "name": name,
            "time": time,
            "taken": False
        })
        st.success("Medicine added successfully!")

# -------------------------------------------------
# Medicine Checklist
# -------------------------------------------------
st.header("📋 Today’s Medicine Checklist")

if not st.session_state.medicines:
    st.info("No medicines added yet.")
else:
    for i, med in enumerate(st.session_state.medicines):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
        c1.write(f"**{med['name']}**")
        c2.write(med["time"].strftime("%H:%M"))

        status = get_status(med["time"], med["taken"])

        if status == "Taken":
            c3.success("🟢 Taken")
        elif status == "Upcoming":
            c3.warning("🟡 Upcoming")
        else:
            c3.error("🔴 Missed")

        if c4.button("Mark as Taken", key=f"take_{i}"):
            st.session_state.medicines[i]["taken"] = True
            st.rerun()

# -------------------------------------------------
# Progress Overview
# -------------------------------------------------
st.header("📊 Progress Overview")

score = calculate_adherence()
st.progress(score)
st.write(f"**Adherence Score:** {score}%")

update_streak()
check_badges(score)

st.write(f"🔥 **Current Streak:** {st.session_state.streak} day(s)")

# -------------------------------------------------
# Motivational Tips (FIXED & ALWAYS VISIBLE)
# -------------------------------------------------
st.subheader("🌟 Motivational Tips")

if score == 100:
    st.success("🏆 Perfect day! You didn’t miss a single dose.")
elif score >= 80:
    st.success("🌟 Great consistency! Keep it up.")
elif score >= 50:
    st.warning("🙂 You’re doing okay. Try to stay consistent.")
else:
    st.error("💙 Tough day. Tomorrow is a fresh start.")

if score >= 80:
    st.image(draw_reward_image(), caption="🎉 Keep going!")

# -------------------------------------------------
# Achievements & Badges
# -------------------------------------------------
st.header("🏆 Achievements & Badges")

if st.session_state.badges:
    for badge in st.session_state.badges:
        st.success(badge)
else:
    st.info("No badges earned yet. Stay consistent to unlock rewards!")

if st.session_state.streak == 7:
    st.balloons()

# -------------------------------------------------
# Feedback Form
# -------------------------------------------------
st.header("📝 User Feedback")

with st.form("feedback_form"):
    feedback = st.text_area("Share your thoughts about MedTimer")
    send = st.form_submit_button("Submit Feedback")

    if send and feedback:
        st.success("Thank you for your feedback! 💙")

# -------------------------------------------------
# Download Report
# -------------------------------------------------
st.header("⬇️ Download Medicine Report")

if st.session_state.medicines:
    df = pd.DataFrame([
        {
            "Medicine": m["name"],
            "Time": m["time"].strftime("%H:%M"),
            "Taken": "Yes" if m["taken"] else "No"
        }
        for m in st.session_state.medicines
    ])

    st.download_button(
        "Download CSV Report",
        df.to_csv(index=False),
        "medtimer_report.csv",
        "text/csv"
    )
