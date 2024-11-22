from datetime import date, datetime

from django.shortcuts import reverse
from django.test import Client, TestCase
from django.test.utils import override_settings
from parameterized import parameterized

from lyceum.middleware import (
    reverse_russian_words,
)
from users.models import User


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

    def test_correct_default_reverse_behaviour(
        self,
    ):
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


class BirthdayContextProcessor(TestCase):
    def test_today_birthday(self):
        data_signup = {
            "username": "user",
            "email": "test@user.ru",
            "password1": "140806Bb",
            "password2": "140806Bb",
        }
        Client().post(
            reverse("users:signup"),
            data=data_signup,
        )
        new_user = User.objects.prefetch_related("profile").first()
        new_user.profile.birthday = datetime.now().date()
        new_user.profile.save()
        users_birthday = User.objects.filter(
            profile__birthday__day=datetime.now().date().day,
            profile__birthday__month=datetime.now().date().month,
        ).select_related("profile")
        response = Client().get(reverse("homepage:index-page"))
        self.assertQuerysetEqual(
            users_birthday.all(),
            response.context["birthday_people"].all(),
        )

    def test_not_today_birthday(self):
        data_signup = {
            "username": "user",
            "email": "test@user.ru",
            "password1": "140806Bb",
            "password2": "140806Bb",
        }
        Client().post(
            reverse("users:signup"),
            data=data_signup,
        )
        now = datetime.now().date()
        new_user = User.objects.prefetch_related("profile").first()
        new_user.profile.birthday = date(now.year, now.month, now.day - 1)
        new_user.profile.save()
        response = Client().get(reverse("homepage:index-page"))
        self.assertRaises(
            TypeError,
            response.context["birthday_people"].first(),
        )
        self.assertRaisesMessage(
            "argument of type 'NoneType' is not iterable",
            response.context["birthday_people"].first(),
        )


__all__ = ()
