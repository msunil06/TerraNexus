from flask import Blueprint, render_template, request, abort
from flask_login import current_user
from services.geographic_service import GeographicService
from models.user import UserFavorite

seas_bp = Blueprint("seas", __name__, url_prefix="/seas")

@seas_bp.route("")
def list_seas():
    ocean_slug = request.args.get("ocean")
    seas = GeographicService.get_all_seas(ocean_slug=ocean_slug)
    oceans = GeographicService.get_all_oceans()
    return render_template("seas/index.html", seas=seas, oceans=oceans, selected_ocean=ocean_slug)

@seas_bp.route("/<slug>")
def sea_detail(slug):
    sea = GeographicService.get_sea_by_slug(slug)
    if not sea:
        abort(404)

    is_favorite = False
    if current_user.is_authenticated:
        fav = UserFavorite.query.filter_by(
            user_id=current_user.id,
            item_type="sea",
            item_id=sea.slug
        ).first()
        is_favorite = bool(fav)

    return render_template("seas/detail.html", sea=sea, is_favorite=is_favorite)
