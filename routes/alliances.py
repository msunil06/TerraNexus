from flask import Blueprint, render_template, abort
from services.alliance_service import AllianceService

alliances_bp = Blueprint("alliances", __name__, url_prefix="/alliances")

@alliances_bp.route("")
def index():
    alliances = AllianceService.get_all_alliances()
    return render_template(
        "alliances/index.html",
        alliances=alliances
    )

@alliances_bp.route("/<alliance_id>")
def detail(alliance_id):
    alliance = AllianceService.get_alliance_by_id(alliance_id)
    if not alliance:
        abort(404)
    return render_template(
        "alliances/detail.html",
        alliance=alliance
    )
