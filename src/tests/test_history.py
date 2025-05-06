import unittest
from unittest import mock
from streamlit.testing.v1 import AppTest
import os
import time


def mocked_requests_get(*args, **kwargs):
    """
    Weather History request mock
    """
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    url = args[0]
    if url.endswith("/weather/Moscow/history"):
        return MockResponse([
            {
                "location": "Moscow",
                "main_weather": "Clouds",
                "icon": "04d",
                "description": "overcast clouds",
                "temperature": 13.13,
                "temperature_feels_like": 11.46,
                "temperature_min": 10.24,
                "temperature_max": 13.15,
                "pressure": 1013.0,
                "humidity": 37.0,
                "visibility": 10000.0,
                "wind_speed": 4.88,
                "wind_deg": 262.0,
                "timestamp": "2025-05-06T13:17:09.842114Z",
                "lat": 55.7522,
                "lon": 37.6156,
                "sunrise": "2025-05-06T01:35:40Z",
                "sunset": "2025-05-06T17:16:36Z"
            },
        ], 200)
    return MockResponse(None, 404)


def mocked_cookiemanager(*args, **kwargs):
    """
    CookieManager mock
    """
    class MockCookie:
        def get_all(self, key=None):
            return {"token": "token"}

        def get(self, key):
            return "token"

    return MockCookie()


class TestWeatherHistory(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('extra_streamlit_components.CookieManager', side_effect=mocked_cookiemanager)
    @mock.patch('streamlit.page_link')  # избегаем switch_page
    def test_weather_history_display(self, m_page_link, m_cookie, m_get):
        """
        Tests history rendering
        """
        print(m_page_link, m_cookie, m_get)
        os.environ['API_BASE_URL'] = 'http://localhost:8000'
        at = AppTest.from_file("src/pages/history.py", default_timeout=15)
        at.run()

        time.sleep(3)

        assert at.title[0].value == "Weather History"

        print(at.markdown.values)
        assert any("🕒 **Time**: 06.05.2025 13:17:09" in m.value for m in at.markdown)

        info = at.markdown.values[1].split("  \n")

        assert any("• **Weather state**: Clouds" in m for m in info)
        assert any("• **Description**: Overcast clouds" in m for m in info)
        assert any("• **Temperature**: 13.13 °C" in m for m in info)
        assert any("• **Feels like**: 11.46 °C" in m for m in info)
        assert any("• **Minimum temperature**: 10.24 °C" in m for m in info)
        assert any("• **Maximum temperature**: 13.15 °C" in m for m in info)
        assert any("• **Pressure**: 1013.0 hPa" in m for m in info)
        assert any("• **Humidity**: 37.0 %" in m for m in info)
        assert any("• **Wind speed**: 4.88 m/s" in m for m in info)
        assert any("• **Wind direction**: W (262.0°)" in m for m in info)
        assert any("• **Sunrise at**: 01:35" in m for m in info)
        assert any("• **Sunset at**: 17:16" in m for m in info)
        assert any("• **Latitude**: 55.7522" in m for m in info)
        assert any("• **Longitude**: 37.6156" in m for m in info)

        assert len(at.error) == 0
        assert not at.exception
