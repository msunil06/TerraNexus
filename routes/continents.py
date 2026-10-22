from flask import Blueprint, render_template, abort
from services.geographic_service import GeographicService
from models.geography import Country

continents_bp = Blueprint("continents", __name__, url_prefix="/continents")

@continents_bp.route("")
def list_continents():
    continents = GeographicService.get_all_continents()
    continents_data = []
    for c in continents:
        countries = c.countries.order_by(Country.common_name.asc()).all()
        continents_data.append({
            "continent": c,
            "countries": countries,
            "count": len(countries)
        })
    return render_template("continents/index.html", continents=continents, continents_data=continents_data)

@continents_bp.route("/<slug>")
def continent_detail(slug):
    continent = GeographicService.get_continent_by_slug(slug)
    if not continent:
        abort(404)
    countries = continent.countries.all()
    return render_template("continents/detail.html", continent=continent, countries=countries)
