import http

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get("/about/")
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Status code should be 200",
        )
