import streamlit as st
from extra_streamlit_components import CookieManager
import time
import requests

def register_page():
    st.title("Register", anchor=False)

    if "registered" not in st.session_state:
        st.session_state["registered"] = False

    # Input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    full_name = st.text_input("Full name")

    # Submit button
    if st.button("Register"):
        result = requests.post("http://localhost:8000/register", json={
            "username": username,
            "password": password,
            "email": email,
            "full_name": full_name
        })
        if result.status_code == 201:
            st.session_state["registered"] = True
            st.success("Registration successful! Redirecting...")
            time.sleep(2)
            st.rerun()
        else:
            st.error(result.json()["detail"])


    if st.session_state["registered"]:
        st.session_state["registered"] = False
        st.switch_page("pages/auth.py")

if __name__ == "__main__":
    register_page()