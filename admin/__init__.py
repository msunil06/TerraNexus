"""
TerraNexus Administrator Command Portal
=======================================
Dedicated administrative package providing comprehensive control over:
- User Data & User Controls (profile editing, password reset, role assignment, suspension, remote disconnect)
- Database Records (Full CRUD across Countries, Continents, Divisions, Features, Oceans, Seas)
- Website Content (Announcements, taglines, featured locations, user reports, data imports)
- System Settings (Maintenance mode, registrations, theme defaults, Mapbox & Google Maps API keys)
- Live Server Telemetry & Audit Logs
"""

from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Import routes to register endpoints on blueprint
from admin import routes
