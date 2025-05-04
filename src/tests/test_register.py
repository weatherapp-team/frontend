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
    print(args, kwargs)
    if kwargs['url'] == 'http://localhost:8000/auth/register':
        if kwargs['json']['username'] and kwargs['json']['password']:
            return MockResponse(
                json_data={"message": "User created successfully"},
                status_code=201
            )
        else:
            return MockResponse(
                json_data={"detail": "Error: Unprocessable Entity"},
                status_code=422
            )
    else:
        return MockResponse(None, 404)


class TestRegister(unittest.TestCase):

    @mock.patch('streamlit.switch_page')
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('streamlit.success')
    def test_login(self, mock_success, mock_post, mock_switch_page):
        at = AppTest.from_file("../pages/register.py", default_timeout=15)
        at.run()

        at.text_input[0].input("testusername")
        at.text_input[1].input("testpass")
        at.text_input[2].input("testemail@bread.example")
        at.text_input[3].input("testfullname")

        at.button[0].click().run()

        time.sleep(3)

        mock_post.assert_called_once_with(
            url='http://localhost:8000/auth/register',
            json={
                'username': 'testusername',
                'password': 'testpass',
                'email': 'testemail@bread.example',
                'full_name': 'testfullname'
            },
            timeout=30)

        success_text = 'Registration successful! Redirecting...'
        mock_success.assert_called_once_with(success_text)
        mock_switch_page.assert_called_once_with("pages/auth.py")
        assert len(at.error) == 0
        assert not at.exception
