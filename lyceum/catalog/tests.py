from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def test_catalog_index_endpoint_correct(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)
    
    def test_catalog_converter_endpoint_correct(self):
        response = Client().get("/catalog/11/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_converter_endpoint_incorrect(self):
        response = Client().get("/catalog/-1/")
        self.assertEqual(response.status_code, 404)