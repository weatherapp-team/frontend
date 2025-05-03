import unittest
from unittest import mock
from streamlit.testing.v1 import AppTest
import time


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
        if (username == 'testauth' and password == 'testpass'):
            return MockResponse(
                json_data={"access_token": "token"},
                status_code=200
            )
        else:
            return MockResponse(
                json_data={"detail": "Incorrect username or password"},
                status_code=401
            )
    else:
        return MockResponse(None, 404)


class TestAuth(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('streamlit.success')
    def test_login(self, m_success, m_post):
        at = AppTest.from_file("../pages/auth.py", default_timeout=15)
        at.run()

        at.text_input[0].input("testauth")
        at.text_input[1].input("testpass")

        at.button[0].click().run()

        time.sleep(3)

        m_post.assert_called_once_with(
            url='http://localhost:8000/auth/login',
            json={'username': 'testauth', 'password': 'testpass'},
            timeout=30
        )
        m_success.assert_called_once_with('Login successful! Redirecting...')
        assert len(at.error) == 0
        assert not at.exception

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('streamlit.error')
    def test_error(self, m_error, m_post):
        at = AppTest.from_file("../pages/auth.py", default_timeout=15)
        at.run()

        at.text_input[0].input("testauth")
        at.text_input[1].input("invalidpass")

        at.button[0].click().run()

        time.sleep(3)

        m_post.assert_called_once_with(
            url='http://localhost:8000/auth/login',
            json={'username': 'testauth', 'password': 'invalidpass'},
            timeout=30
        )
        m_error.assert_called_once_with('Incorrect username or password')
        assert len(at.error) == 0
        assert not at.exception
