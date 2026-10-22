import unittest
from app import create_app
from config import TestConfig
from models import db
from models.user import User, Role, UserRole, UserSession
from models.geography import Country, Continent
from models.marine_and_physical import Ocean, GeographicFeature
from server.connection_manager import ServerConnectionManager
from api.config import API_REGISTRY, update_api_url, get_all_apis
from api.gateway import ApiGateway

class TestMapsAndAdminSecurity(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Seed roles
        self.admin_role = Role(name="System Administrator")
        self.user_role = Role(name="Registered User")
        db.session.add_all([self.admin_role, self.user_role])
        db.session.commit()

        # Seed admin user
        self.admin = User(username="superadmin", email="admin@terranexus.internal")
        self.admin.set_password("AdminSecurePass2026!")
        db.session.add(self.admin)
        db.session.commit()
        db.session.add(UserRole(user_id=self.admin.id, role_id=self.admin_role.id))

        # Seed regular user
        self.user = User(username="explorer_john", email="john@example.com")
        self.user.set_password("UserPass2026!")
        db.session.add(self.user)
        db.session.commit()
        db.session.add(UserRole(user_id=self.user.id, role_id=self.user_role.id))

        # Seed geography
        self.cont = Continent(name="Europe", slug="europe", code="EU", area_km2=10180000)
        db.session.add(self.cont)
        db.session.commit()

        self.country = Country(
            common_name="Iceland",
            official_name="Republic of Iceland",
            iso_a2="IS",
            iso_a3="ISL",
            slug="iceland",
            continent_id=self.cont.id,
            latitude=64.9631,
            longitude=-19.0208
        )
        self.ocean = Ocean(
            name="Arctic Ocean",
            slug="arctic-ocean",
            area_km2=14060000,
            avg_depth_m=1204,
            max_depth_m=5450,
            overview="The smallest and shallowest of the world's five major oceans."
        )
        self.island = GeographicFeature(
            name="Greenland",
            slug="greenland",
            feature_type="island",
            latitude=72.0,
            longitude=-40.0,
            overview="World largest non-continental island."
        )
        db.session.add_all([self.country, self.ocean, self.island])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # 1. Maps Section Tests
    def test_maps_hub_route(self):
        res = self.client.get("/maps")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Cartographic Atlas", res.data)

    def test_maps_world_route(self):
        res = self.client.get("/maps/world")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Interactive World Map", res.data)

    def test_maps_countries_gallery_and_detail(self):
        res = self.client.get("/maps/countries")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Country Maps Explorer", res.data)

        res_detail = self.client.get(f"/maps/countries/{self.country.slug}")
        self.assertEqual(res_detail.status_code, 200)
        self.assertIn(b"Iceland", res_detail.data)

    def test_maps_oceans_gallery_and_detail(self):
        res = self.client.get("/maps/oceans")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Ocean & Marine Maps", res.data)

        res_detail = self.client.get(f"/maps/oceans/{self.ocean.slug}")
        self.assertEqual(res_detail.status_code, 200)
        self.assertIn(b"Arctic Ocean", res_detail.data)

    def test_maps_islands_gallery_and_detail(self):
        res = self.client.get("/maps/islands")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"World Island & Archipelago Maps", res.data)

        res_detail = self.client.get(f"/maps/islands/{self.island.slug}")
        self.assertEqual(res_detail.status_code, 200)
        self.assertIn(b"Greenland", res_detail.data)

    # 2. Centralized API Registry Tests
    def test_api_registry_completeness(self):
        apis = API_REGISTRY
        self.assertGreaterEqual(len(apis), 10)
        self.assertIn("map_osm", apis)
        self.assertIn("weather", apis)
        self.assertIn("geocoding", apis)
        self.assertIn("forex", apis)
        self.assertIn("demographics", apis)

    def test_api_registry_hot_swap(self):
        original_url = API_REGISTRY["weather"]["url"]
        success = update_api_url("weather", "https://custom-meteo-mirror.internal/v1")
        self.assertTrue(success)
        self.assertEqual(API_REGISTRY["weather"]["url"], "https://custom-meteo-mirror.internal/v1")
        # Reset back
        update_api_url("weather", original_url)

    # 3. Server Connection Manager & Remote Disconnect Tests
    def test_server_connection_lifecycle(self):
        # Register a fake connection
        with self.app.test_request_context("/"):
            from flask import request
            token = ServerConnectionManager.register_connection(self.user, request)
            self.assertIsNotNone(token)
            
            # Connection should be valid
            valid = ServerConnectionManager.validate_connection(self.user)
            self.assertTrue(valid)

            # Get session
            session_rec = UserSession.query.filter_by(session_token=token).first()
            self.assertIsNotNone(session_rec)
            self.assertTrue(session_rec.is_active)

            # Disconnect session via admin
            success, msg = ServerConnectionManager.disconnect_session(session_rec.id, admin_user=self.admin)
            self.assertTrue(success)

            # Validation now returns False
            valid_after = ServerConnectionManager.validate_connection(self.user)
            self.assertFalse(valid_after)

    # 4. High-Security Admin Login & Authorization Tests
    def test_admin_login_portal_get(self):
        res = self.client.get("/admin/login")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Restricted Administrative Command", res.data)

    def test_regular_user_cannot_access_admin_portal(self):
        res = self.client.post("/admin/login", data={
            "login_id": "explorer_john",
            "password": "UserPass2026!"
        }, follow_redirects=True)
        self.assertIn(b"Access denied", res.data)

    def test_admin_successful_login(self):
        res = self.client.post("/admin/login", data={
            "login_id": "superadmin",
            "password": "AdminSecurePass2026!"
        }, follow_redirects=True)
        self.assertIn(b"Platform Operations Overview", res.data)

    def test_admin_user_profile_edit(self):
        # Log in as admin
        self.client.post("/admin/login", data={
            "login_id": "superadmin",
            "password": "AdminSecurePass2026!"
        })

        # Edit regular user's profile
        res = self.client.post(f"/admin/users/{self.user.id}/edit-profile", data={
            "username": "explorer_john_modified",
            "email": "john.new@example.com",
            "display_name": "Captain John",
            "bio": "Experienced navigator",
            "location": "Reykjavik, Iceland",
            "is_active_account": "on"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        updated_user = User.query.get(self.user.id)
        self.assertEqual(updated_user.username, "explorer_john_modified")
        self.assertEqual(updated_user.email, "john.new@example.com")
        self.assertEqual(updated_user.display_name, "Captain John")

    def test_admin_reset_user_password(self):
        # Log in as admin
        self.client.post("/admin/login", data={
            "login_id": "superadmin",
            "password": "AdminSecurePass2026!"
        })

        # Reset regular user's password
        res = self.client.post(f"/admin/users/{self.user.id}/reset-password", data={
            "new_password": "NewSuperSecretPassword99!"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        # Verify old password fails and new password succeeds
        user_check = User.query.get(self.user.id)
        self.assertFalse(user_check.check_password("UserPass2026!"))
        self.assertTrue(user_check.check_password("NewSuperSecretPassword99!"))

if __name__ == "__main__":
    unittest.main()
