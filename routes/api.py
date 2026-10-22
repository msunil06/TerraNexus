from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from models import db
from models.user import UserFavorite, SavedLocation
from models.geography import Country, Continent, AdministrativeDivision, Capital
from models.marine_and_physical import Ocean, Sea, GeographicFeature
from services.geographic_service import GeographicService
from services.search_service import SearchService
from services.live_data_service import LiveDataService

api_bp = Blueprint("api", __name__, url_prefix="/api")

# --- Public Geographic Endpoints ---

@api_bp.route("/countries")
def get_countries():
    continent = request.args.get("continent")
    search = request.args.get("q")
    countries = GeographicService.get_all_countries(continent_slug=continent, search_query=search)
    return jsonify({
        "status": "success",
        "count": len(countries),
        "data": [{
            "common_name": c.common_name,
            "official_name": c.official_name,
            "slug": c.slug,
            "iso_a2": c.iso_a2,
            "iso_a3": c.iso_a3,
            "capital": c.capital_name,
            "continent": c.continent_rel.name if c.continent_rel else None,
            "population": c.population,
            "area_km2": c.area_km2,
            "flag_emoji": c.flag_emoji,
            "currency_code": c.currency_code
        } for c in countries]
    })

@api_bp.route("/countries/<identifier>")
def get_country_detail(identifier):
    country = GeographicService.get_country_by_slug(identifier)
    if not country:
        return jsonify({"status": "error", "message": f"Country '{identifier}' not found"}), 404

    return jsonify({
        "status": "success",
        "data": {
            "common_name": country.common_name,
            "official_name": country.official_name,
            "slug": country.slug,
            "iso_a2": country.iso_a2,
            "iso_a3": country.iso_a3,
            "continent": country.continent_rel.name if country.continent_rel else None,
            "subregion": country.subregion,
            "capital": country.capital_name,
            "largest_city": country.largest_city,
            "population": country.population,
            "area_km2": country.area_km2,
            "latitude": country.latitude,
            "longitude": country.longitude,
            "highest_point": country.highest_point,
            "currency": {
                "code": country.currency_code,
                "name": country.currency_name,
                "symbol": country.currency_symbol
            },
            "languages": country.official_languages,
            "demonym": country.demonym,
            "calling_code": country.calling_code,
            "tld": country.tld,
            "time_zones": country.time_zones,
            "driving_side": country.driving_side,
            "gdp_usd_billions": country.gdp_usd_billions,
            "overview": country.overview,
            "data_source": country.data_source,
            "last_updated": country.last_updated.isoformat() if country.last_updated else None
        }
    })

@api_bp.route("/countries/<identifier>/live")
def get_country_live_data(identifier):
    country = GeographicService.get_country_by_slug(identifier)
    if not country:
        return jsonify({"status": "error", "message": f"Country '{identifier}' not found"}), 404

    live_data = LiveDataService.get_composite_live_data(country)
    return jsonify({
        "status": "success",
        "country": {
            "name": country.common_name,
            "slug": country.slug,
            "iso_a2": country.iso_a2,
            "iso_a3": country.iso_a3,
            "capital": country.capital_name,
            "currency_code": country.currency_code
        },
        "live": live_data
    })

@api_bp.route("/countries/<identifier>/neighbors")
def get_country_neighbors(identifier):
    country = GeographicService.get_country_by_slug(identifier)
    if not country:
        return jsonify({"status": "error", "message": "Country not found"}), 404

    neighbors = GeographicService.get_country_neighbors(country)
    return jsonify({
        "status": "success",
        "country": country.common_name,
        "count": len(neighbors),
        "data": [{
            "name": n["country"].common_name,
            "slug": n["country"].slug,
            "iso_a3": n["country"].iso_a3,
            "flag_emoji": n["country"].flag_emoji,
            "border_type": n["border_type"],
            "length_km": n["length_km"]
        } for n in neighbors]
    })

@api_bp.route("/countries/<identifier>/divisions")
def get_country_divisions(identifier):
    country = GeographicService.get_country_by_slug(identifier)
    if not country:
        return jsonify({"status": "error", "message": "Country not found"}), 404

    divisions = GeographicService.get_country_divisions(country)
    return jsonify({
        "status": "success",
        "country": country.common_name,
        "count": len(divisions),
        "data": [{
            "name": d.name,
            "slug": d.slug,
            "code": d.code,
            "type": d.division_type,
            "capital_or_center": d.capital_or_center,
            "area_km2": d.area_km2,
            "population": d.population,
            "subdivisions_count": len(d.subdivisions)
        } for d in divisions]
    })

