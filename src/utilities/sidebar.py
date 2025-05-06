import streamlit as st
import time


def generate_sidebar(cookie_manager):
    if "logged_out" not in st.session_state:
        st.session_state["logged_out"] = False

    with st.sidebar:
        st.page_link(
            page="pages/dashboard.py",
            label="Dashboard")
        st.page_link(
            page="pages/alert_settings.py",
            label="Alert Settings")
        st.page_link(
            page="pages/notification_center.py",
            label="Notifications"
        )
        st.page_link(
            page="pages/history.py",
            label="Weather History",
        )

        if st.button("Log out", type='secondary', use_container_width=True):
            st.session_state["logged_out"] = True
            if cookie_manager.get("token"):
                cookie_manager.delete("token")
                time.sleep(1)
                st.switch_page("pages/auth.py")

            # st.session_state["logged_out"] = False
            st.session_state["submitted"] = False
            st.switch_page("pages/auth.py")
