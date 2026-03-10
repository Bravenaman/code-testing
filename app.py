import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Mission Control Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# COLORFUL UI STYLING
# -----------------------------------

st.markdown("""
<style>

.stApp {
background: linear-gradient(-45deg,#0f172a,#020617,#1e293b,#020617);
background-size: 400% 400%;
animation: gradientBG 20s ease infinite;
color:white;
}

@keyframes gradientBG {
0% {background-position:0% 50%;}
50% {background-position:100% 50%;}
100% {background-position:0% 50%;}
}

section[data-testid="stSidebar"] {
background: linear-gradient(180deg,#020617,#0f172a);
border-right:1px solid rgba(255,255,255,0.1);
}

.glass {
background: rgba(255,255,255,0.05);
border-radius:20px;
padding:25px;
backdrop-filter: blur(10px);
border:1px solid rgba(255,255,255,0.1);
box-shadow:0 8px 30px rgba(0,0,0,0.6);
}

.gradient-text {
font-size:40px;
font-weight:700;
background: linear-gradient(90deg,#38bdf8,#818cf8,#c084fc);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.stButton>button {
background: linear-gradient(90deg,#3b82f6,#8b5cf6);
color:white;
border:none;
padding:10px 25px;
border-radius:10px;
font-weight:600;
transition:0.3s;
}

.stButton>button:hover {
transform:scale(1.05);
box-shadow:0 0 15px rgba(99,102,241,0.8);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown('<div class="gradient-text">🚀 Rocket Mission Dashboard</div>', unsafe_allow_html=True)

st.write("Mission systems online. Adjust launch parameters and explore mission analytics.")

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.header("🚀 Mission Panel")

    st.progress(0.25)

    st.write("Simulation Ready")

    st.divider()

    st.write("Analytics Enabled")

# -----------------------------------
# TABS
# -----------------------------------

tab1, tab2, tab3 = st.tabs([
    "🚀 Launch Simulator",
    "📊 Mission Analytics",
    "📚 Data Exploration"
])

# -----------------------------------
# TAB 1 : LAUNCH SIMULATOR
# -----------------------------------

with tab1:

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.header("Level 1 Simulator: Flight Cadet")

    st.write("MISSION: Adjust parameters to break the altitude target of **15000 meters**")

    thrust = st.slider("Engine Thrust (N)", 1000000, 7000000, 4000000)

    fuel = st.slider("Fuel Mass (kg)", 10000, 200000, 100000)

    payload = st.slider("Payload Mass (kg)", 5000, 50000, 20000)

    def simulate(thrust, fuel, payload):

        time = np.linspace(0, 300, 120)

        acceleration = thrust / (fuel + payload + 50000)

        altitude = acceleration * time**1.5 * 50

        return time, altitude

    if st.button("🔥 IGNITION"):

        time, altitude = simulate(thrust, fuel, payload)

        df_launch = pd.DataFrame({
            "Time (s)": time,
            "Altitude (m)": altitude
        })

        fig = px.line(
            df_launch,
            x="Time (s)",
            y="Altitude (m)",
            title="Flight Path Trajectory"
        )

        fig.add_hline(
            y=15000,
            line_dash="dash",
            line_color="red",
            annotation_text="Target Altitude"
        )

        st.plotly_chart(fig, use_container_width=True)

        if altitude.max() > 15000:
            st.success("🎉 Mission Success! Target altitude reached.")
        else:
            st.warning("Mission Failed — Adjust parameters and try again.")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------
# TAB 2 : MISSION ANALYTICS
# -----------------------------------

with tab2:

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.header("Mission Analytics")

    np.random.seed(42)

    missions = 200

    payload = np.random.randint(5000, 50000, missions)
    fuel = payload * np.random.uniform(0.05, 0.15, missions)

    mission_cost = np.random.randint(50, 300, missions)
    mission_result = np.random.choice(["Success", "Failure"], missions)

    mission_duration = np.random.randint(5, 40, missions)
    distance = mission_duration * np.random.uniform(20000, 60000, missions)

    crew_size = np.random.randint(1, 8, missions)
    success_percent = np.random.uniform(60, 98, missions)

    scientific_yield = np.random.randint(10, 100, missions)

    df = pd.DataFrame({
        "Payload Weight": payload,
        "Fuel Consumption": fuel,
        "Mission Cost": mission_cost,
        "Mission Result": mission_result,
        "Mission Duration": mission_duration,
        "Distance from Earth": distance,
        "Crew Size": crew_size,
        "Mission Success %": success_percent,
        "Scientific Yield": scientific_yield
    })

    fig1 = px.scatter(df, x="Payload Weight", y="Fuel Consumption", color="Mission Result")
    st.plotly_chart(fig1, use_container_width=True)

    cost_df = df.groupby("Mission Result")["Mission Cost"].mean().reset_index()
    fig2 = px.bar(cost_df, x="Mission Result", y="Mission Cost", color="Mission Result")
    st.plotly_chart(fig2, use_container_width=True)

    duration_df = df.sort_values("Mission Duration")
    fig3 = px.line(duration_df, x="Mission Duration", y="Distance from Earth")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.box(df, x="Crew Size", y="Mission Success %")
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.scatter(df, x="Mission Cost", y="Scientific Yield", color="Crew Size")
    st.plotly_chart(fig5, use_container_width=True)

    corr = df.corr(numeric_only=True).round(2)
    fig_heatmap = px.imshow(corr, text_auto=True, color_continuous_scale="viridis")

    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------
# TAB 3 : DATA EXPLORATION
# -----------------------------------

with tab3:

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.header("📚 Data Exploration: Physics Behind Rocket Launches")

    st.write("""
Rocket launches follow **Newton’s Second Law of Motion**:

**Force = Mass × Acceleration**

In rockets, the main upward force is **thrust**, while forces like **drag** and the **weight of the payload** resist motion.
Understanding how these variables interact helps scientists design efficient launch systems.
""")

    st.subheader("🚀 Thrust")
    st.write("""
Thrust is the force produced by rocket engines when fuel burns and exhaust gases are expelled at extremely high speeds.  
This force pushes the rocket upward against gravity.  
Large launch vehicles produce millions of Newtons of thrust to lift spacecraft into orbit.
""")

    st.subheader("📦 Payload")
    st.write("""
Payload is the cargo a rocket carries into space.  
This can include satellites, scientific instruments, astronauts, or supplies.

Heavier payloads increase the rocket’s total mass, which reduces acceleration unless additional thrust is provided.
""")

    st.subheader("🌬 Drag")
    st.write("""
Drag is air resistance that slows objects moving through the atmosphere.

During launch, rockets must push through dense air near Earth’s surface.  
As altitude increases, the atmosphere becomes thinner, reducing drag and allowing the rocket to accelerate faster.
""")

    st.subheader("Guiding Questions")

    st.write("""
**1. How does adding more payload affect altitude?**

Ans. Adding payload increases total mass. If thrust remains constant, acceleration decreases, meaning the rocket climbs slower and may not reach the same altitude.

**2. How does increasing thrust affect launch success?**

Ans. Higher thrust increases upward force. If thrust exceeds gravity and drag, the rocket accelerates upward more effectively and can carry heavier payloads.

**3. Does lower drag at higher altitudes improve speed?**

Ans. Yes. Thinner atmosphere means less resistance, allowing rockets to reach higher speeds more efficiently.

**4. How long would it take to reach orbit?**

Ans. Most rockets reach orbit in about **8–10 minutes** after launch. They must reach speeds around **7.8 km/s** to stay in low Earth orbit.

**5. Can simulation values be compared with real missions?**

Ans. Yes. Engineers often use simulations to test rocket performance before real launches. While simplified models do not include every factor, they demonstrate the core physics behind real aerospace engineering.
""")

    st.markdown('</div>', unsafe_allow_html=True)
