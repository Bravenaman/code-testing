import streamlit as st

st.set_page_config(page_title="Mission Control", page_icon="🚀", layout="wide")

# Background styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa");
        background-size: cover;
        background-position: center;
    }

    .login-box {
        background: rgba(0,0,0,0.6);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session state
if "commander" not in st.session_state:
    st.session_state.commander = None


if st.session_state.commander is None:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        st.title("🚀 Mission Control")

        st.subheader("Rocket Launch Visualization System")

        commander_name = st.text_input("Enter Commander Name")

        if st.button("Launch Dashboard"):
            if commander_name:
                st.session_state.commander = commander_name
                st.rerun()

        st.caption("Authorized Personnel Only")

        st.markdown('</div>', unsafe_allow_html=True)

else:

    st.success(f"Welcome Commander {st.session_state.commander}")

    st.write("Mission Dashboard Loading...")
