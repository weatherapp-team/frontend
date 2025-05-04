import unittest
from unittest import mock
from streamlit.testing.v1 import AppTest
import os


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    url = args[0]
    if url.endswith("/alerts/notifications"):
        return MockResponse([
            {
                "column_name": "temperature",
                "comparator": ">",
                "number": 30,
                "location": "Moscow",
                "actual_number": 35,
                "timestamp": "2025-05-04T18:15:00"
            }
        ], 200)
    return MockResponse(None, 404)


def mocked_cookiemanager(*args, **kwargs):
    class MockCookie:
        def get_all(self, key=None):
            return {"token": "token"}

        def get(self, key):
            return "token"

    return MockCookie()


class TestNotificationCenter(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('extra_streamlit_components.CookieManager', side_effect=mocked_cookiemanager)
    @mock.patch('streamlit.page_link')  # избегаем switch_page
    def test_notification_display(self, m_page_link, m_cookie, m_get):
        os.environ['API_BASE_URL'] = 'http://localhost:8000'
        at = AppTest.from_file("src/pages/notification_center.py", default_timeout=15)
        at.run()

        assert at.title[0].value == "Alert Notifications"

        assert any("temperature" in m.value.lower() for m in at.markdown)
        assert any("Moscow" in m.value for m in at.markdown)
        assert any("Actual value" in m.value for m in at.markdown)
        assert any("Threshold" in m.value for m in at.markdown)
        assert any("Time" in m.value for m in at.markdown)

        assert len(at.error) == 0
        assert not at.exception
