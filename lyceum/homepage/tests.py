import http

from django.conf import settings
from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_homepage_endpoint_correct(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_coffee_endpoint_correct_text(self):
        responses = []

        for _ in range(10):
            responses.append(Client().get("/coffee/").content.decode())

        if settings.ALLOW_REVERSE:
            self.assertIn("Я кинйач", responses)
        else:
            self.assertIn("Я чайник", responses)

    def test_coffee_endpoint_correct_status_code(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
