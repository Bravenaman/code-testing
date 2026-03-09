import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Mission Control Dashboard",
    page_icon="🚀",
    layout="wide"
)

# CSS Styling (Background + Glass Panel)
st.markdown("""
<style>

.stApp {
    background-image: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Glass overlay panel */
.login-box {
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(12px);
    padding: 50px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0px 0px 35px rgba(0,0,0,0.7);
}

/* Make text white */
h1, h2, h3, p, label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# Session state
if "commander" not in st.session_state:
    st.session_state.commander = None


# ENTRY SCREEN
if st.session_state.commander is None:

    # Center layout
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


# MAIN DASHBOARD (placeholder for now)
else:

    st.success(f"Welcome Commander {st.session_state.commander}")

    st.title("🚀 Rocket Mission Dashboard")

    st.write("Mission systems online. Analytics loading...")
    
import numpy as np
import pandas as pd
import plotly.express as px


# ----------------------------
# SESSION STATE
# ----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ----------------------------
# LOGIN SCREEN
# ----------------------------

if not st.session_state.logged_in:

    st.title("🚀 Mission Control Login")

    username = st.text_input("Commander Name")
    password = st.text_input("Access Code", type="password")

    if st.button("Enter Mission Control"):

        if username != "" and password != "":
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Please enter credentials")


# ----------------------------
# MAIN APPLICATION
# ----------------------------

else:

    st.sidebar.title("👨‍🚀 Commander")

    st.sidebar.write("Rank: LVL 1")
    st.sidebar.progress(0.25)

    st.sidebar.write("XP: 50 / 200")
    st.sidebar.write("Level Goal: Reach 15000m")

    if st.sidebar.button("Abort Mission (Logout)"):
        st.session_state.logged_in = False
        st.rerun()


    st.title("🚀 Space Mission Control")


    tab1, tab2, tab3 = st.tabs(
        ["🚀 Launch Sim", "📊 Mission Analytics", "🏆 Achievements"]
    )


    # ----------------------------
    # TAB 1 — LAUNCH SIMULATOR
    # ----------------------------

    with tab1:

        st.header("Level 1 Simulator: Flight Cadet")

        st.write(
            "MISSION: Adjust parameters to break the altitude target of **15000 meters**!"
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
                st.warning("Mission Failed — Try adjusting parameters.")


    # ----------------------------
    # TAB 2 — MISSION ANALYTICS
    # ----------------------------

    with tab2:

        st.header("Historical Mission Data")

        payload_data = np.random.rand(200) * 100
        fuel_data = np.random.rand(200) * 5000

        df1 = pd.DataFrame({
            "Payload Weight": payload_data,
            "Fuel Consumption": fuel_data
        })

        fig1 = px.scatter(
            df1,
            x="Payload Weight",
            y="Fuel Consumption",
            title="Payload vs Fuel Consumption"
        )

        st.plotly_chart(fig1, use_container_width=True)


        success = np.random.rand(200) * 30 + 70
        cost = np.random.rand(200) * 300

        df2 = pd.DataFrame({
            "Mission Success": success,
            "Mission Cost": cost
        })

        fig2 = px.scatter(
            df2,
            x="Mission Success",
            y="Mission Cost",
            title="Mission Success vs Mission Cost"
        )

        st.plotly_chart(fig2, use_container_width=True)


    # ----------------------------
    # TAB 3 — ACHIEVEMENTS
    # ----------------------------

    with tab3:

        st.header("🏆 Achievements")

        st.write("🚀 First Launch")
        st.write("🔥 Break 15000m Altitude")
        st.write("⛽ Fuel Efficiency Expert")
        st.write("🛰 Payload Master")
        st.write("🏅 Elite Commander")
