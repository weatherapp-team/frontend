from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st
import time
import os
from utils.token import unauthorized_only, save_token


def handle_click(username: str, password: str):
    if st.session_state.submitted:
        return
    
    st.session_state.submitted = True

    save_token('hello')

    time.sleep(0.3)

    st.session_state.submitted = False

    st.switch_page("pages/home.py")

@unauthorized_only
def authpage():
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    st.title("Authorize", anchor=False)
    st.write("To continue, please log in")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", disabled=st.session_state.submitted):
        handle_click(username, password)

authpage()