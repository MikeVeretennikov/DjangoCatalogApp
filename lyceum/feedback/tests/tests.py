import django.test
import django.urls
from parameterized import parameterized

import feedback.models


class FeedbackTests(django.test.TestCase):

    def test_form_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        self.assertIn("form", response.context)

    @parameterized.expand(
        [("name", "Имя"), ("text", "Текст"), ("mail", "Почта")],
    )
    def test_correct_labels(self, field, label):
        url = django.urls.reverse("feedback:feedback")
        response = django.test.Client().get(url)
        form = response.context["form"]
        self.assertEqual(form[field].label, label)

    @parameterized.expand(
        [
            ("name", "Ваше имя"),
            ("text", "Введите текст обращения"),
            ("mail", "Введите вашу почту"),
        ],
    )
    def test_correct_help_text(self, field, help_text):
        url = django.urls.reverse("feedback:feedback")
        response = django.test.Client().get(url)
        form = response.context["form"]
        self.assertEqual(form[field].help_text, help_text)

    def test_feedback_redirects(self):
        url = django.urls.reverse("feedback:feedback")
        data = {
            "name": "Mike",
            "text": "Test",
            "mail": "test@yandex.ru",
        }
        response = django.test.Client().post(url, data, follow=True)

        self.assertRedirects(
            response,
            url,
            status_code=302,
            target_status_code=200,
        )

        self.assertIn("messages", response.context.keys())
        self.assertEqual(
            list(response.context.get("messages"))[0].message,
            "Все прошло успешно",
        )

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

    def test_feedback_form_error(self):
        url = django.urls.reverse("feedback:feedback")
        data = {
            "name": "Mike",
            "text": "Test",
            "mail": "test@incorrect",
        }
        response = django.test.Client().post(url, data)

        self.assertFormError(
            response.context["form"],
            "mail",
            ["Введите правильный адрес электронной почты."],
        )


__all__ = []
