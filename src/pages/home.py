from utils.token import authorized_only
import os
import streamlit as st

@authorized_only
def homepage():
    st.write('Home page')
    pass

homepage()