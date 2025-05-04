import streamlit as st
import requests
from extra_streamlit_components import CookieManager
from utilities.sidebar import generate_sidebar
from dotenv import load_dotenv
import os


load_dotenv()
API_URL = f"{os.getenv('API_BASE_URL')}/alerts"


def get_alerts(token):
    res = requests.get(API_URL, headers={"Authorization": f"Bearer {token}"})
    return res.json() if res.status_code == 200 else []


def add_alert(alert, token):
    res = requests.post(
        API_URL,
        json=alert,
        headers={"Authorization": f"Bearer {token}"}
    )
    return res.ok


def delete_alert(alert_id, token):
    res = requests.delete(
        API_URL,
        json={"id": alert_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    return res.ok


def alert_settings_page():
    cookie_manager = CookieManager(key="alerts_cookie")
    cookies = cookie_manager.get_all(key="alerts_get_all")
    token = cookie_manager.get("token")

    if cookies == {}:
        st.stop()

    if not token or st.session_state["logged_out"]:
        st.session_state["logged_out"] = False
        st.switch_page("pages/auth.py")

    generate_sidebar(cookie_manager)
    st.title("Alert Threshold Settings")

    # Add new alert
    st.subheader("Add New Threshold")
    with st.form("add_alert_form"):
        location = st.text_input("Location")
        column_name = st.selectbox(
            "Field", ["temperature", "humidity", "pressure"]
        )
        comparator = st.selectbox("Comparator", [">=", "<=", ">", "<"])
        number = st.number_input(
            "Number",
            min_value=-1000,
            max_value=1000,
            step=1)

        submitted = st.form_submit_button("Add Alert")
        if submitted:
            if not location:
                st.warning("Location is required.")
            else:
                success = add_alert({
                    "location": location,
                    "column_name": column_name,
                    "comparator": comparator,
                    "number": number
                }, token)
                if success:
                    st.success("Alert added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add alert.")

    # Show existing alerts
    st.subheader("Current Thresholds")
    alerts = get_alerts(token)
    for alert in alerts:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        col1.markdown(f"**Location:** {alert['location']}")
        col2.markdown(f"**Field:** {alert['column_name']}")
        col3.markdown(f"**Comparator:** {alert['comparator']}")
        col4.markdown(f"**Number:** {alert['number']}")
        if col5.button("❌", key=f"del_{alert['id']}"):
            if delete_alert(alert['id'], token):
                st.success("Alert deleted")
                st.rerun()

    st.divider()


if __name__ == "__main__":
    alert_settings_page()