@api_bp.route("/continents")
def get_continents():
    continents = GeographicService.get_all_continents()
    return jsonify({
        "status": "success",
        "data": [{
            "name": c.name,
            "slug": c.slug,
            "code": c.code,
            "area_km2": c.area_km2,
            "population": c.population,
            "countries_count": c.countries_count
        } for c in continents]
    })

@api_bp.route("/oceans")
def get_oceans():
    oceans = GeographicService.get_all_oceans()
    return jsonify({
        "status": "success",
        "data": [{
            "name": o.name,
            "slug": o.slug,
            "area_km2": o.area_km2,
            "avg_depth_m": o.avg_depth_m,
            "max_depth_m": o.max_depth_m,
            "max_depth_location": o.max_depth_location,
            "surrounding_continents": o.surrounding_continents
        } for o in oceans]
    })

@api_bp.route("/oceans/<slug>")
def get_ocean_detail(slug):
    ocean = GeographicService.get_ocean_by_slug(slug)
    if not ocean:
        return jsonify({"status": "error", "message": "Ocean not found"}), 404

    return jsonify({
        "status": "success",
        "data": {
            "name": ocean.name,
            "slug": ocean.slug,
            "area_km2": ocean.area_km2,
            "avg_depth_m": ocean.avg_depth_m,
            "max_depth_m": ocean.max_depth_m,
            "max_depth_location": ocean.max_depth_location,
            "marginal_seas": [s.name for s in ocean.seas],
            "major_currents": ocean.major_currents,
            "overview": ocean.overview,
            "marine_biodiversity": ocean.marine_biodiversity,
            "economic_importance": ocean.economic_importance,
            "environmental_challenges": ocean.environmental_challenges
        }
    })

@api_bp.route("/seas")
def get_seas():
    ocean_slug = request.args.get("ocean")
    seas = GeographicService.get_all_seas(ocean_slug=ocean_slug)
    return jsonify({
        "status": "success",
        "count": len(seas),
        "data": [{
            "name": s.name,
            "slug": s.slug,
            "sea_type": s.sea_type,
            "area_km2": s.area_km2,
            "max_depth_m": s.max_depth_m,
            "ocean": s.ocean.name if s.ocean else None,
            "latitude": s.latitude,
            "longitude": s.longitude
        } for s in seas]
    })

@api_bp.route("/seas/<slug>")
def get_sea_detail(slug):
    sea = GeographicService.get_sea_by_slug(slug)
    if not sea:
        return jsonify({"status": "error", "message": "Sea not found"}), 404

    return jsonify({
        "status": "success",
        "data": {
            "name": sea.name,
            "slug": sea.slug,
            "alternative_names": sea.alternative_names,
            "sea_type": sea.sea_type,
            "ocean": sea.ocean.name if sea.ocean else None,
            "area_km2": sea.area_km2,
            "avg_depth_m": sea.avg_depth_m,
            "max_depth_m": sea.max_depth_m,
            "latitude": sea.latitude,
            "longitude": sea.longitude,
            "surrounding_countries": sea.surrounding_countries,
            "connected_water_bodies": sea.connected_water_bodies,
            "major_ports": sea.major_ports,
            "overview": sea.overview
        }
    })

@api_bp.route("/features")
def get_features():
    ftype = request.args.get("type")
    features = GeographicService.get_all_features(feature_type=ftype)
    return jsonify({
        "status": "success",
        "count": len(features),
        "data": [{
            "name": f.name,
            "slug": f.slug,
            "type": f.feature_type,
            "elevation_m": f.elevation_m,
            "length_km": f.length_km,
            "area_km2": f.area_km2,
            "latitude": f.latitude,
            "longitude": f.longitude,
            "countries_involved": f.countries_involved
        } for f in features]
    })

@api_bp.route("/search")
def search():
    query_str = request.args.get("q", "")
    limit = min(int(request.args.get("limit", 15)), 50)
    results = SearchService.global_search(query_str, limit=limit)
    return jsonify({
        "status": "success",
        "query": query_str,
        "count": len(results),
        "data": results
    })

