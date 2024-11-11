import tempfile


import django.test
import django.urls
from parameterized import parameterized

import feedback.models


class FeedbackFormTests(django.test.TestCase):
    def test_form_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        self.assertIn("form", response.context)

    @parameterized.expand(
        [
            ("name", "Имя"),
            ("mail", "Почта"),
        ],
    )
    def test_correct_labels(self, field, label):
        url = django.urls.reverse("feedback:feedback")
        response = django.test.Client().get(url)
        form = response.context["feedback_author"]
        self.assertEqual(form[field].label, label)

    @parameterized.expand(
        [
            ("name", "Ваше имя"),
            ("mail", "Введите вашу почту"),
        ],
    )
    def test_correct_help_text(self, field, help_text):
        url = django.urls.reverse("feedback:feedback")
        response = django.test.Client().get(url)
        form = response.context["feedback_author"]
        self.assertEqual(form[field].help_text, help_text)

    def test_feedback_form_error(self):
        url = django.urls.reverse("feedback:feedback")
        data = {
            "name": "Mike",
            "text": "Test",
            "mail": "test@incorrect",
        }
        response = django.test.Client().post(url, data)

        self.assertFormError(
            response.context["feedback_author"],
            "mail",
            ["Введите правильный адрес электронной почты."],
        )


class FeedbackURLTests(django.test.TestCase):

    def test_feedback_create(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Test",
            "text": "Test",
            "mail": "test@yandex.ru",
        }

        self.assertFalse(
            feedback.models.Feedback.objects.filter(
                text="Test",
            ).exists(),
        )

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count + 1,
        )

        self.assertTrue(
            feedback.models.Feedback.objects.filter(
                text="Test",
            ).exists(),
        )

        self.assertIn("messages", response.context.keys())
        self.assertEqual(
            list(response.context.get("messages"))[0].message,
            "Все прошло успешно",
        )

    @django.test.override_settings(
        MEDIA_ROOT=tempfile.TemporaryDirectory().name,
    )
    def test_file_upload(self):
        files = [
            django.core.files.base.ContentFile(
                f"file_{index}".encode(),
                name="filename",
            )
            for index in range(10)
        ]

        form_data = {
            "name": "Test",
            "text": "file_test",
            "mail": "test@yandex.ru",
            "files": files,
        }

        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )


class FeedbackModelTests(django.test.TestCase):
    def test_feedback_model_save(self):
        feedback_model_count = feedback.models.Feedback.objects.count()
        url = django.urls.reverse("feedback:feedback")
        data = {
            "name": "Mike",
            "text": "Test",
            "mail": "test@yandex.ru",
        }
        django.test.Client().post(url, data)

        self.assertEqual(
            feedback_model_count + 1,
            feedback.models.Feedback.objects.count(),
        )
        feedback_item = feedback.models.Feedback.objects.first()
        self.assertTrue(feedback_item)


__all__ = []
