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
