import unittest
from app import create_app
from config import TestConfig
from models import db
from database.seed_data import run_all_seeds

class IntegrationRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        run_all_seeds(self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page_loads_with_db_statistics(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"One Planet. Endless Discoveries.", response.data)
        self.assertIn(b"Cataloged Countries", response.data)

    def test_countries_catalog_and_detail(self):
        # Catalog
        res_list = self.client.get("/countries")
        self.assertEqual(res_list.status_code, 200)
        self.assertIn(b"India", res_list.data)

        # Country Detail
        res_country = self.client.get("/countries/india")
        self.assertEqual(res_country.status_code, 200)
        self.assertIn(b"Republic of India", res_country.data)
        self.assertIn(b"New Delhi", res_country.data)
        self.assertIn(b"Indian Rupee", res_country.data)

    def test_administrative_divisions(self):
        res_div = self.client.get("/countries/india/divisions/maharashtra")
        self.assertEqual(res_div.status_code, 200)
        self.assertIn(b"Maharashtra", res_div.data)
        self.assertIn(b"Mumbai", res_div.data)

    def test_oceans_and_seas(self):
        # Ocean Detail
        res_ocean = self.client.get("/oceans/indian-ocean")
        self.assertEqual(res_ocean.status_code, 200)
        self.assertIn(b"Indian Ocean", res_ocean.data)

        # Sea Detail
        res_sea = self.client.get("/seas/arabian-sea")
        self.assertEqual(res_sea.status_code, 200)
        self.assertIn(b"Arabian Sea", res_sea.data)

    def test_rest_api_search_and_countries(self):
        res_api_search = self.client.get("/api/search?q=ind")
        self.assertEqual(res_api_search.status_code, 200)
        json_data = res_api_search.get_json()
        self.assertEqual(json_data["status"], "success")
        self.assertTrue(len(json_data["data"]) > 0)

        res_api_country = self.client.get("/api/countries/IND")
        self.assertEqual(res_api_country.status_code, 200)
        data = res_api_country.get_json()["data"]
        self.assertEqual(data["common_name"], "India")
        self.assertEqual(data["capital"], "New Delhi")

    def test_unauthorized_admin_access_denied(self):
        # Guest accessing /admin/dashboard should be redirected to login
        res_guest = self.client.get("/admin/dashboard")
        self.assertEqual(res_guest.status_code, 302)

if __name__ == "__main__":
    unittest.main()
