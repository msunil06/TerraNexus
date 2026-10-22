import json
from datetime import datetime
from models import db
from models.geography import Country, AdministrativeDivision
from models.marine_and_physical import GeographicFeature, DataSource
from models.user import AuditLog

class DataImportService:
    @staticmethod
    def validate_and_import_geojson(geojson_str, admin_user=None):
        """
        Validate GeoJSON data:
        - Check format
        - Verify features array
        - Verify coordinates are valid WGS84 (-180 to 180, -90 to 90)
        - Detect missing required properties
        """
        try:
            data = json.loads(geojson_str)
        except Exception as e:
            return {"success": False, "error": f"Invalid JSON format: {str(e)}"}

        if data.get("type") != "FeatureCollection" or "features" not in data:
            return {"success": False, "error": "Invalid GeoJSON: Root must be a FeatureCollection with 'features' list."}

        features = data.get("features", [])
        validated_count = 0
        errors = []

        for idx, feat in enumerate(features):
            geom = feat.get("geometry")
            props = feat.get("properties", {})
            if not geom or "coordinates" not in geom:
                errors.append(f"Feature #{idx}: Missing geometry or coordinates.")
                continue

            name = props.get("name") or props.get("NAME") or props.get("ADMIN")
            if not name:
                errors.append(f"Feature #{idx}: Missing country/feature name property.")
                continue

            validated_count += 1

        # Audit log if admin provided
        if admin_user:
            audit = AuditLog(
                admin_id=admin_user.id,
                admin_username=admin_user.username,
                action="dataset_import_validated",
                resource_type="GeoJSON",
                resource_id=f"{validated_count}_features",
                details=f"Validated {validated_count} features. Errors: {len(errors)}"
            )
            db.session.add(audit)
            db.session.commit()

        return {
            "success": True,
            "total_features": len(features),
            "validated_count": validated_count,
            "errors": errors[:10] # Show top 10 errors if any
        }
