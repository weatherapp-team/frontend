import streamlit as st
from extra_streamlit_components import CookieManager
import time
import requests

cookie_manager = CookieManager()

def validate_auth_data(username_field, password_field):
    is_error = False

    if not username_field[1]:
        username_field[0][0].error("Username is required")
        is_error = True

    if not password_field[1]:
        password_field[0][0].error("Password is required")
        is_error = True

    return is_error

def generate_fields():
    username_ff = st.columns(1)
    username = username_ff[0].text_input("Username")

    password_ff = st.columns(1)
    password = password_ff[0].text_input("Password", type="password")

    return (username_ff, username), (password_ff, password)

def login_page():
    st.title("Authorize", anchor=False)
    st.markdown("Do not have an account? <a href=\"/register\" target=\"_self\">Register</a>", unsafe_allow_html=True)

    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    username_field, password_field = generate_fields()
    (_, username) = username_field
    (_, password) = password_field

    if st.session_state["submitted"]:
        validate_auth_data(username_field, password_field)

    if st.button("Submit"):
        with st.spinner("Loading..."):
            st.session_state["submitted"] = True

            is_error = validate_auth_data(username_field, password_field)

            if is_error:
                return
            else:
                st.session_state["submitted"] = False
                result = requests.post(
                    url="http://localhost:8000/auth/login",
                    json={
                        "username": username,
                        "password": password,
                    },
                    timeout=30
                )
                if result.status_code == 200:
                    cookie_manager.set(
                        cookie="token",
                        val=result.json()["access_token"],
                        max_age=3600
                    )
                    st.success("Login successful! Redirecting...")
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error(result.json()["detail"])

    cookies = cookie_manager.get_all()

    if cookies.get("token"):
        st.switch_page("pages/dashboard.py")


if __name__ == "__main__":
    login_page()
