import http

from django.test import Client, TestCase
from parameterized import parameterized


class StaticURLTests(TestCase):
    def test_catalog_index_endpoint_correct(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)


class CatalogEndpointURLTests(TestCase):
    def test_catalog_converter_endpoint_correct(self):
        response = Client().get("/catalog/100/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_catalog_converter_endpoint_incorrect(self):
        response = Client().get("/catalog/-1/")
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)


class CatalogReEndpointURLTests(TestCase):
    @parameterized.expand(
        [
            ("1"),
            ("01"),
            ("010"),
            ("10"),
            ("100"),
            ("001"),
            ("99999999"),
        ]
    )
    def test_catalog_re_converter_endpoint_correct(self, path):
        response = Client().get(f"/catalog/re/{path}/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @parameterized.expand(
        [
            ("0"),
            ("-1"),
            ("-99999999"),
            ("-0"),
            ("10.1"),
            ("0.123"),
            ("0,123"),
            ("1a23"),
            ("a123"),
            ("123a"),
        ]
    )
    def test_catalog_re_converter_endpoint_incorrect(self, path):
        response = Client().get(f"/catalog/re/{path}/")
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)


class CatalogConverterEndpointURLTests(TestCase):
    @parameterized.expand(
        [
            ("1"),
            ("01"),
            ("010"),
            ("10"),
            ("100"),
            ("001"),
            ("99999999"),
        ]
    )
    def test_catalog_re_converter_endpoint_correct(self, path):
        response = Client().get(f"/catalog/converter/{path}/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @parameterized.expand(
        [
            ("0"),
            ("-1"),
            ("-99999999"),
            ("-0"),
            ("10.1"),
            ("0.123"),
            ("0,123"),
            ("1a23"),
            ("a123"),
            ("123a"),
        ]
    )
    def test_catalog_re_converter_endpoint_incorrect(self, path):
        response = Client().get(f"/catalog/converter/{path}/")
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)
