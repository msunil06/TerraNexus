"""
TerraNexus Centralized API Configuration Registry
=================================================
This file houses all external free API endpoints in ONE centralized location.
When you want to replace an API with a faster/better one, simply edit the endpoint URL here.
Zero API keys are required for any of these default services.
"""

# Master API Registry
API_REGISTRY = {
    "weather": {
        "id": "weather",
        "name": "Open-Meteo Global Meteorological Forecast",
        "category": "Weather & Meteorology",
        "url": "https://api.open-meteo.com/v1/forecast",
        "method": "GET",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.20&current=temperature_2m",
        "description": "High-accuracy live capital weather, thermal comfort index, relative humidity, wind speed, and WMO codes.",
        "documentation": "https://open-meteo.com/en/docs"
    },
    "forex": {
        "id": "forex",
        "name": "Open Exchange Rates Free Public Endpoint",
        "category": "Foreign Exchange",
        "url": "https://open.er-api.com/v6/latest/{currency}",
        "method": "GET",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://open.er-api.com/v6/latest/USD",
        "description": "Real-time foreign exchange benchmark valuations across major fiat currencies.",
        "documentation": "https://open.er-api.com"
    },
    "telemetry": {
        "id": "telemetry",
        "name": "REST Countries v3.1 Open API",
        "category": "Sovereign Indicators",
        "url": "https://restcountries.com/v3.1/alpha/{code}",
        "method": "GET",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://restcountries.com/v3.1/alpha/IN",
        "description": "UN member state status, official sovereign coat of arms (SVG/PNG), and territorial indicators.",
        "documentation": "https://restcountries.com"
    },
    "demographics": {
        "id": "demographics",
        "name": "World Bank Open Data Population API",
        "category": "Demographics & Census",
        "url": "https://api.worldbank.org/v2/country/{code}/indicator/SP.POP.TOTL?format=json",
        "method": "GET",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://api.worldbank.org/v2/country/IN/indicator/SP.POP.TOTL?format=json&per_page=1",
        "description": "Authoritative global population counts, historical trends, and official census statistics.",
        "documentation": "https://datahelpdesk.worldbank.org"
    },
    "geocoding": {
        "id": "geocoding",
        "name": "Nominatim OpenStreetMap Geocoding API",
        "category": "Map Search & Geocoding",
        "url": "https://nominatim.openstreetmap.org/search",
        "method": "GET",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://nominatim.openstreetmap.org/search?q=London&format=json&limit=1",
        "description": "Global place, boundary, country, island, ocean, and coordinate search with zero API key.",
        "documentation": "https://nominatim.org"
    },
    "map_satellite": {
        "id": "map_satellite",
        "name": "ESRI World Imagery (Satellite Tiles)",
        "category": "Map Tiles",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "method": "TILE",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/0/0/0",
        "description": "High-resolution satellite and aerial photography covering the entire planet Earth.",
        "documentation": "https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9"
    },
    "map_carto_dark": {
        "id": "map_carto_dark",
        "name": "CartoDB Dark Matter Basemap",
        "category": "Map Tiles",
        "url": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        "method": "TILE",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://a.basemaps.cartocdn.com/dark_all/0/0/0.png",
        "description": "Sleek dark theme map tiles ideal for nighttime navigation and neon data overlays.",
        "documentation": "https://carto.com/basemaps"
    },
    "map_carto_light": {
        "id": "map_carto_light",
        "name": "CartoDB Positron Light Basemap",
        "category": "Map Tiles",
        "url": "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        "method": "TILE",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://a.basemaps.cartocdn.com/light_all/0/0/0.png",
        "description": "High-contrast minimalist light atlas tiles designed for daytime clarity.",
        "documentation": "https://carto.com/basemaps"
    },
    "map_osm": {
        "id": "map_osm",
        "name": "OpenStreetMap Standard Cartography",
        "category": "Map Tiles",
        "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "method": "TILE",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://a.tile.openstreetmap.org/0/0/0.png",
        "description": "The open standard for global geographic features, roads, and national borders.",
        "documentation": "https://www.openstreetmap.org"
    },
    "map_opentopo": {
        "id": "map_opentopo",
        "name": "OpenTopoMap Physical Relief",
        "category": "Map Tiles",
        "url": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        "method": "TILE",
        "is_free": True,
        "key_required": False,
        "ping_url": "https://a.tile.opentopomap.org/0/0/0.png",
        "description": "Topographical elevation contours, mountain relief shading, and hydrographic water bodies.",
        "documentation": "https://opentopomap.org"
    }
}

def get_api_endpoint(api_id):
    """Retrieve an API configuration by ID."""
    return API_REGISTRY.get(api_id)

def get_all_apis():
    """Retrieve all registered APIs as a list."""
    return list(API_REGISTRY.values())

def update_api_url(api_id, new_url):
    """Dynamically replace an API endpoint URL with an alternative."""
    if api_id in API_REGISTRY:
        API_REGISTRY[api_id]["url"] = new_url
        return True
    return False
