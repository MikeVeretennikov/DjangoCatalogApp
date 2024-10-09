import http

from django.test import Client, TestCase
from django.conf import settings


class StaticURLTests(TestCase):
    def test_homepage_endpoint_correct(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_coffee_endpoint_correct_text(self):
        responses = []

        for _ in range(10):
            responses.append(Client().get("/coffee/").content.decode())

        if settings.ALLOW_REVERSE:
            self.assertIn("<body>Я кинйач</body>", responses)
        else:
            self.assertIn("<body>Я чайник</body>", responses)

    def test_coffee_endpoint_correct_status_code(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
