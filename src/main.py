import streamlit as st

pt = st.navigation([
    st.Page(page="pages/dashboard.py", url_path="/dashboard"),
    st.Page(page="pages/alert_settings.py", url_path="/alerts"),
    st.Page(page="pages/notification_center.py", url_path="/notifications"),
    st.Page(page="pages/auth.py", url_path="/auth"),
    st.Page(page="pages/register.py", url_path="/register")
])
pt.run()
