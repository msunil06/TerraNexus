import unittest
from app import create_app
from config import TestConfig
from models import db
from models.user import User, Role, UserRole, UserFavorite
from database.seed_data import run_all_seeds

class EndToEndJourneyTestCase(unittest.TestCase):
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

    def test_full_user_journey(self):
        # 1. Open Home Page
        res_home = self.client.get("/")
        self.assertEqual(res_home.status_code, 200)

        # 2. Search for India via API
        res_search = self.client.get("/api/search?q=India")
        self.assertEqual(res_search.status_code, 200)
        search_results = res_search.get_json()["data"]
        self.assertTrue(any("India" in r["title"] for r in search_results))

        # 3. View India's country details page
        res_india = self.client.get("/countries/india")
        self.assertEqual(res_india.status_code, 200)

        # 4. View capital, currency, languages
        self.assertIn(b"New Delhi", res_india.data)
        self.assertIn(b"Indian Rupee", res_india.data)
        self.assertIn(b"Hindi", res_india.data)

        # 5. Open state and district
        res_state = self.client.get("/countries/india/divisions/maharashtra")
        self.assertEqual(res_state.status_code, 200)
        self.assertIn(b"Maharashtra", res_state.data)
        self.assertIn(b"Pune", res_state.data)

        # 6. Explore neighboring countries API
        res_neighbors = self.client.get("/api/countries/IND/neighbors")
        self.assertEqual(res_neighbors.status_code, 200)
        neighbors_list = res_neighbors.get_json()["data"]
        self.assertTrue(len(neighbors_list) > 0)

        # 7. Open Arabian Sea page
        res_sea = self.client.get("/seas/arabian-sea")
        self.assertEqual(res_sea.status_code, 200)
        self.assertIn(b"Arabian Sea", res_sea.data)

        # 8. Register an account
        res_register = self.client.post("/register", data={
            "username": "journey_user",
            "email": "journey@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "display_name": "Journey Explorer"
        }, follow_redirects=True)
        self.assertEqual(res_register.status_code, 200)

        # 9. Log in
        self.client.get("/logout", follow_redirects=True)
        res_login = self.client.post("/login", data={
            "login_id": "journey_user",
            "password": "Password123!"
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b"Journey Explorer", res_login.data)

        # 10. Save a favorite country via API
        res_fav = self.client.post("/api/me/favorites", json={
            "item_type": "country",
            "item_id": "india",
            "item_title": "India"
        })
        self.assertEqual(res_fav.status_code, 200)
        self.assertTrue(res_fav.get_json()["favorited"])

        # View favorites page
        res_fav_page = self.client.get("/favorites")
        self.assertEqual(res_fav_page.status_code, 200)
        self.assertIn(b"India", res_fav_page.data)

        # 11. Log out and log in again
        self.client.get("/logout", follow_redirects=True)
        res_relogin = self.client.post("/login", data={
            "login_id": "journey@example.com",
            "password": "Password123!"
        }, follow_redirects=True)
        self.assertEqual(res_relogin.status_code, 200)

        # 12. Attempt unauthorized admin action and receive denial (403)
        res_admin_denial = self.client.get("/admin/dashboard")
        self.assertEqual(res_admin_denial.status_code, 403)

        # 13. Sign in as authorized administrator and manage allowed test account
        self.client.get("/logout", follow_redirects=True)
        res_admin_login = self.client.post("/login", data={
            "login_id": "admin",
            "password": "Admin@TerraNexus2026!"
        }, follow_redirects=True)
        self.assertEqual(res_admin_login.status_code, 200)

        # Admin dashboard access
        res_admin_dash = self.client.get("/admin/dashboard")
        self.assertEqual(res_admin_dash.status_code, 200)
        self.assertIn(b"Platform Operations Overview", res_admin_dash.data)

        # Manage user: Toggle suspension of journey_user
        test_user = User.query.filter_by(username="journey_user").first()
        res_suspend = self.client.post(f"/admin/users/{test_user.id}/toggle-suspend", data={
            "reason": "Test E2E hold"
        }, follow_redirects=True)
        self.assertEqual(res_suspend.status_code, 200)

        test_user_reloaded = User.query.filter_by(username="journey_user").first()
        self.assertTrue(test_user_reloaded.is_suspended)

if __name__ == "__main__":
    unittest.main()
