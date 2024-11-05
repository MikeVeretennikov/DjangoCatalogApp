import django.test
import django.urls
from parameterized import parameterized

import feedback.models


class FeedbackFormTests(django.test.TestCase):

    def test_form_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback-page"),
        )
        self.assertIn("form", response.context)

    @parameterized.expand(
        [("name", "Имя"), ("text", "Текст"), ("mail", "Почта")],
    )
    def test_correct_labels(self, field, label):
        url = django.urls.reverse("feedback:feedback-page")
        response = django.test.Client().get(url)
        form = response.context["form"]
        self.assertEqual(form[field].label, label)

    def test_feedback_redirects(self):
        url = django.urls.reverse("feedback:feedback-page")
        data = {
            "name": "Mike",
            "text": "Test",
            "mail": "test@yandex.ru",
        }
        response = django.test.Client().post(url, data)

        self.assertRedirects(response, url)

    def test_feedback_model_save(self):
        feedback_model_count = feedback.models.Feedback.objects.count()
        url = django.urls.reverse("feedback:feedback-page")
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


__all__ = []
