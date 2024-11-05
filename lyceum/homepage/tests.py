import http

import django.conf
import django.db.models.query
from django.test import Client, TestCase
from django.urls import reverse

import catalog.models


class HomepageURLTests(TestCase):
    @classmethod
    def setUp(cls):
        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name="тестовая опубликованная категория",
            slug="test-true",
            weight=100,
        )
        cls.unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name="тестовая неопубликованная категория",
            slug="test-false",
            weight=100,
        )

        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name="тестовый опубликованный тег",
            slug="test-true",
        )
        cls.unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name="тестовый неопубликованный тег",
            slug="test-false",
        )

        cls.unpublished_item_is_not_on_main = (
            catalog.models.Item.objects.create(
                name="тестовый айтем с is_on_main=False, is_published=False",
                category=cls.unpublished_category,
                text="роскошно",
                is_on_main=False,
                is_published=False,
            )
        )
        cls.published_item_is_on_main = catalog.models.Item.objects.create(
            name="тестовый айтем с is_on_main=True, is_published=True",
            category=cls.published_category,
            text="роскошно",
            is_on_main=True,
            is_published=True,
        )

        cls.published_item_is_on_main = catalog.models.Item.objects.create(
            name="тестовый 2 айтем с is_on_main=True, is_published=True",
            category=cls.published_category,
            text="роскошно",
            is_on_main=True,
            is_published=True,
        )

        cls.unpublished_item_is_not_on_main.tags.add(cls.unpublished_tag)
        cls.published_item_is_on_main.tags.add(cls.published_tag)

    def test_homepage_correct_context(self):
        response = Client().get(reverse("homepage:index-page"))
        self.assertIn("items", response.context)

    def test_homepage_correct_context_type(self):
        response = Client().get(reverse("homepage:index-page"))
        self.assertEqual(
            type(response.context["items"]),
            django.db.models.query.QuerySet,
        )

    def test_correct_prefetch_context(self):
        response = Client().get(reverse("homepage:index-page"))
        item = response.context["items"].all()[0]
        self.assertIn("_prefetched_objects_cache", item.__dict__)

    def test_homepage_correct_context_content(self):
        response = Client().get(reverse("homepage:index-page"))

        self.assertEqual(len(response.context["items"]), 2)
        item = response.context["items"].first()
        self.assertIsInstance(item.name, str)
        self.assertIsInstance(item.is_on_main, bool)
        self.assertEqual(item.is_on_main, True)
        self.assertIsInstance(item.is_published, bool)
        self.assertIsInstance(item.category, catalog.models.Category)

    def test_coffee_endpoint_correct_text(self):
        responses = []

        for _ in range(10):
            responses.append(
                Client().get(reverse("homepage:coffee-page")).content.decode(),
            )

        if django.conf.settings.ALLOW_REVERSE:
            self.assertIn(
                "Я кинйач",
                responses,
                "Text should be 'Я чайник' reversed"
                "because ALLOW_REVERSE is True",
            )
        else:
            self.assertIn("Я чайник", responses, "Text should be 'Я чайник'")

    def test_coffee_endpoint_correct_status_code(self):
        response = Client().get(reverse("homepage:coffee-page"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.IM_A_TEAPOT,
            "Status code should be 418",
        )

    def test_no_extra_fields(self):
        response = Client().get(reverse("homepage:index-page"))
        item = response.context["items"].first()
        self.assertNotIn("is_published", item.__dict__)
        self.assertNotIn("is_published", item.category.__dict__)
        for tag in item.tags.all():
            self.assertNotIn("is_published", tag.__dict__)

    def test_echo_submit_page(self):
        response = Client().get(reverse("homepage:echo-submit-page"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.METHOD_NOT_ALLOWED,
        )

    def test_echo_page(self):
        data = {"text": "test text"}
        response = Client().post(reverse("homepage:echo-page"), data)
        self.assertEqual(response.status_code, 405)


__all__ = []
