import http

import django.core.exceptions
from django.test import Client, TestCase
from parameterized import parameterized

import catalog.models
import catalog.validators


class CatalogStaticURLTests(TestCase):
    def test_catalog_index_endpoint_correct(self):
        response = Client().get("/catalog/")
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Status code should be 200",
        )


class CatalogReEndpointURLTests(TestCase):
    @parameterized.expand(["1", "01", "010", "10", "100", "001", "99999999"])
    def test_catalog_re_converter_endpoint_correct(self, path):
        response = Client().get(f"/catalog/re/{path}/")
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Ints with leading zeroes are correct",
        )

    @parameterized.expand(
        [
            "0",
            "-1",
            "-99999999",
            "-0",
            "10.1",
            "0.123",
            "0,123",
            "1a23",
            "a123",
            "123a",
        ],
    )
    def test_catalog_re_converter_endpoint_incorrect(self, path):
        response = Client().get(f"/catalog/re/{path}/")
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.NOT_FOUND,
            "Some bad ints are valid for current regex",
        )


class CatalogConverterEndpointURLTests(TestCase):
    @parameterized.expand(
        [
            "1",
            "01",
            "010",
            "10",
            "100",
            "001",
            "99999999",
        ],
    )
    def test_catalog_re_converter_endpoint_correct(self, path):
        response = Client().get(f"/catalog/converter/{path}/")
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Ints with leading zeroes are correct",
        )

    @parameterized.expand(
        [
            "0",
            "-1",
            "-99999999",
            "-0",
            "10.1",
            "0.123",
            "0,123",
            "1a23",
            "a123",
            "123a",
        ],
    )
    def test_catalog_re_converter_endpoint_incorrect(self, path):
        response = Client().get(f"/catalog/converter/{path}/")
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.NOT_FOUND,
            "Some bad ints are valid for current regex",
        )


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
        [("абоба", "абоба"), ("аБО.,-_!?бА", "абоба"), ("AbOBa", "авова")],
    )
    def test_normalize_correct(self, input, expected):
        self.assertEqual(catalog.models.normalize(input), expected)


class CatalogNormalizationValidationTests(TestCase):
    def test_collision(self):
        tag = catalog.models.Tag(
            is_published=True,
            name="KомпрOм_аt.",
            slug="test-tag-slug",
        )
        tag.full_clean()
        tag.save()
        item_count = catalog.models.Tag.objects.count()
        tag2 = catalog.models.Tag(
            is_published=True,
            name="компромат",
            slug="test-tag-slug2",
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            tag2.full_clean()
            tag2.save()
        self.assertEqual(item_count, catalog.models.Tag.objects.count())
