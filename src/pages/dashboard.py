import streamlit as st
from extra_streamlit_components import CookieManager
import requests
from datetime import datetime
import time

cookie_manager = CookieManager()

def get_data(location: str, token: str):
    result = requests.get(f"http://localhost:8000/weather/{location}", headers={'Authorization': f"Bearer {token}"})
    if result.status_code == 200:
        return result.json(), False
    elif result.status_code == 401:
        cookie_manager.delete("token")
        time.sleep(1)
        st.switch_page("pages/auth.py")
    else:
        print(result)
        st.error(result.json())
        return result.json(), True


def dashboard():
    cookies = cookie_manager.get_all()

    input = st.text_input("Location", value="Moscow")

    weather, fail = get_data(input, cookies.get("token"))

    st1, st2 = st.columns([0.9, 0.1], vertical_alignment="center")
    st1.subheader(f"{input}: {weather['main_weather']}")
    st1.text(f"{weather['description']}.".capitalize())
    st2.image(f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png")
    

    temp_col1, temp_col2, temp_col3, temp_col4 = st.columns(4)

    temp_col1.metric("Temperature", f"{weather['temperature']} °C")
    temp_col2.metric("Feels like", f"{weather['temperature_feels_like']} °C")
    temp_col3.metric("Minimum temperature", f"{weather['temperature_min']} °C")
    temp_col4.metric("Maximum temperature", f"{weather['temperature_max']} °C")

    sun1, sun2 = st.columns(2)
    sun1.metric("Sunrise at", datetime.fromisoformat(weather["sunrise"]).strftime("%H:%M"))
    sun2.metric("Sunset at", datetime.fromisoformat(weather["sunset"]).strftime("%H:%M"))

    humidity, pressure = st.columns(2)
    humidity.metric("Humidity", f"{weather['humidity']} %")
    pressure.metric("Pressure", f"{weather['pressure']} hPa")

    wind_speed, wind_direction = st.columns(2)
    wind_speed.metric("Wind speed", f"{weather['wind_speed']} m/s")
    wind_direction.metric("Wind direction", f"{weather['wind_deg']} °")

    st.markdown(f"**Last updated:** {datetime.fromisoformat(weather['timestamp']).strftime('%d.%m.%Y %H:%M:%S')}")
    st.map(data=[{"lat": 1.23456789, "lon": -0.987654321}], latitude="lat", longitude="lon", zoom=4)
    pass

if __name__ == "__main__":
    dashboard()