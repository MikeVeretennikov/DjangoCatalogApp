import django.test
import django.urls

import feedback.models


class FeedbackFormTests(django.test.TestCase):

    def test_unable_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Тест",
            "text": "Тест",
            "mail": "notmail",
        }

        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count,
        )

    def test_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Тест",
            "text": "Тест",
            "mail": "123@l.com",
        }

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


__all__ = []