import streamlit as st
import time
import requests
import re
from dotenv import load_dotenv
import os


load_dotenv()
API_URL = f"{os.getenv('API_BASE_URL')}/auth/register"


def validate_register_data(
        username_field,
        password_field,
        email_field,
        full_name_field
):
    """
    Validates data for the registration form.
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
    if not email_field[1]:
        email_field[0][0].error("Email is required")
        is_error = True
    else:
        match = re.match(r"^\S+@\S+\.\S+$", email_field[1])
        if not match:
            email_field[0][0].error("Invalid email format")
            is_error = True
    if not full_name_field[1]:
        full_name_field[0][0].error("Full name is required")
        is_error = True
    return is_error


def generate_fields():
    """
    Generates input fields for registration form.
    Columns are used to display validation errors
    """
    username_ff = st.columns(1)
    username = username_ff[0].text_input("Username")

    password_ff = st.columns(1)
    password = password_ff[0].text_input("Password", type="password")

    email_ff = st.columns(1)
    email = email_ff[0].text_input("Email")

    full_name_ff = st.columns(1)
    full_name = full_name_ff[0].text_input("Full name")

    return (
        (username_ff, username),
        (password_ff, password),
        (email_ff, email),
        (full_name_ff, full_name)
    )


def register_request(username, password, email, full_name):
    """
    Sends registration request to the API
    """
    result = requests.post(
        url=API_URL,
        json={
            "username": username,
            "password": password,
            "email": email,
            "full_name": full_name
        },
        timeout=30
    )
    return result


def submit_function(
    username_field,
    password_field,
    email_field,
    full_name_field
):
    """
    Processes user registration request and sends it to the API
    """
    st.session_state["submitted"] = True

    is_error = validate_register_data(
        username_field,
        password_field,
        email_field,
        full_name_field
    )
    if is_error:
        return
    else:
        st.session_state["submitted"] = False
        result = register_request(
            username=username_field[1],
            password=password_field[1],
            email=email_field[1],
            full_name=full_name_field[1]
        )
        if result.status_code == 201:
            st.session_state["registered"] = True
            st.success("Registration successful! Redirecting...")
            time.sleep(2)
            st.rerun()
        else:
            try:
                error = result.json()["detail"]
                st.error(error)
            except Exception:
                st.error("Unknown error occurred. Please try again.")


def register_page():
    """
    Renders registration page
    """
    st.title("Register", anchor=False)
    text = "Already have an account? "
    link = "<a href=\"/auth\" target=\"_self\">Authorize</a>"
    st.markdown(
        body=(text + link),
        unsafe_allow_html=True
    )

    if "registered" not in st.session_state:
        st.session_state["registered"] = False

    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    (username_field,
     password_field,
     email_field,
     full_name_field) = generate_fields()

    is_validation_error = False
    if st.session_state["submitted"]:
        is_validation_error = validate_register_data(
            username_field,
            password_field,
            email_field,
            full_name_field
        )

    if st.button("Register") and not is_validation_error:
        with st.spinner("Loading..."):
            submit_function(
                username_field,
                password_field,
                email_field,
                full_name_field
            )

    if st.session_state["registered"]:
        st.session_state["registered"] = False
        st.switch_page("pages/auth.py")


if __name__ == "__main__":
    register_page()
