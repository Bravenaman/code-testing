import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Mission Control Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------
# CSS Styling
# ---------------------------
st.markdown("""
<style>

.stApp {
    background-image: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.login-box {
    background: rgba(0,0,0,0.75);
    backdrop-filter: blur(12px);
    padding: 50px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0px 0px 35px rgba(0,0,0,0.7);
}

h1, h2, h3, p, label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Session State
# ---------------------------
if "commander" not in st.session_state:
    st.session_state.commander = None


# ---------------------------
# LOGIN SCREEN
# ---------------------------
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


# ---------------------------
# MAIN DASHBOARD
# ---------------------------
else:

    st.success(f"Welcome Commander {st.session_state.commander}")

    st.title("🚀 Rocket Mission Dashboard")

    # ---------------------------
    # Load Dataset
    # ---------------------------
    df = pd.read_csv("rocket_missions.csv")

    st.subheader("📂 Mission Dataset Preview")
    st.dataframe(df.head())


    # ---------------------------
    # Sidebar Filters
    # ---------------------------
    st.sidebar.header("🔎 Filter Missions")

    mission_type = st.sidebar.selectbox(
        "Select Mission Type",
        df["Mission Type"].unique()
    )

    filtered_df = df[df["Mission Type"] == mission_type]

    st.write(f"Showing missions for: **{mission_type}**")


    # ---------------------------
    # Visualization 1
    # Payload vs Fuel
    # ---------------------------
    st.subheader("🚀 Payload Weight vs Fuel Consumption")

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=filtered_df,
        x="Payload Weight",
        y="Fuel Consumption",
        hue="Mission Success",
        ax=ax
    )

    ax.set_title("Payload vs Fuel Usage")

    st.pyplot(fig)
