from flask import Blueprint, render_template, request, abort
from flask_login import current_user
from services.geographic_service import GeographicService
from models.user import UserFavorite

features_bp = Blueprint("features", __name__, url_prefix="/features")

@features_bp.route("")
def list_features():
    ftype = request.args.get("type")
    features = GeographicService.get_all_features(feature_type=ftype)
    
    types = [
        ("mountain", "Mountains"),
        ("mountain_range", "Mountain Ranges"),
        ("river", "Rivers"),
        ("lake", "Lakes & Inland Seas"),
        ("desert", "Deserts"),
        ("strait", "Straits & Channels"),
        ("trench", "Ocean Trenches")
    ]

    return render_template(
        "features/index.html",
        features=features,
        feature_types=types,
        selected_type=ftype
    )

@features_bp.route("/<slug>")
def feature_detail(slug):
    feature = GeographicService.get_feature_by_slug(slug)
    if not feature:
        abort(404)

    is_favorite = False
    if current_user.is_authenticated:
        fav = UserFavorite.query.filter_by(
            user_id=current_user.id,
            item_type="feature",
            item_id=feature.slug
        ).first()
        is_favorite = bool(fav)

    return render_template("features/detail.html", feature=feature, is_favorite=is_favorite)
