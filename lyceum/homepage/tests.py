import http

from django.test import Client, TestCase
from django.test.utils import override_settings


class StaticURLTests(TestCase):
    def test_homepage_endpoint_correct(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @override_settings(ALLOW_REVERSE=False)
    def test_coffee_endpoint_correct_text(self):
        client = Client()
        [client.get("/coffee/") for i in range(9)]
        response = client.get("/coffee/")
        self.assertIn("Я чайник", response.content.decode())

    def test_coffee_endpoint_correct_status_code(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
