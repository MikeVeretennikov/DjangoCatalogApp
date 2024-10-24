import http

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get(reverse("about:index-page"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Status code should be 200",
        )


__all__ = ["StaticURLTests"]
