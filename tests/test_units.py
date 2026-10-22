import unittest
from app import create_app
from config import TestConfig
from models import db
from models.user import User, Role, UserRole
from models.geography import Country, Continent
from services.search_service import SearchService
from services.geographic_service import GeographicService
from services.data_import_service import DataImportService

class UnitTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_country_code_and_slug_handling(self):
        cont = Continent(name="Asia", slug="asia", code="AS")
        db.session.add(cont)
        db.session.flush()

        india = Country(
            iso_a2="IN", iso_a3="IND", common_name="India",
            official_name="Republic of India", slug="india",
            continent_id=cont.id, area_km2=3287263, population=1428627663
        )
        db.session.add(india)
        db.session.commit()

        # Lookup by lowercase slug
        by_slug = GeographicService.get_country_by_slug("india")
        self.assertIsNotNone(by_slug)
        self.assertEqual(by_slug.common_name, "India")

        # Lookup by ISO-2 (lowercase and uppercase)
        by_iso2 = GeographicService.get_country_by_slug("in")
        self.assertIsNotNone(by_iso2)
        self.assertEqual(by_iso2.iso_a3, "IND")

        # Lookup by ISO-3
        by_iso3 = GeographicService.get_country_by_slug("IND")
        self.assertIsNotNone(by_iso3)
        self.assertEqual(by_iso3.common_name, "India")

    def test_missing_data_handling(self):
        """Verify that missing values are preserved as None rather than defaulted to zero."""
        cont = Continent(name="Europe", slug="europe", code="EU")
        db.session.add(cont)
        db.session.flush()

        # Country without population or area specified
        c = Country(
            iso_a2="XX", iso_a3="XXX", common_name="Testland",
            official_name="Republic of Testland", slug="testland",
            continent_id=cont.id
        )
        db.session.add(c)
        db.session.commit()

        retrieved = GeographicService.get_country_by_slug("testland")
        self.assertIsNone(retrieved.population)
        self.assertIsNone(retrieved.area_km2)
        self.assertIsNone(retrieved.highest_elevation_m)

    def test_password_hashing_and_verification(self):
        user = User(username="test_traveler", email="traveler@example.com")
        user.set_password("SecureGeoPass2026!")
        self.assertNotEqual(user.password_hash, "SecureGeoPass2026!")
        self.assertTrue(user.check_password("SecureGeoPass2026!"))
        self.assertFalse(user.check_password("WrongPassword"))

    def test_role_and_permission_enforcement(self):
        admin_role = Role(name="Administrator")
        reg_role = Role(name="Registered User")
        db.session.add_all([admin_role, reg_role])
        db.session.flush()

        user = User(username="standard_user", email="user@example.com")
        user.set_password("pass12345")
        admin = User(username="admin_user", email="admin@example.com")
        admin.set_password("adminpass123")
        db.session.add_all([user, admin])
        db.session.flush()

        db.session.add(UserRole(user_id=user.id, role_id=reg_role.id))
        db.session.add(UserRole(user_id=admin.id, role_id=admin_role.id))
        db.session.commit()

        self.assertFalse(user.is_admin)
        self.assertTrue(admin.is_admin)

    def test_geojson_validator_service(self):
        # Invalid JSON
        res_invalid = DataImportService.validate_and_import_geojson("not json")
        self.assertFalse(res_invalid["success"])

        # Valid GeoJSON FeatureCollection
        valid_payload = '''{
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Lilliput"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[10, 10], [20, 10], [20, 20], [10, 20], [10, 10]]]
                    }
                }
            ]
        }'''
        res_valid = DataImportService.validate_and_import_geojson(valid_payload)
        self.assertTrue(res_valid["success"])
        self.assertEqual(res_valid["validated_count"], 1)

if __name__ == "__main__":
    unittest.main()
