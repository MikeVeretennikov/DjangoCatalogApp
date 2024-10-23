from django.test import Client, TestCase
from django.test.utils import override_settings
from parameterized import parameterized

from lyceum.middleware import reverse_russian_words


class ReverseResponseMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_correct_on_reverse_behaviour(self):
        responses = []

        for _ in range(31):
            responses.append(Client().get("/coffee/").content.decode())

        reverse_count = len([i for i in responses if i == "Я кинйач"])

        self.assertGreaterEqual(
            reverse_count,
            3,
            "When ALLOW_REVERSE is True, MW should  work",
        )

    @override_settings(ALLOW_REVERSE=False)
    def test_correct_off_reverse_behaviour(self):
        responses = []

        for _ in range(31):
            responses.append(Client().get("/coffee/").content.decode())

        reverse_count = len([i for i in responses if i == "Я кинйач"])

        self.assertEqual(
            reverse_count,
            0,
            "When ALLOW_REVERSE is False, MW should not work",
        )

    def test_correct_default_reverse_behaviour(self):
        responses = []

        for _ in range(31):
            responses.append(Client().get("/coffee/").content.decode())

        reverse_count = len([i for i in responses if i == "Я кинйач"])

        self.assertGreaterEqual(
            reverse_count,
            3,
            "When ALLOW_REVERSE is not given, default value"
            "True should be used, MW should work",
        )


class RegexReverseRussianWordsTests(TestCase):

    @parameterized.expand(
        [
            ("Слово", "оволС"),
            ("словоqwerty", "словоqwerty"),
            ("Я чайник", "Я кинйач"),
            ("слово123", "слово123"),
            ("123 456", "123 456"),
            ("123слово", "123слово"),
        ],
    )
    def test_reverse_only_russian_words(self, word, expected):
        self.assertEqual(
            reverse_russian_words(word),
            expected,
            "Word with only russian letters and some symbols"
            "is the only right form of a russian word",
        )


__all__ = ["ReverseResponseMiddlewareTests", "ReverseResponseMiddlewareTests"]
