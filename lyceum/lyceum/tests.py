from django.test import Client, TestCase
from django.test.utils import override_settings


class ReverseResponseMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_correct_on_reverse_behaviour(self):
        client = Client()

        for i in range(9):
            client.get("/coffee/").content.decode()

        tenth_response = client.get("/coffee/")

        self.assertIn("Я кинйач", tenth_response.content.decode())

    @override_settings(ALLOW_REVERSE=False)
    def test_correct_off_reverse_behaviour(self):
        client = Client()

        for i in range(9):
            client.get("/coffee/").content.decode()

        tenth_response = client.get("/coffee/")

        self.assertIn("Я чайник", tenth_response.content.decode())
