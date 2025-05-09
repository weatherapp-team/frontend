import os
import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
from extra_streamlit_components import CookieManager
from utilities.sidebar import generate_sidebar


load_dotenv()
API_URL = f"{os.getenv('API_BASE_URL')}/alerts/notifications"


def get_notifications(token):
    """
    Gets notifications from the API
    """
    res = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30
    )
    return res.json() if res.status_code == 200 else []


def get_comparator_string(comparator):
    """
    Returns human-readable string from the provided comparator
    """
    return {
        ">=": "greater or equal to",
        "<=": "less or equal to",
        ">": "greater than",
        "<": "less than"
    }.get(comparator, comparator)


def notification_center_page():
    """
    Renders notification center page
    """
    cookie_manager = CookieManager(key="notifications_cookie")
    cookies = cookie_manager.get_all(key="notifications_get_all")

    token = cookie_manager.get("token")

    if cookies == {}:
        st.stop()

    if not token or st.session_state.get("logged_out"):
        st.session_state["logged_out"] = False
        st.switch_page("pages/auth.py")

    generate_sidebar(cookie_manager)
    st.title("Alert Notifications")

    notifications = get_notifications(token)
    if not notifications:
        st.info("No notifications yet.")
        return

    for notif in notifications:
        with st.container():
            st.markdown(
                f"🔔 **Value `{notif['column_name']}` is "
                f"{get_comparator_string(notif['comparator'])} "
                f"than {notif['number']}!**"
            )
            date = datetime.fromisoformat(notif['timestamp'])
            time = date.strftime('%d.%m.%Y %H:%M:%S')
            st.markdown(
                f"• **Location**: {notif['location']}  \n"
                f"• **Actual value**: {notif['actual_number']}  \n"
                f"• **Threshold**: {notif['number']}  \n"
                f"• **Time**: "
                f"{time}"
            )
            st.divider()


if __name__ == "__main__":
    notification_center_page()
