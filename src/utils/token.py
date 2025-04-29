from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st
import os
import extra_streamlit_components as stx
import time

@st.fragment
def get_manager(key: str):
    return stx.CookieManager(key)

def check_token():
    # time.sleep(0.3)

    if 'token' not in st.context.cookies:
        return False
    else:
        return True
    
def authorized_only(func):
    def wrapper():
        token = check_token()
        if token:
            func()
        else:
            st.switch_page("pages/auth.py")
    return wrapper
    
def unauthorized_only(func):
    def wrapper():
        token = check_token()
        if not token:
            func()
        else:
            # pass
            st.switch_page("pages/home.py")
            # st.stop()
    return wrapper

def save_token(token: str):
    cookies = get_manager(key="save_token")

    cookies.set("token", token)

    # time.sleep(0.3)