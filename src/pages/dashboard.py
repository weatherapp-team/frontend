import streamlit as st
from extra_streamlit_components import CookieManager
import requests
from datetime import datetime
import time
from utilities.wind_direction import deg_to_direction
from utilities.sidebar import generate_sidebar

cookie_manager = CookieManager()


def get_data(location: str, token: str):
    result = requests.get(
        url=f"http://localhost:8000/weather/{location}",
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
    st1, st2 = st.columns([0.9, 0.1], vertical_alignment="center")
    st1.subheader(f"{weather['location']}: {weather['main_weather']}", anchor=False)
    st1.text(f"{weather['description']}.".capitalize())
    st2.image(f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png")


def weather_temp(weather):
    temp_col1, temp_col2, temp_col3, temp_col4 = st.columns(4)

    temp_col1.metric("Temperature", f"{weather['temperature']} °C")
    temp_col2.metric("Feels like", f"{weather['temperature_feels_like']} °C")
    temp_col3.metric("Minimum temperature", f"{weather['temperature_min']} °C")
    temp_col4.metric("Maximum temperature", f"{weather['temperature_max']} °C")


def weather_sun(weather):
    col1, col2 = st.columns(2)

    col1.metric(
        label="Sunrise at",
        value=datetime.fromisoformat(weather["sunrise"]).strftime("%H:%M")
    )
    col2.metric(
        label="Sunset at",
        value=datetime.fromisoformat(weather["sunset"]).strftime("%H:%M")
    )


def weather_humidity(weather):
    humidity, pressure = st.columns(2)
    humidity.metric("Humidity", f"{weather['humidity']} %")
    pressure.metric("Pressure", f"{weather['pressure']} hPa")


def weather_wind(weather):
    wind_speed, wind_direction = st.columns(2)
    wind_speed.metric("Wind speed", f"{weather['wind_speed']} m/s")

    direction = deg_to_direction(weather['wind_deg'])
    wind_direction.metric(
        label="Wind direction",
        value=f"{direction} ({weather['wind_deg']} °)"
    )


def dashboard():
    cookie_manager.get_all()

    input = st.text_input("Location", value="Moscow")

    if "logged_out" not in st.session_state:
        st.session_state["logged_out"] = False

    generate_sidebar(cookie_manager)
                
    if st.session_state["logged_out"]:
        st.session_state["logged_out"] = False
        st.session_state["submitted"] = False
        st.switch_page("pages/auth.py")

    with st.spinner("Loading..."):
        weather = get_data(input, cookie_manager.get("token"))

        if weather:
            weather_base_info(weather)

            weather_temp(weather)

            weather_sun(weather)

            weather_humidity(weather)

            weather_wind(weather)

            timestamp = datetime.fromisoformat(weather['timestamp'])
            last_updated = timestamp.strftime('%d.%m.%Y %H:%M:%S')

            st.markdown(f"**Last updated:** {last_updated}")
            st.map(
                data=[weather],
                latitude="lat",
                longitude="lon",
                zoom=11
            )


if __name__ == "__main__":
    dashboard()
