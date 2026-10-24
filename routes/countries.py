from flask import Blueprint, render_template, request, abort
from flask_login import current_user
from services.geographic_service import GeographicService
from services.live_data_service import LiveDataService
from services.hydrography_service import HydrographyService
from services.governance_military_service import GovernanceMilitaryService
from models.user import UserFavorite
from models.geography import AdministrativeDivision, City

countries_bp = Blueprint("countries", __name__, url_prefix="/countries")

@countries_bp.route("", strict_slashes=False)
@countries_bp.route("/", strict_slashes=False)
def list_countries():
    continent = request.args.get("continent")
    search = request.args.get("q")
    sort = request.args.get("sort", "name")

    countries = GeographicService.get_all_countries(continent_slug=continent, search_query=search, sort_by=sort)
    continents = GeographicService.get_all_continents()

    return render_template(
        "countries/index.html",
        countries=countries,
        continents=continents,
        selected_continent=continent,
        search_query=search,
        current_sort=sort,
        total_count=len(countries)
    )

@countries_bp.route("/<slug>")
def country_detail(slug):
    country = GeographicService.get_country_by_slug(slug)
    if not country:
        abort(404)

    neighbors = GeographicService.get_country_neighbors(country)
    divisions = GeographicService.get_country_divisions(country)
    capitals = country.capitals.all()
    cities = country.cities.limit(10).all()

    # Automatic inbuilt free live data (weather, forex, UN telemetry, World Bank live economy)
    live_data = LiveDataService.get_composite_live_data(country)

    # Ocean, marginal sea, and river connectivity
    hydrography = HydrographyService.get_country_hydrography(country)

    # Border sharing ranked by length (longest border priority first)
    ranked_borders_data = HydrographyService.get_ranked_borders(country)

    # Leadership & Armed Forces Intelligence
    leadership_military = GovernanceMilitaryService.get_country_leadership_and_military(country)

    # Check if user has favorited
    is_favorite = False
    if current_user.is_authenticated:
        fav = UserFavorite.query.filter_by(
            user_id=current_user.id,
            item_type="country",
            item_id=country.slug
        ).first()
        is_favorite = bool(fav)

    return render_template(
        "countries/detail.html",
        country=country,
        neighbors=neighbors,
        divisions=divisions,
        capitals=capitals,
        cities=cities,
        live_data=live_data,
        hydrography=hydrography,
        ranked_borders_data=ranked_borders_data,
        leadership_military=leadership_military,
        is_favorite=is_favorite
    )

@countries_bp.route("/<country_slug>/divisions/<division_slug>")
def division_detail(country_slug, division_slug):
    country, division = GeographicService.get_division_by_slug(country_slug, division_slug)
    if not country or not division:
        abort(404)

    subdivisions = division.subdivisions
    cities = division.cities.all()

    return render_template(
        "countries/division_detail.html",
        country=country,
        division=division,
        subdivisions=subdivisions,
        cities=cities
    )
