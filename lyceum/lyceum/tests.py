from django.test import Client, TestCase
from django.test.utils import override_settings


class ReverseResponseMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_correct_on_reverse_behaviour(self):
        responses = []

        for _ in range(10):
            responses.append(Client().get("/coffee/").content.decode())
        self.assertIn("Я кинйач", responses)

    @override_settings(ALLOW_REVERSE=False)
    def test_correct_off_reverse_behaviour(self):
        responses = []

        for _ in range(10):
            responses.append(Client().get("/coffee/").content.decode())
        self.assertNotIn("Я кинйач", responses)
