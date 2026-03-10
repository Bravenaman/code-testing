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
# CSS STYLING
# -----------------------------------

st.markdown("""
<style>

/* BLACK BACKGROUND */

.stApp {
    background-color: #000000;
}

/* Glass login panel */

.login-box {
    background: rgba(0,0,0,0.75);
    backdrop-filter: blur(12px);
    padding: 50px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0px 0px 35px rgba(0,0,0,0.7);
}

/* White text */

h1, h2, h3, p, label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "commander" not in st.session_state:
    st.session_state.commander = None


# -----------------------------------
# ENTRY / LOGIN SCREEN
# -----------------------------------

if st.session_state.commander is None:

    col1, col2, col3 = st.columns([2,3,2])

    with col2:

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        st.title("🚀 Mission Control")

        st.subheader("Rocket Launch Visualization System")

        st.write("Enter your Commander Name to access the system")

        commander_name = st.text_input("Commander Name")

        if st.button("Launch Dashboard"):

            if commander_name != "":
                st.session_state.commander = commander_name
                st.rerun()

            else:
                st.warning("Please enter a commander name")

        st.caption("Authorized Personnel Only")

        st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------
# MAIN DASHBOARD
# -----------------------------------

else:

    st.success(f"Welcome Commander {st.session_state.commander}")

    st.title("🚀 Rocket Mission Dashboard")

    st.write("Mission systems online. Analytics ready.")


# -----------------------------------
# SIDEBAR COMMAND PANEL
# -----------------------------------

    with st.sidebar:

        st.header(f"👨‍🚀 Cmdr. {st.session_state.commander}")

        st.markdown("**Rank: LVL 1**")

        st.progress(0.25)

        st.write("XP: 50 / 200")

        st.write("Level Goal: Reach 15000m")

        st.divider()

        if st.button("Abort Mission (Logout)"):
            st.session_state.commander = None
            st.rerun()


# -----------------------------------
# MAIN TABS
# -----------------------------------

    tab1, tab2, tab3 = st.tabs([
        "🚀 Launch Sim",
        "📊 Mission Analytics",
        "🏆 Achievements"
    ])


# -----------------------------------
# TAB 1 : LAUNCH SIMULATOR
# -----------------------------------

    with tab1:

        st.header("Level 1 Simulator: Flight Cadet")

        st.write(
            "MISSION: Adjust parameters to break the altitude target of **15000 meters**"
        )

        st.subheader("Flight Parameters")

        thrust = st.slider(
            "Engine Thrust (N)",
            1000000,
            7000000,
            4000000
        )

        fuel = st.slider(
            "Fuel Mass (kg)",
            10000,
            200000,
            100000
        )

        payload = st.slider(
            "Payload Mass (kg)",
            5000,
            50000,
            20000
        )


        def simulate(thrust, fuel, payload):

            time = np.linspace(0, 300, 120)

            acceleration = thrust / (fuel + payload + 50000)

            altitude = acceleration * time**1.5 * 50

            return time, altitude


        if st.button("🔥 IGNITION"):

            time, altitude = simulate(thrust, fuel, payload)

            df = pd.DataFrame({
                "Time (s)": time,
                "Altitude (m)": altitude
            })

            fig = px.line(
                df,
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


# -----------------------------------
# TAB 2 : MISSION ANALYTICS
# -----------------------------------

    with tab2:

         st.header("📊 Mission Analytics")

    st.write("Historical mission analysis and performance metrics")

    import plotly.express as px
    import numpy as np
    import pandas as pd

    # Generate synthetic dataset
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


    # --------------------------------
    # 1. SCATTER PLOT
    # Payload vs Fuel
    # --------------------------------

    st.subheader("Payload Weight vs Fuel Consumption")

    fig1 = px.scatter(
        df,
        x="Payload Weight",
        y="Fuel Consumption",
        color="Mission Result",
        title="Payload vs Fuel Consumption"
    )

    st.plotly_chart(fig1, use_container_width=True)


    # --------------------------------
    # 2. BAR CHART
    # Mission Cost Success vs Failure
    # --------------------------------

    st.subheader("Mission Cost: Success vs Failure")

    cost_df = df.groupby("Mission Result")["Mission Cost"].mean().reset_index()

    fig2 = px.bar(
        cost_df,
        x="Mission Result",
        y="Mission Cost",
        color="Mission Result",
        title="Average Mission Cost by Outcome"
    )

    st.plotly_chart(fig2, use_container_width=True)


    # --------------------------------
    # 3. LINE CHART
    # Duration vs Distance
    # --------------------------------

    st.subheader("Mission Duration vs Distance from Earth")

    duration_df = df.sort_values("Mission Duration")

    fig3 = px.line(
        duration_df,
        x="Mission Duration",
        y="Distance from Earth",
        title="Mission Duration vs Distance"
    )

    st.plotly_chart(fig3, use_container_width=True)


    # --------------------------------
    # 4. BOX PLOT
    # Crew Size vs Success %
    # --------------------------------

    st.subheader("Crew Size vs Mission Success %")

    fig4 = px.box(
        df,
        x="Crew Size",
        y="Mission Success %",
        title="Crew Size vs Mission Success Rate"
    )

    st.plotly_chart(fig4, use_container_width=True)


    # --------------------------------
    # 5. SCATTER PLOT
    # Scientific Yield vs Mission Cost
    # --------------------------------

    st.subheader("Scientific Yield vs Mission Cost")

    fig5 = px.scatter(
        df,
        x="Mission Cost",
        y="Scientific Yield",
        color="Crew Size",
        title="Scientific Yield vs Mission Cost"
    )

    st.plotly_chart(fig5, use_container_width=True)
# -----------------------------------
# TAB 3 : ACHIEVEMENTS
# -----------------------------------

    with tab3:

        st.header("🏆 Achievements")

        st.write("🚀 First Launch")

        st.write("🔥 Break 15000m Altitude")

        st.write("⛽ Fuel Efficiency Expert")

        st.write("🛰 Payload Master")

        st.write("🏅 Elite Commander")
