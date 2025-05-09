import streamlit as st
from extra_streamlit_components import CookieManager
import time
import requests
from dotenv import load_dotenv
import os


load_dotenv()
API_URL = f"{os.getenv('API_BASE_URL')}/auth/login"

cookie_manager = CookieManager()


def validate_auth_data(username_field, password_field):
    """
    Validates user input for login form.
    """
    is_error = False
    if not username_field[1]:
        username_field[0][0].error("Username is required")
        is_error = True
    elif len(username_field[1]) < 5:
        username_field[0][0].error("Username must be at least 5 characters")
        is_error = True

    if not password_field[1]:
        password_field[0][0].error("Password is required")
        is_error = True
    elif len(password_field[1]) < 8:
        password_field[0][0].error("Password must be at least 8 characters")
        is_error = True

    return is_error


def generate_fields():
    """
    Generates input fields for auth form.
    Columns are used to display validation errors
    """
    username_ff = st.columns(1)
    username = username_ff[0].text_input("Username")

    password_ff = st.columns(1)
    password = password_ff[0].text_input("Password", type="password")

    return (username_ff, username), (password_ff, password)


def login_page():
    """
    Generates login page
    """
    if st.session_state.get("redirect_to_dashboard"):
        st.session_state.pop("redirect_to_dashboard")
        st.switch_page("pages/dashboard.py")

    st.title("Authorize", anchor=False)
    text = "Do not have an account? "
    link = "<a href=\"/register\" target=\"_self\">Register</a>"
    st.markdown(
        body=(text + link),
        unsafe_allow_html=True
    )

    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    username_field, password_field = generate_fields()
    (_, username) = username_field
    (_, password) = password_field

    is_validation_error = False
    if st.session_state["submitted"]:
        is_validation_error = validate_auth_data(
            username_field,
            password_field
        )

    if st.button("Submit") and not is_validation_error:
        with st.spinner("Loading..."):
            st.session_state["submitted"] = True

            is_error = validate_auth_data(username_field, password_field)

            if is_error:
                return
            else:
                st.session_state["submitted"] = False
                result = requests.post(
                    url=API_URL,
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
                    st.session_state["redirect_to_dashboard"] = True
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error(result.json()["detail"])


if __name__ == "__main__":
    login_page()
