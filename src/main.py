import streamlit as st

pt = st.navigation([st.Page(page="pages/home.py", url_path="/home"), st.Page(page="pages/auth.py", url_path="/auth")])
pt.run()