import unittest
from unittest import mock
from streamlit.testing.v1 import AppTest
import streamlit as st
import time
import os
from dotenv import load_dotenv


load_dotenv()
os.environ['API_BASE_URL'] = 'http://localhost:8000'


def mocked_requests_get(*args, **kwargs):
    """
    Dashboard data request mock
    """
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs['url'].startswith('http://localhost:8000/weather'):
        if kwargs['headers']['Authorization'] == 'Bearer token':
            if kwargs['url'].endswith('/Moscow'):
                return MockResponse({
                    "location": "Moscow",
                    "main_weather": "Rain",
                    "icon": "10d",
                    "description": "light rain",
                    "temperature": 11.38,
                    "temperature_feels_like": 9.91,
                    "temperature_min": 10.29,
                    "temperature_max": 11.48,
                    "pressure": 1003.0,
                    "humidity": 51.0,
                    "visibility": 10000.0,
                    "wind_speed": 7.27,
                    "wind_deg": 7.27,
                    "timestamp": "2025-05-03T15:08:56.984512",
                    "lat": 55.7522,
                    "lon": 37.6156,
                    "sunrise": "2025-05-03T01:42:03",
                    "sunset": "2025-05-03T17:10:39"
                }, 200)
            else:
                return MockResponse({"detail": "City not found"}, 404)
        else:
            return MockResponse({"detail": "Not authenticated"}, 401)
    return MockResponse(None, 404)


def mocked_cookiemanager(*args, **kwargs):
    """
    CookieManager mock
    """
    class MockCookieManager:
        def get_all(self, *args, **kwargs):
            return {"token": "token"}

        def get(self, key):
            return "token" if key == "token" else None

        def delete(self, key):
            pass

    return MockCookieManager()


def mocked_page_link(page, label):
    """
    Page link mock
    """
    return st.write(f"[Mocked page link] {label}")


class TestDashboard(unittest.TestCase):

    @mock.patch('streamlit.page_link', side_effect=mocked_page_link)
    @mock.patch('extra_streamlit_components.CookieManager', side_effect=mocked_cookiemanager)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_dashboard(self, mock_get, mock_cookiemanager, mock_page_link):
        """
        Tests dashboard data loading
        """
        at = AppTest.from_file("src/pages/dashboard.py", default_timeout=15)
        at.run()

        time.sleep(2)

        mock_get.assert_called_once_with(
            url='http://localhost:8000/weather/Moscow',
            headers={'Authorization': 'Bearer token'},
            timeout=30
        )

        expected_metrics = {
            "Temperature": "11.38 °C",
            "Feels like": "9.91 °C",
            "Minimum temperature": "10.29 °C",
            "Maximum temperature": "11.48 °C",
            "Sunrise at": "01:42",
            "Sunset at": "17:10",
            "Humidity": "51.0 %",
            "Pressure": "1003.0 hPa",
            "Wind speed": "7.27 m/s",
            "Wind direction": "N (7.27 °)"
        }

        for metric in at.metric:
            assert expected_metrics[metric.label] == metric.value

        assert len(at.error) == 0
        assert not at.exception