@api_bp.route("/map/markers")
def map_markers():
    """Return point features (capitals, seas, physical features) for interactive map layers."""
    markers = []

    # Country Capitals
    for country in Country.query.filter(Country.latitude.isnot(None), Country.longitude.isnot(None)).all():
        markers.append({
            "id": f"country-{country.slug}",
            "type": "country",
            "name": country.common_name,
            "capital": country.capital_name,
            "lat": country.latitude,
            "lon": country.longitude,
            "flag": country.flag_emoji,
            "url": f"/countries/{country.slug}",
            "population": country.population,
            "currency": country.currency_code
        })

    # Seas
    for sea in Sea.query.filter(Sea.latitude.isnot(None), Sea.longitude.isnot(None)).all():
        markers.append({
            "id": f"sea-{sea.slug}",
            "type": "sea",
            "name": sea.name,
            "lat": sea.latitude,
            "lon": sea.longitude,
            "max_depth_m": sea.max_depth_m,
            "url": f"/seas/{sea.slug}"
        })

    # Physical Features
    for feat in GeographicFeature.query.filter(GeographicFeature.latitude.isnot(None), GeographicFeature.longitude.isnot(None)).all():
        markers.append({
            "id": f"feature-{feat.slug}",
            "type": feat.feature_type,
            "name": feat.name,
            "lat": feat.latitude,
            "lon": feat.longitude,
            "elevation_m": feat.elevation_m,
            "length_km": feat.length_km,
            "url": f"/features/{feat.slug}"
        })

    return jsonify({"status": "success", "count": len(markers), "data": markers})

# --- Authenticated User Endpoints ---

@api_bp.route("/me")
@login_required
def get_current_user_profile():
    return jsonify({
        "status": "success",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "display_name": current_user.display_name,
            "preferred_language": current_user.preferred_language,
            "theme_preference": current_user.theme_preference,
            "is_admin": current_user.is_admin,
            "favorites_count": current_user.favorites.count()
        }
    })

@api_bp.route("/me/favorites", methods=["GET"])
@login_required
def get_user_favorites():
    favs = current_user.favorites.all()
    return jsonify({
        "status": "success",
        "data": [{
            "id": f.id,
            "item_type": f.item_type,
            "item_id": f.item_id,
            "item_title": f.item_title,
            "item_subtitle": f.item_subtitle,
            "item_flag": f.item_flag,
            "created_at": f.created_at.isoformat()
        } for f in favs]
    })

@api_bp.route("/me/favorites", methods=["POST"])
@login_required
def add_user_favorite():
    data = request.get_json(silent=True) or request.form
    item_type = data.get("item_type")
    item_id = data.get("item_id")
    item_title = data.get("item_title", item_id)
    item_subtitle = data.get("item_subtitle")
    item_flag = data.get("item_flag")

    if not item_type or not item_id:
        return jsonify({"status": "error", "message": "item_type and item_id are required"}), 400

    existing = UserFavorite.query.filter_by(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id
    ).first()

    if existing:
        return jsonify({"status": "success", "message": "Item already in favorites", "favorited": True})

    new_fav = UserFavorite(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id,
        item_title=item_title,
        item_subtitle=item_subtitle,
        item_flag=item_flag
    )
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"status": "success", "message": "Saved to favorites", "favorited": True, "id": new_fav.id})

@api_bp.route("/me/favorites/<item_type>/<item_id>", methods=["DELETE"])
@login_required
def remove_user_favorite(item_type, item_id):
    fav = UserFavorite.query.filter_by(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id
    ).first()

    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"status": "success", "message": "Removed from favorites", "favorited": False})
    
    return jsonify({"status": "error", "message": "Favorite not found"}), 404

@api_bp.route("/me/saved-locations", methods=["POST"])
@login_required
def add_saved_location():
    data = request.get_json(silent=True) or request.form
    name = data.get("name", "Saved Map Point")
    lat = float(data.get("latitude", 0.0))
    lon = float(data.get("longitude", 0.0))
    zoom = int(data.get("zoom_level", 6))
    notes = data.get("notes")

    loc = SavedLocation(
        user_id=current_user.id,
        name=name,
        latitude=lat,
        longitude=lon,
        zoom_level=zoom,
        notes=notes
    )
    db.session.add(loc)
    db.session.commit()

    return jsonify({"status": "success", "message": "Location saved", "id": loc.id})
