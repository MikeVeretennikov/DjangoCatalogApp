from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_homepage_endpoint_correct(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint_correct_text(self):
        response = Client().get("/coffee/")
        self.assertIn("Я чайник", response.content.decode())

    def test_coffee_endpoint_correct_status_code(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, 418)
