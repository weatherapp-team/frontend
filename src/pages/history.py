import os
import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
from extra_streamlit_components import CookieManager
from utilities.sidebar import generate_sidebar
from utilities.wind_direction import deg_to_direction

load_dotenv()
API_URL = f"{os.getenv('API_BASE_URL')}/weather"

def get_weather_history(token, location):
    res = requests.get(
        f"{API_URL}/{location}/history",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30
    )
    return res.json() if res.status_code == 200 else []

def history():
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
        history = get_weather_history(token, input)
        if not history:
            st.info("No weather history yet for this location.")
            return
        
        for element in history:
            with st.container():
                date = datetime.fromisoformat(element['timestamp'])
                time = date.strftime('%d.%m.%Y %H:%M:%S')

                sunrise_at = datetime.fromisoformat(element["sunrise"]).strftime("%H:%M")
                sunset_at = datetime.fromisoformat(element["sunset"]).strftime("%H:%M")

                st.markdown(f"🕒 **Time**: {time}")
                st.markdown(
                    f"• **Weather state**: {element['main_weather'].capitalize()}  \n"
                    f"• **Description**: {element['description'].capitalize()}  \n"
                    f"• **Temperature**: {element['temperature']} °C  \n"
                    f"• **Feels like**: {element['temperature_feels_like']} °C  \n"
                    f"• **Minimum temperature**: {element['temperature_min']} °C  \n"
                    f"• **Maximum temperature**: {element['temperature_max']} °C  \n"
                    f"• **Pressure**: {element['pressure']} hPa  \n"
                    f"• **Humidity**: {element['humidity']} %  \n"
                    f"• **Wind speed**: {element['wind_speed']} m/s  \n"
                    f"• **Wind direction**: {deg_to_direction(element['wind_deg'])} ({element['wind_deg']}°)  \n"
                    f"• **Sunrise at**: {sunrise_at}  \n"
                    f"• **Sunset at**: {sunset_at}  \n"
                    f"• **Latitude**: {element['lat']}  \n"
                    f"• **Longitude**: {element['lon']} \n"
                )
                st.divider()

if __name__ == "__main__":
    history()
