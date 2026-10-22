from flask import Blueprint, render_template, abort
from flask_login import current_user
from services.geographic_service import GeographicService
from models.user import UserFavorite

oceans_bp = Blueprint("oceans", __name__, url_prefix="/oceans")

@oceans_bp.route("")
def list_oceans():
    oceans = GeographicService.get_all_oceans()
    return render_template("oceans/index.html", oceans=oceans)

@oceans_bp.route("/<slug>")
def ocean_detail(slug):
    ocean = GeographicService.get_ocean_by_slug(slug)
    if not ocean:
        abort(404)

    seas = ocean.seas.all()

    is_favorite = False
    if current_user.is_authenticated:
        fav = UserFavorite.query.filter_by(
            user_id=current_user.id,
            item_type="ocean",
            item_id=ocean.slug
        ).first()
        is_favorite = bool(fav)

    return render_template(
        "oceans/detail.html",
        ocean=ocean,
        seas=seas,
        is_favorite=is_favorite
    )
