import http

from django.test import Client, TestCase
from django.urls import exceptions, reverse
from parameterized import parameterized


class CatalogStaticURLTests(TestCase):
    def test_catalog_index_endpoint_correct(self):
        response = Client().get(
            reverse("catalog:default-converter-page", args=[2]),
        )
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Status code should be 200",
        )


class CatalogReEndpointURLTests(TestCase):
    @parameterized.expand(["1", "01", "010", "10", "100", "001", "99999999"])
    def test_catalog_re_converter_endpoint_correct(self, path):
        response = Client().get(
            reverse("catalog:re-converter-page", args=[path]),
        )
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
        with self.assertRaises(exceptions.NoReverseMatch):
            reverse("catalog:re-converter-page", args=[path])


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
        response = Client().get(
            reverse("catalog:custom-converter-page", args=[path]),
        )
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
        with self.assertRaises(exceptions.NoReverseMatch):
            reverse("catalog:custom-converter-page", args=[path])


__all__ = []
