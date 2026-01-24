import streamlit as st
from datetime import datetime, date
from PIL import Image, ImageDraw
import pandas as pd
import random

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="MedTimer – Daily Medicine Companion",
    layout="wide"
)

st.title("💊 MedTimer – Daily Medicine Companion")
st.write("A calm, friendly companion to help you manage your daily medicines with confidence.")

# ---------------------------------
# Session State
# ---------------------------------
if "medicines" not in st.session_state:
    st.session_state.medicines = []

# ---------------------------------
# Tips, Motivation & Suggestions
# ---------------------------------
health_tips = [
    "💡 Keep medicines near your toothbrush to remember morning doses.",
    "💡 Taking medicines at the same time daily builds a strong habit.",
    "💡 Use alarms along with this app for extra reminders.",
    "💡 Never skip doses unless advised by your doctor.",
    "💡 Store medicines in a visible and safe place."
]

def get_random_tip():
    return random.choice(health_tips)

def get_suggestion(score):
    if score >= 80:
        return "🌟 You're doing great! Keep following your routine."
    elif score >= 50:
        return "🙂 You're on track, but try not to miss any doses."
    else:
        return "⚠️ Consider setting reminders or adjusting your schedule."

def get_motivation(score):
    if score == 100:
        return "🏆 Perfect score! Your consistency is inspiring."
    elif score >= 80:
        return "🔥 Amazing effort! You're taking great care of your health."
    elif score >= 50:
        return "💪 Keep going! Small improvements matter."
    else:
        return "🌱 Every day is a new chance. You’ve got this!"

# ---------------------------------
# Helper Functions
# ---------------------------------
def get_status(med):
    now = datetime.now()
    scheduled = datetime.combine(med["date"], med["time"])

    if med["taken"]:
        return "Taken", "green"
    elif now < scheduled:
        return "Upcoming", "orange"
    else:
        return "Missed", "red"

def calculate_adherence():
    if not st.session_state.medicines:
        return 0
    taken = sum(1 for m in st.session_state.medicines if m["taken"])
    return int((taken / len(st.session_state.medicines)) * 100)

def draw_reward_image():
    img = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(img)

    draw.ellipse((50, 50, 250, 250), outline="green", width=6)
    draw.ellipse((110, 120, 130, 140), fill="black")
    draw.ellipse((170, 120, 190, 140), fill="black")
    draw.arc((110, 150, 190, 220), start=0, end=180, fill="green", width=5)

    return img

def generate_report():
    data = []
    for med in st.session_state.medicines:
        status, _ = get_status(med)
        data.append({
            "Medicine Name": med["name"],
            "Scheduled Time": med["time"].strftime("%H:%M"),
            "Date": med["date"].strftime("%Y-%m-%d"),
            "Status": status,
            "Taken": "Yes" if med["taken"] else "No"
        })
    return pd.DataFrame(data)

# ---------------------------------
# Sidebar (Colour + Tips)
# ---------------------------------
st.sidebar.header("🌈 Daily Companion")
st.sidebar.write("Your health matters every day 💙")
st.sidebar.info(get_random_tip())

# ---------------------------------
# Add Medicine
# ---------------------------------
st.header("➕ Add a Medicine")

with st.form("add_medicine_form"):
    name = st.text_input("Medicine Name")
    med_time = st.time_input("Scheduled Time")
    add = st.form_submit_button("Add Medicine")

    if add and name:
        st.session_state.medicines.append({
            "name": name,
            "time": med_time,
            "taken": False,
            "date": date.today()
        })
        st.success("Medicine added successfully!")

# ---------------------------------
# Medicine Checklist
# ---------------------------------
st.header("📋 Today's Medicine Checklist")

if not st.session_state.medicines:
    st.info("No medicines added yet.")
else:
    for i, med in enumerate(st.session_state.medicines):
        status, color = get_status(med)

        c1, c2, c3, c4 = st.columns([3, 2, 2, 3])

        c1.write(f"**{med['name']}**")
        c2.write(med["time"].strftime("%H:%M"))
        c3.markdown(
            f"<span style='color:{color}; font-weight:bold'>{status}</span>",
            unsafe_allow_html=True
        )

        b1, b2 = c4.columns(2)

        if b1.button("✅ Taken", key=f"taken_{i}"):
            st.session_state.medicines[i]["taken"] = True
            st.rerun()

        if b2.button("❌ Delete", key=f"delete_{i}"):
            st.session_state.medicines.pop(i)
            st.rerun()

# ---------------------------------
# Adherence, Motivation & Suggestions
# ---------------------------------
st.header("📊 Weekly Adherence Score")

score = calculate_adherence()
st.progress(score / 100)
st.write(f"**Adherence: {score}%**")

st.success(get_suggestion(score))
st.write(get_motivation(score))

if score >= 80:
    st.image(draw_reward_image(), caption="🎉 Great consistency!")
    if score == 100:
        st.balloons()

# ---------------------------------
# Download Report
# ---------------------------------
st.header("⬇️ Download Medicine Report")

if st.session_state.medicines:
    df = generate_report()
    st.download_button(
        label="Download CSV Report",
        data=df.to_csv(index=False),
        file_name="medtimer_report.csv",
        mime="text/csv"
    )
else:
    st.info("Add medicines to generate a report.")

# ---------------------------------
# Feedback Form
# ---------------------------------
st.header("📝 User Feedback")

with st.form("feedback_form"):
    feedback = st.text_area("Share your thoughts or suggestions about MedTimer")
    submit_fb = st.form_submit_button("Submit Feedback")

    if submit_fb and feedback:
        st.success("Thank you for your feedback! 💙")
