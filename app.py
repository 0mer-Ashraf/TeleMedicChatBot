import streamlit as st
from chat_screen import chat_screen
from landing_page import landing_page

# ----- Page Configuration -----
st.set_page_config(page_title="TeleMedicine Chatbot", page_icon=":hospital:", layout="wide")

# ----- Custom CSS for Styling -----
st.markdown(
    """
    <style>
    /* Set the background color to white */
    .reportview-container {
        background-color: white;
    }
    /* Center the container */
    .centered-container {
        max-width: 800px;
        margin: auto;
        padding: 2rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    /* Input field styling */
    .stTextInput > div > input {
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
        width: 100%;
    }
    /* Button styling */
    .stButton > button {
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
    }
    .stButton > button:hover {
        opacity: 0.9;
    }
    /* Title styling */
    .title {
        font-family: 'Arial', sans-serif;
        color: #333;
        margin-top: 20px;
    }
    /* Subtitle styling */
    .subtitle {
        font-family: 'Arial', sans-serif;
        color: #666;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----- Dummy User Database -----
USERS = {
    "admin": "admin",
}

# ----- Initialize Session State -----
if "page" not in st.session_state:
    st.session_state.page = "landing"  # Default to landing page

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----- Login Screen -----
def login_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>Welcome to TeleMedicine</h1>", unsafe_allow_html=True)
        
    st.markdown('<h4 class="subtitle">Sign In</h4>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Sign In", type="primary"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.page = "chat"
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")
        
        # Back button to return to landing page
        if st.button("Back to Home"):
            st.session_state.page = "landing"
            st.rerun()

# ----- App Routing -----
def main():
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "login":
        login_screen()
    elif st.session_state.page == "chat":
        if st.session_state.logged_in:
            chat_screen()
        else:
            st.session_state.page = "login"
            st.rerun()

if __name__ == "__main__":
    main()
