import unittest
from unittest import mock
from streamlit.testing.v1 import AppTest
import time
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['API_BASE_URL'] = 'http://localhost:8000'


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs['url'] == 'http://localhost:8000/auth/login':
        username = kwargs['json']['username']
        password = kwargs['json']['password']
        if username == 'testauth' and password == 'testpass':
            return MockResponse({"access_token": "token"}, 200)
        else:
            return MockResponse({"detail": "Incorrect username or password"}, 401)
    return MockResponse(None, 404)


class TestAuth(unittest.TestCase):

    @mock.patch('streamlit.switch_page')  # <- важный фикс!
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('streamlit.success')
    def test_login(self, m_success, m_post, m_switch_page):
        at = AppTest.from_file("pages/auth.py", default_timeout=15)
        at.run()

        at.text_input[0].input("testauth")
        at.text_input[1].input("testpass")

        at.button[0].click().run()
        time.sleep(1)

        m_post.assert_called_once_with(
            url='http://localhost:8000/auth/login',
            json={'username': 'testauth', 'password': 'testpass'},
            timeout=30
        )
        m_success.assert_called_once_with('Login successful! Redirecting...')
        m_switch_page.assert_called_once_with("pages/dashboard.py")  # <-- ФИКС
        assert len(at.error) == 0
        assert not at.exception

    @mock.patch('streamlit.switch_page')
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('streamlit.error')
    def test_error(self, m_error, m_post, m_switch_page):
        at = AppTest.from_file("pages/auth.py", default_timeout=15)
        at.run()

        at.text_input[0].input("testauth")
        at.text_input[1].input("invalidpass")

        at.button[0].click().run()
        time.sleep(1)

        m_post.assert_called_once_with(
            url='http://localhost:8000/auth/login',
            json={'username': 'testauth', 'password': 'invalidpass'},
            timeout=30
        )
        m_error.assert_called_once_with('Incorrect username or password')
        m_switch_page.assert_not_called()
        assert len(at.error) == 0
        assert not at.exception
