import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from extra_streamlit_components import CookieManager
from utilities.wind_direction import deg_to_direction
from utilities.sidebar import generate_sidebar


load_dotenv()
API_URL = f"{os.getenv('API_BASE_URL')}/weather"


def get_data(location: str, token: str, cookie_manager: CookieManager):
    """
    Gets data for the dashboard metrics
    """
    result = requests.get(
        url=f"{API_URL}/{location}",
        headers={'Authorization': f"Bearer {token}"},
        timeout=30
    )
    if result.status_code == 200:
        return result.json()
    elif result.status_code == 401:
        if cookie_manager.get("token"):
            cookie_manager.delete("token")
        time.sleep(1)
        st.switch_page("pages/auth.py")
    else:
        st.write("City not found. Please try again.")
        return None


def weather_base_info(weather):
    """
    Renders basic info about the weather.
    It shows description of current weather and title of the location
    """
    st1, st2 = st.columns([0.9, 0.1], vertical_alignment="center")
    st1.subheader(
        body=f"{weather['location']}: {weather['main_weather']}",
        anchor=False
    )
    st1.text(f"{weather['description']}.".capitalize())
    st2.image(f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png")


def weather_temp(weather):
    """
    Renders temperature info about the weather.
    It shows four temperature metrics
    """
    temp_col1, temp_col2, temp_col3, temp_col4 = st.columns(4)
    temp_col1.metric("Temperature", f"{weather['temperature']} °C")
    temp_col2.metric("Feels like", f"{weather['temperature_feels_like']} °C")
    temp_col3.metric("Minimum temperature", f"{weather['temperature_min']} °C")
    temp_col4.metric("Maximum temperature", f"{weather['temperature_max']} °C")


def weather_sun(weather):
    """
    Renders info about sunrise and sunset
    """
    col1, col2 = st.columns(2)
    col1.metric(
        "Sunrise at",
        datetime.fromisoformat(weather["sunrise"]).strftime("%H:%M"))
    col2.metric(
        "Sunset at",
        datetime.fromisoformat(weather["sunset"]).strftime("%H:%M"))


def weather_humidity(weather):
    """
    Renders info about humidity
    """
    humidity, pressure = st.columns(2)
    humidity.metric("Humidity", f"{weather['humidity']} %")
    pressure.metric("Pressure", f"{weather['pressure']} hPa")


def weather_wind(weather):
    """
    Renders info about wind speed and direction
    """
    wind_speed, wind_direction = st.columns(2)
    wind_speed.metric("Wind speed", f"{weather['wind_speed']} m/s")

    direction = deg_to_direction(weather['wind_deg'])
    wind_direction.metric(
        "Wind direction",
        f"{direction} ({weather['wind_deg']} °)")


def dashboard():
    """
    Renders dashboard page
    """
    cookie_manager = CookieManager(key="dashboard_cookie")
    cookies = cookie_manager.get_all(key="dashboard_get_all")
    token = cookies.get("token")

    if cookies == {}:
        st.stop()

    if not token or st.session_state.get("logged_out"):
        st.session_state["logged_out"] = False
        st.switch_page("pages/auth.py")

    generate_sidebar(cookie_manager)

    input = st.text_input("Location", value="Moscow")

    with st.spinner("Loading..."):
        weather = get_data(input, token, cookie_manager)

        if weather:
            weather_base_info(weather)
            weather_temp(weather)
            weather_sun(weather)
            weather_humidity(weather)
            weather_wind(weather)

            timestamp = datetime.fromisoformat(weather['timestamp'])
            last_updated = timestamp.strftime('%d.%m.%Y %H:%M:%S')
            st.markdown(f"**Last updated:** {last_updated}")
            st.map(data=[weather], latitude="lat", longitude="lon", zoom=11)


if __name__ == "__main__":
    dashboard()
