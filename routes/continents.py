from flask import Blueprint, render_template, abort
from services.geographic_service import GeographicService

continents_bp = Blueprint("continents", __name__, url_prefix="/continents")

@continents_bp.route("")
def list_continents():
    continents = GeographicService.get_all_continents()
    return render_template("continents/index.html", continents=continents)

@continents_bp.route("/<slug>")
def continent_detail(slug):
    continent = GeographicService.get_continent_by_slug(slug)
    if not continent:
        abort(404)
    countries = continent.countries.all()
    return render_template("continents/detail.html", continent=continent, countries=countries)
