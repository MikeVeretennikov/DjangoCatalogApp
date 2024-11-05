import django.core.exceptions
from django.test import TestCase
from parameterized import parameterized

import catalog.models
import catalog.validators


class CatalogModelItemTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="test_category",
            slug="test-category-slug",
            weight=100,
        )

        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="test_tag",
            slug="test-tag-slug",
        )

    def test_item_create(self):
        item_count = catalog.models.Item.objects.count()

        item = catalog.models.Item(
            name="name",
            text="превосходно text",
            category=CatalogModelItemTests.category,
        )

        item.full_clean()
        item.save()
        item.tags.add(CatalogModelItemTests.tag)
        self.assertEqual(catalog.models.Item.objects.count(), item_count + 1)

    def test_validator_error_no_perfect_item_create(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="name",
                text="text",
                category=self.category,
            )

            self.item.full_clean()
            self.item.save()
            self.item.tags.add(CatalogModelItemTests.tag)

        self.assertEqual(catalog.models.Item.objects.count(), item_count)

    def test_validator_error_not_string_item_create(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="name",
                text=123,
                category=self.category,
            )

            self.item.full_clean()
            self.item.save()
            self.item.tags.add(CatalogModelItemTests.tag)

        self.assertEqual(catalog.models.Item.objects.count(), item_count)


class CatalogModelCatalogTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="test_category",
            slug="test-category-slug",
            weight=100,
        )

        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="test_tag",
            slug="test-tag-slug",
        )

    def test_category_create(self):
        category_count = catalog.models.Category.objects.count()

        category = catalog.models.Category(
            is_published=True,
            name="name",
            slug="text-slug",
            weight=100,
        )
        category.full_clean()
        category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
        )

    def test_validator_error_slug_category_create(self):
        category_count = catalog.models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            category = catalog.models.Category(
                is_published=True,
                name="name",
                slug="абоба)",
                weight=100,
            )
            category.full_clean()
            category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )

    def test_validator_error_weight_category_create(self):

        category_count = catalog.models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            category = catalog.models.Category(
                is_published=True,
                name="name",
                slug="text-slug",
                weight=-100,
            )
            category.full_clean()
            category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )


class CatalogModelTagTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="test_category",
            slug="test-category-slug",
            weight=100,
        )

        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="test_tag",
            slug="test-tag-slug",
        )

    def test_tag_create(self):
        tag_count = catalog.models.Tag.objects.count()
        tag = catalog.models.Tag(name="name", slug="text-slug")
        tag.full_clean()
        tag.save()
        self.assertEqual(catalog.models.Tag.objects.count(), tag_count + 1)

    def test_validator_error_slug_tag_create(self):
        tag_count = catalog.models.Tag.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            tag = catalog.models.Tag(name="name", slug="абоба)")
            tag.full_clean()
            tag.save()

        self.assertEqual(catalog.models.Category.objects.count(), tag_count)


class CatalogValidatorPositiveIntTests(TestCase):
    @parameterized.expand([1, 1241, 32767])
    def test_correct_intpositive_validator(self, num):
        catalog.validators.validate_int_from_1_to_32767(num)

    @parameterized.expand([-1, 0, 32768, -32676, 199.3])
    def test_incorrect_intpositive_validator(self, num):
        with self.assertRaises(django.core.exceptions.ValidationError):
            catalog.validators.validate_int_from_1_to_32767(num)


