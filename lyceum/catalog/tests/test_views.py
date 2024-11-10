import django.db.models.query
from django.test import Client, TestCase
from django.urls import reverse

import catalog.models


class CatalogURLTests(TestCase):
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

        cls.unpublished_item_is_on_main_2 = catalog.models.Item.objects.create(
            name="тестовый айтем с is_on_main=True, is_published=False",
            category=cls.published_category,
            text="роскошно",
            is_on_main=True,
            is_published=False,
        )

        cls.unpublished_item_is_not_on_main.tags.add(cls.unpublished_tag)
        cls.published_item_is_on_main.tags.add(cls.published_tag)
        cls.unpublished_item_is_on_main_2.tags.add(cls.published_tag)

    def test_correct_item_detail(self):
        response = Client().get(
            reverse(
                "catalog:default-converter-page",
                kwargs={"pk": 2},
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_catalog_correct_context(self):
        response = Client().get(reverse("catalog:index-page"))
        self.assertIn("items", response.context)

    def test_catalog_correct_context_type(self):
        response = Client().get(reverse("catalog:index-page"))
        self.assertEqual(
            type(response.context["items"]),
            django.db.models.query.QuerySet,
        )

    def test_catalog_correct_context_content(
        self,
    ):
        response = Client().get(reverse("catalog:index-page"))
        self.assertEqual(len(response.context["items"]), 1)
        item = response.context["items"].first()
        self.assertIsInstance(item.name, str)
        self.assertIsInstance(item.is_on_main, bool)
        self.assertIsInstance(item.is_published, bool)
        self.assertEqual(item.is_published, True)
        self.assertIsInstance(item.category, catalog.models.Category)

    def test_correct_prefetch_context(self):
        response = Client().get(reverse("catalog:index-page"))
        item = response.context["items"].all()[0]
        self.assertIn(
            "_prefetched_objects_cache",
            item.__dict__,
        )

    def test_item_detail_not_found(self):
        response = Client().get(
            reverse(
                "catalog:default-converter-page",
                args=[5],
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_no_extra_fields(self):
        response = Client().get(reverse("catalog:index-page"))
        item = response.context["items"].first()
        self.assertNotIn("is_published", item.__dict__)
        self.assertNotIn("is_published", item.category.__dict__)
        for tag in item.tags.all():
            self.assertNotIn("is_published", tag.__dict__)

    def test_friday_items_view(self):
        response = self.client.get(reverse("catalog:friday-page"))
        self.assertEqual(response.status_code, 200)

    def test_new_items_view(self):
        response = self.client.get(reverse("catalog:new-page"))
        self.assertEqual(response.status_code, 200)

    def test_unverified_items_view(self):
        response = self.client.get(reverse("catalog:unverified-page"))
        self.assertEqual(response.status_code, 200)


__all__ = []
