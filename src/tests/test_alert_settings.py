import unittest
from unittest import mock
from streamlit.testing.v1 import AppTest
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
os.environ['API_BASE_URL'] = 'http://localhost:8000'


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self._json_data = json_data
            self.status_code = status_code

        def json(self):
            return self._json_data

    if args[0].endswith("/alerts"):
        return MockResponse([
            {
                "id": 1,
                "location": "Moscow",
                "column_name": "temperature",
                "comparator": ">",
                "number": 30
            }
        ], 200)

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code
            self.ok = status_code == 200

    if args[0].endswith("/alerts"):
        return MockResponse(200)

    return MockResponse(404)


def mocked_requests_delete(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code
            self.ok = status_code == 200

    if args[0].endswith("/alerts"):
        return MockResponse(200)

    return MockResponse(404)


def mocked_cookiemanager(*args, **kwargs):
    class MockCookies:
        def get(self, key):
            if key == "token":
                return "token"
            raise KeyError(key)

    class MockCookieManager:
        def get_all(self, *args, **kwargs):
            return {"token": "token"}
        def get(self, key):
            return "token"

    return MockCookieManager()


def mocked_page_link(page, label):
    return st.write(label)


class TestAlertSettings(unittest.TestCase):

    @mock.patch("streamlit.page_link", side_effect=mocked_page_link)
    @mock.patch("streamlit.rerun")
    @mock.patch("streamlit.success")
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("extra_streamlit_components.CookieManager", side_effect=mocked_cookiemanager)
    def test_add_alert(self, m_cookie, m_get, m_post, m_success, m_rerun, m_page_link):
        at = AppTest.from_file("src/pages/alert_settings.py", default_timeout=15)
        at.session_state["logged_out"] = False
        at.run()

        at.text_input[0].input("Moscow")
        at.selectbox[0].set_value("temperature")
        at.selectbox[1].set_value(">")
        at.number_input[0].set_value(30)
        at.button[0].click().run()

        m_post.assert_called_once()
        m_success.assert_called_once_with("Alert added successfully!")

    @mock.patch("streamlit.page_link", side_effect=mocked_page_link)
    @mock.patch("streamlit.rerun")
    @mock.patch("streamlit.success")
    @mock.patch("requests.delete", side_effect=mocked_requests_delete)
    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("extra_streamlit_components.CookieManager", side_effect=mocked_cookiemanager)
    def test_delete_alert(self, m_cookie, m_get, m_delete, m_success, m_rerun, m_page_link):
        at = AppTest.from_file("src/pages/alert_settings.py", default_timeout=15)
        at.session_state["logged_out"] = False
        at.run()

        delete_button = next(b for b in at.button if b.label == "❌")
        delete_button.click().run()

        m_delete.assert_called_once()
        m_success.assert_called_once_with("Alert deleted")

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("extra_streamlit_components.CookieManager", side_effect=mocked_cookiemanager)
    @mock.patch("streamlit.page_link", side_effect=mocked_page_link)
    def test_show_existing_alerts(self, m_cookie, m_get, m_page_link):
        at = AppTest.from_file("src/pages/alert_settings.py", default_timeout=15)
        at.session_state["logged_out"] = False
        at.run()

        assert any("Moscow" in m.value for m in at.markdown), "Moscow alert not found in output"