class CatalogValidatorPerfectInTextTests(TestCase):
    @parameterized.expand(
        [
            "Роскошно",
            "роскошно!",
            "роскошно\\",
            "роскошно.",
            "роскошно",
            "все очень роскошно",
            "Превосходно",
            "превосходно!",
            "!роскошно\\",
            ",,,,,,роскошно...",
            "   роскоШно   ",
            "'роскошно'",
            "(роскошно)",
            "...роскошно...роскsadfsошно",
            "роскошно'",
            "роскошно!авыа",
            "аываыо!роскошно",
            "sdfsdfsdf sп прев а превосходно авыаываываыва123",
        ],
    )
    def test_validator_correct(self, text):
        catalog.validators.validate_perfect_in_text(text)

    @parameterized.expand(
        [
            "рРоскошно",
            "ороскошно",
            "роскошноо",
            "пПревосходно",
            "Ппревосходно",
            "превороскошноабоба",
            "роскопревосходноабоба",
        ],
    )
    def test_validator_incorrect(self, text):
        with self.assertRaises(
            django.core.exceptions.ValidationError,
            msg=text,
        ):
            catalog.validators.validate_perfect_in_text(text)


class CatalogClassValidatorMustContaintTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.validator = catalog.validators.ValidateMustContain(
            "роскошно",
            "превосходно",
        )

    @parameterized.expand(
        [
            "Роскошно",
            "роскошно!",
            "роскошно\\",
            "роскошно.",
            "роскошно",
            "все очень роскошно",
            "Превосходно",
            "превосходно!",
            "!роскошно\\",
            ",,,,,,роскошно...",
            "   роскоШно   ",
            "'роскошно'",
            "(роскошно)",
            "...роскошно...роскsadfsошно",
            "роскошно'",
            "роскошно!авыа",
            "аываыо!роскошно",
            "sdfsdfsdf sп прев а превосходно авыаываываыва123",
        ],
    )
    def test_validator_correct(self, text):
        CatalogClassValidatorMustContaintTests.validator(text)

    @parameterized.expand(
        [
            "рРоскошно",
            "ороскошно",
            "роскошноо",
            "пПревосходно",
            "Ппревосходно",
            "превороскошноабоба",
            "роскопревосходноабоба",
        ],
    )
    def test_validator_incorrect(self, text):
        with self.assertRaises(
            django.core.exceptions.ValidationError,
            msg=text,
        ):
            CatalogClassValidatorMustContaintTests.validator(text)


class CatalogNormalizeTests(TestCase):
    @parameterized.expand(
        [
            (
                "абоба",
                "aboba",
            ),  # contains english letters, must become russian
            ("аБО.,-_!?бА", "abo_ba"),
            (
                "AbOBa",
                "aboba",
            ),  # contains english letters, must become russian
            ("aбOбa123))__!@#", "aboba123__"),
            (
                "MmmeeETtt",
                "mmmeeettt",
            ),  # contains english letters, must become russian
        ],
    )
    def test_normalize_correct(self, text, expected):
        self.assertEqual(catalog.models.normalize(text), expected)

    @parameterized.expand(
        [("bBb", "бБб"), ("абоба123", "абоба")],
    )
    def test_normalize_incorrect(self, text, expected):
        self.assertNotEqual(catalog.models.normalize(text), expected)


class CatalogNormalizationValidationTests(TestCase):
    def test_normalization_name_collision(self):
        tag = catalog.models.Tag(
            is_published=True,
            name="KомпрOмаt.",
            slug="test-tag-slug",
        )
        tag.full_clean()
        tag.save()
        item_count = catalog.models.Tag.objects.count()
        not_unique_tag = catalog.models.Tag(
            is_published=True,
            name="компромат",
            slug="test-tag-slug2",
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            not_unique_tag.full_clean()
            not_unique_tag.save()

        self.assertEqual(item_count, catalog.models.Tag.objects.count())

    def test_no_normalization_name_collision(self):
        tag = catalog.models.Tag(
            is_published=True,
            name="KомпрOмаt.",
            slug="test-tag-slug",
        )
        tag.full_clean()
        tag.save()
        item_count = catalog.models.Tag.objects.count()
        unique_tag = catalog.models.Tag(
            is_published=True,
            name="компроматы",
            slug="test-tag-slug2",
        )

        unique_tag.full_clean()
        unique_tag.save()
        self.assertEqual(item_count + 1, catalog.models.Tag.objects.count())


__all__ = []
