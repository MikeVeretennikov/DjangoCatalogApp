from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_index_endpoint_correct(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)


class DynamicURLTests(TestCase):
    def test_catalog_converter_endpoint_correct(self):
        response = Client().get("/catalog/11/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_converter_endpoint_incorrect(self):
        response = Client().get("/catalog/-1/")
        self.assertEqual(response.status_code, 404)

    def test_catalog_re_converter_endpoint_correct(self):
        response = Client().get("/catalog/re/1/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_re_converter_endpoint_incorrect_1(self):
        response = Client().get("/catalog/re/0/")
        self.assertEqual(response.status_code, 404)

    def test_catalog_re_converter_endpoint_incorrect_2(self):
        response = Client().get("/catalog/re/-1/")
        self.assertEqual(response.status_code, 404)

    def test_catalog_custom_converter_endpoint_correct(self):
        response = Client().get("/catalog/converter/1/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_custom_converter_endpoint_incorrect_1(self):
        response = Client().get("/catalog/converter/0/")
        self.assertEqual(response.status_code, 404)

    def test_catalog_custom_converter_endpoint_incorrect_2(self):
        response = Client().get("/catalog/converter/-1/")
        self.assertEqual(response.status_code, 404)
