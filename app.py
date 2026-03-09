import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="Rocket Mission Simulator", layout="wide")

# ---------- SPACE BACKGROUND ----------

page_bg = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa");
background-size: cover;
background-position: center;
}

[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}

[data-testid="stSidebar"]{
background: rgba(0,0,0,0.7);
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------- SESSION STATE ----------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "missions" not in st.session_state:
    st.session_state.missions = []

if "user" not in st.session_state:
    st.session_state.user = ""

# ---------- LOGIN ----------

if not st.session_state.logged_in:

    st.title("🚀 Mission Control")

    username = st.text_input("Enter Commander Name")

    if st.button("Enter Mission Control"):

        if username != "":
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()

        else:
            st.warning("Please enter your name")

# ---------- MAIN APP ----------

else:

    xp = st.session_state.xp
    level = xp // 200 + 1

    st.sidebar.title(f"👨‍🚀 Cmdr. {st.session_state.user}")
    st.sidebar.write(f"RANK: LVL {level}")
    st.sidebar.progress((xp % 200)/200)
    st.sidebar.write(f"XP: {xp}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs([
        "🚀 Launch Simulator",
        "📊 Mission Analytics",
        "🏆 Achievements"
    ])

# ---------- PHYSICS MODEL ----------

    def rocket_simulation(thrust, fuel_mass, payload_mass):

        g = 9.81
        mass = fuel_mass + payload_mass

        acceleration = (thrust / mass) - g

        time_values = np.linspace(0, 300, 100)

        altitude = 0.5 * acceleration * time_values**2

        altitude[altitude < 0] = 0

        return time_values, altitude

# ---------- TAB 1: LAUNCH SIM ----------

    with tab1:

        st.title("Level 1 Simulator: Flight Cadet")
        st.write("Mission: Reach **15000 meters** altitude")

        col1, col2 = st.columns([1,2])

        with col1:

            st.subheader("Flight Parameters")

            thrust = st.slider("Engine Thrust (N)",1000000,8000000,4000000,step=100000)
            fuel = st.slider("Fuel Mass (kg)",20000,200000,100000,step=5000)
            payload = st.slider("Payload Mass (kg)",1000,50000,20000,step=1000)

            ignite = st.button("🔥 IGNITION")

        with col2:

            if ignite:

                st.info("🚀 Running flight simulation...")

                time_values, altitude = rocket_simulation(thrust,fuel,payload)

                results_df = pd.DataFrame({
                    "Time": time_values,
                    "Altitude": altitude
                })

                max_altitude = altitude.max()

                st.session_state.xp += 10

                if max_altitude > 15000:
                    st.session_state.xp += 50

                st.session_state.missions.append({
                    "thrust": thrust,
                    "fuel": fuel,
                    "payload": payload,
                    "altitude": max_altitude
                })

                fig = px.line(
                    results_df,
                    x="Time",
                    y="Altitude",
                    template="plotly_dark",
                    title="🚀 Rocket Flight Trajectory",
                    labels={
                        "Time": "Time (seconds)",
                        "Altitude": "Altitude (meters)"
                    }
                )

                fig.add_hline(
                    y=15000,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Target Altitude",
                    annotation_position="top right"
                )

                max_row = results_df.loc[results_df["Altitude"].idxmax()]

                fig.add_scatter(
                    x=[max_row["Time"]],
                    y=[max_row["Altitude"]],
                    mode="markers+text",
                    text=["🚀"],
                    textposition="top center",
                    marker=dict(size=18, color="cyan"),
                    showlegend=False
                )

                fig.update_layout(
                    height=500,
                    hovermode="x unified"
                )

                st.plotly_chart(fig, use_container_width=True)

                if max_altitude > 15000:
                    st.success("🚀 Target altitude reached!")
                else:
                    st.warning("Mission failed — adjust parameters")

# ---------- TAB 2 ANALYTICS ----------

    with tab2:

        st.header("Mission Analytics")

        if len(st.session_state.missions) == 0:
            st.write("No missions yet")

        else:

            df = pd.DataFrame(st.session_state.missions)

            st.dataframe(df)

            fig1, ax1 = plt.subplots()

            ax1.scatter(df["thrust"], df["altitude"])

            ax1.set_xlabel("Thrust")
            ax1.set_ylabel("Altitude")
            ax1.set_title("Thrust vs Altitude")

            st.pyplot(fig1)

# ---------- TAB 3 ACHIEVEMENTS ----------

    with tab3:

        st.header("Achievements")

        xp = st.session_state.xp

        if xp >= 10:
            st.success("🚀 First Launch")

        if xp >= 100:
            st.success("🛰 Mission Specialist")

        if xp >= 300:
            st.success("🌕 Orbital Commander")

        if xp >= 600:
            st.success("🌌 Deep Space Pilot")

        if xp < 10:
            st.write("No achievements yet")
