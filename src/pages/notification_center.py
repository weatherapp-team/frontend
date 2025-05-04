import streamlit as st
import requests
from extra_streamlit_components import CookieManager
from utilities.sidebar import generate_sidebar
from datetime import datetime

def get_notifications(token):
    res = requests.get(
        "http://localhost:8000/alerts/notifications",
        headers={"Authorization": f"Bearer {token}"}
    )
    return res.json() if res.status_code == 200 else []

def get_comparator_string(comparator):
    return {
        ">=": "greater or equal to",
        "<=": "less or equal to",
        ">": "greater than",
        "<": "less than"
    }.get(comparator, comparator)

def notification_center_page():
    # ✅ УНИКАЛЬНЫЕ ключи для каждого компонента и вызова
    cookie_manager = CookieManager(key="notifications_cookie")
    cookie_manager.get_all(key="notifications_get_all")

    token = cookie_manager.get("token")

    if token is None:
        st.stop()

    if not token:
        st.warning("Please authorize first.")
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
                f"🔔 **Value `{notif['column_name']}` is {get_comparator_string(notif['comparator'])} than {notif['number']}!**"
            )
            st.markdown(
                f"• **Location**: {notif['location']}  \n"
                f"• **Actual value**: {notif['actual_number']}  \n"
                f"• **Threshold**: {notif['number']}  \n"
                f"• **Time**: {datetime.fromisoformat(notif['timestamp']).strftime('%d.%m.%Y %H:%M:%S')}"
            )
            st.divider()

if __name__ == "__main__":
    notification_center_page()
