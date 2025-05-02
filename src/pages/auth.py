import streamlit as st
from extra_streamlit_components import CookieManager
import time
import requests

cookie_manager = CookieManager()

def login_page():
    st.title("Authorize", anchor=False)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        result = requests.post("http://localhost:8000/auth/login", json={
            "username": username,
            "password": password,
        })
        if result.status_code == 200:
            cookie_manager.set("token", result.json()["access_token"], max_age=3600)
            time.sleep(3)
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error(result.json()["detail"])

    cookies = cookie_manager.get_all()

    if cookies.get("token"):
        st.switch_page("pages/dashboard.py")
    st.write("Current Cookies:", cookies)

if __name__ == "__main__":
    login_page()