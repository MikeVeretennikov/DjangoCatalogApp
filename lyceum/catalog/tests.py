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
            ("1", http.HTTPStatus.OK),
            ("001", http.HTTPStatus.OK),
            ("99999999", http.HTTPStatus.OK),
        ]
    )
    def test_catalog_re_converter_endpoint_correct(self, path, expected):
        response = Client().get(f"/catalog/re/{path}/")
        self.assertEqual(response.status_code, expected)

    @parameterized.expand(
        [
            ("0", http.HTTPStatus.NOT_FOUND),
            ("-1", http.HTTPStatus.NOT_FOUND),
            ("-99999999", http.HTTPStatus.NOT_FOUND),
        ]
    )
    def test_catalog_re_converter_endpoint_incorrect(self, path, expected):
        response = Client().get(f"/catalog/re/{path}/")
        self.assertEqual(response.status_code, expected)


class CatalogConverterEndpointURLTests(TestCase):
    @parameterized.expand(
        [
            ("1", http.HTTPStatus.OK),
            ("001", http.HTTPStatus.OK),
            ("99999999", http.HTTPStatus.OK),
            ("100", http.HTTPStatus.OK),
        ]
    )
    def test_catalog_re_converter_endpoint_correct(self, path, expected):
        response = Client().get(f"/catalog/converter/{path}/")
        self.assertEqual(response.status_code, expected)

    @parameterized.expand(
        [
            ("0", http.HTTPStatus.NOT_FOUND),
            ("-1", http.HTTPStatus.NOT_FOUND),
            ("-99999999", http.HTTPStatus.NOT_FOUND),
        ]
    )
    def test_catalog_re_converter_endpoint_incorrect(self, path, expected):
        response = Client().get(f"/catalog/converter/{path}/")
        self.assertEqual(response.status_code, expected)
