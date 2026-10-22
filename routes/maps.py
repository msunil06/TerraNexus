from flask import Blueprint, render_template, request, jsonify, abort
from models.geography import Country, Continent, AdministrativeDivision
from models.marine_and_physical import Ocean, Sea, GeographicFeature
from services.geographic_service import GeographicService
from api.gateway import ApiGateway
from api.config import API_REGISTRY

maps_bp = Blueprint("maps", __name__, url_prefix="/maps")

@maps_bp.route("")
def maps_hub():
    """Central Map Atlas & Geocartography Portal."""
    countries = GeographicService.get_all_countries()
    oceans = GeographicService.get_all_oceans()
    seas = GeographicService.get_all_seas()
    
    # Query Islands and Archipelagos
    islands = GeographicFeature.query.filter(
        GeographicFeature.feature_type.in_(["island", "archipelago"])
    ).order_by(GeographicFeature.area_km2.desc()).all()

    # Query all physical features
    features = GeographicFeature.query.order_by(GeographicFeature.name.asc()).all()

    return render_template(
        "maps/index.html",
        countries=countries,
        oceans=oceans,
        seas=seas,
        islands=islands,
        features=features,
        total_countries=len(countries),
        total_oceans=len(oceans),
        total_islands=len(islands)
    )

@maps_bp.route("/world")
def world_map():
    """Dedicated Global Interactive World Map with all free basemaps."""
    return render_template("maps/world.html")

@maps_bp.route("/countries")
def countries_gallery():
    """Gallery and search directory for country maps."""
    continent = request.args.get("continent")
    search = request.args.get("q")
    countries = GeographicService.get_all_countries(continent_slug=continent, search_query=search)
    continents = GeographicService.get_all_continents()
    return render_template(
        "maps/countries_gallery.html",
        countries=countries,
        continents=continents,
        selected_continent=continent,
        search_query=search
    )

@maps_bp.route("/countries/<slug>")
@maps_bp.route("/country/<slug>")
def country_map(slug):
    """Dedicated Interactive Country Map with boundaries, capital, and divisions."""
    country = GeographicService.get_country_by_slug(slug)
    if not country:
        abort(404)

    divisions = GeographicService.get_country_divisions(country)
    neighbors = GeographicService.get_country_neighbors(country)
    capitals = country.capitals.all()
    primary_capital = capitals[0] if capitals else None

    return render_template(
        "maps/country.html",
        country=country,
        divisions=divisions,
        neighbors=neighbors,
        capital=primary_capital
    )

@maps_bp.route("/oceans")
def oceans_gallery():
    """Gallery and directory for world oceans and marine maps."""
    oceans = GeographicService.get_all_oceans()
    seas = GeographicService.get_all_seas()
    return render_template("maps/oceans_gallery.html", oceans=oceans, seas=seas)

from services.live_data_service import LiveDataService

@maps_bp.route("/oceans/<slug>")
@maps_bp.route("/ocean/<slug>")
def ocean_map(slug):
    """Dedicated Ocean & Marine Map showing marginal seas, currents, and trenches."""
    ocean = GeographicService.get_ocean_by_slug(slug)
    if not ocean:
        abort(404)

    seas = ocean.seas.all()
    # Find trenches in this ocean
    trenches = GeographicFeature.query.filter(
        GeographicFeature.feature_type == "trench",
        GeographicFeature.connected_features.ilike(f"%{ocean.name}%")
    ).all()

    live_marine = LiveDataService.get_live_ocean_marine(ocean.name)

    return render_template(
        "maps/ocean.html",
        ocean=ocean,
        seas=seas,
        trenches=trenches,
        live_marine=live_marine
    )

@maps_bp.route("/islands")
def islands_gallery():
    """Gallery and directory for world islands and archipelagos."""
    ocean_filter = request.args.get("ocean")
    query = GeographicFeature.query.filter(
        GeographicFeature.feature_type.in_(["island", "archipelago"])
    )

    if ocean_filter:
        query = query.filter(GeographicFeature.connected_features.ilike(f"%{ocean_filter}%"))

    islands = query.order_by(GeographicFeature.area_km2.desc()).all()
    all_oceans = GeographicService.get_all_oceans()

    return render_template(
        "maps/islands_gallery.html",
        islands=islands,
        oceans=all_oceans,
        selected_ocean=ocean_filter
    )

@maps_bp.route("/islands/<slug>")
@maps_bp.route("/island/<slug>")
def island_map(slug):
    """Dedicated Island Map view showing coordinates, elevation, area, and marine context."""
    island = GeographicFeature.query.filter_by(slug=slug).first()
    if not island or island.feature_type not in ("island", "archipelago"):
        abort(404)

    # Find parent country if available
    parent_country = None
    if island.primary_country_iso:
        parent_country = Country.query.filter_by(iso_a3=island.primary_country_iso).first()

    live_island = LiveDataService.get_live_island_data(island)

    return render_template(
        "maps/island.html",
        island=island,
        parent_country=parent_country,
        live_island=live_island
    )

@maps_bp.route("/search")
def map_search():
    """
    Unified Map Geocoding Search API.
    Queries both local database catalog and the free public Nominatim OpenStreetMap API.
    Zero API key required.
    """
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"status": "success", "query": "", "results": []})

    # 1. Local Database Results
    local_results = []
    # Match Country
    for c in Country.query.filter(Country.common_name.ilike(f"%{q}%")).limit(4).all():
        if c.latitude and c.longitude:
            local_results.append({
                "title": f"{c.flag_emoji or '🏛️'} {c.common_name}",
                "type": "Country",
                "lat": c.latitude,
                "lon": c.longitude,
                "zoom": 5,
                "url": f"/maps/countries/{c.slug}",
                "source": "TerraNexus Vector DB"
            })

    # Match Island / Physical Feature
    for f in GeographicFeature.query.filter(GeographicFeature.name.ilike(f"%{q}%")).limit(4).all():
        if f.latitude and f.longitude:
            local_results.append({
                "title": f"🏝️ {f.name}" if f.feature_type in ("island", "archipelago") else f"📍 {f.name}",
                "type": f.feature_type.capitalize(),
                "lat": f.latitude,
                "lon": f.longitude,
                "zoom": 7 if f.feature_type in ("island", "archipelago") else 6,
                "url": f"/maps/islands/{f.slug}" if f.feature_type in ("island", "archipelago") else f"/features/{f.slug}",
                "source": "TerraNexus Geographic DB"
            })

    # Match Ocean / Sea
    for o in Ocean.query.filter(Ocean.name.ilike(f"%{q}%")).limit(2).all():
        local_results.append({
            "title": f"🌊 {o.name}",
            "type": "Ocean",
            "lat": 0.0,
            "lon": 160.0 if "Pacific" in o.name else (0.0 if "Atlantic" in o.name else 75.0),
            "zoom": 3,
            "url": f"/maps/oceans/{o.slug}",
            "source": "TerraNexus Marine DB"
        })

    # 2. External Free Nominatim Public API (if query is specific)
    ext_results = []
    if len(local_results) < 3 and len(q) >= 3:
        nominatim_data = ApiGateway.search_location_free_api(q, limit=3)
        for item in nominatim_data:
            ext_results.append({
                "title": item["name"][:75] + ("..." if len(item["name"]) > 75 else ""),
                "type": item["type"].capitalize(),
                "lat": item["lat"],
                "lon": item["lon"],
                "zoom": 9,
                "url": f"#",
                "source": "Nominatim OpenStreetMap Free API"
            })

    combined = local_results + ext_results
    return jsonify({
        "status": "success",
        "query": q,
        "count": len(combined),
        "results": combined
    })
