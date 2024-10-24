import http

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_homepage_endpoint_correct(self):
        response = Client().get(reverse("homepage:index-page"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Status code should be 200",
        )

    def test_coffee_endpoint_correct_text(self):
        responses = []

        for _ in range(10):
            responses.append(
                Client().get(reverse("homepage:coffee-page")).content.decode(),
            )

        if settings.ALLOW_REVERSE:
            self.assertIn(
                "Я кинйач",
                responses,
                "Text should be 'Я чайник' reversed"
                "because ALLOW_REVERSE is True",
            )
        else:
            self.assertIn("Я чайник", responses, "Text should be 'Я чайник'")

    def test_coffee_endpoint_correct_status_code(self):
        response = Client().get(reverse("homepage:coffee-page"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.IM_A_TEAPOT,
            "Status code should be 418",
        )


__all__ = ["StaticURLTests"]
