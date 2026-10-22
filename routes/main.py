from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from models import db
from models.user import UserReport
from services.geographic_service import GeographicService

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    stats = GeographicService.get_global_statistics()
    featured_countries = GeographicService.get_all_countries()[:6]
    featured_oceans = GeographicService.get_all_oceans()[:3]
    featured_seas = GeographicService.get_all_seas()[:4]
    featured_features = GeographicService.get_all_features()[:4]

    return render_template(
        "index.html",
        stats=stats,
        featured_countries=featured_countries,
        featured_oceans=featured_oceans,
        featured_seas=featured_seas,
        featured_features=featured_features
    )

@main_bp.route("/map")
def explore_map():
    return render_template("map.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/sources")
def sources():
    data_sources = GeographicService.get_all_data_sources()
    return render_template("sources.html", data_sources=data_sources)

@main_bp.route("/accessibility")
def accessibility():
    return render_template("accessibility.html")

@main_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main_bp.route("/terms")
def terms():
    return render_template("terms.html")

@main_bp.route("/report", methods=["GET", "POST"])
def submit_report():
    if request.method == "POST":
        report_type = request.form.get("report_type", "incorrect_info")
        subject_type = request.form.get("subject_type", "country")
        subject_id = request.form.get("subject_id", "").strip()
        subject_name = request.form.get("subject_name", "").strip()
        description = request.form.get("description", "").strip()
        suggested_correction = request.form.get("suggested_correction", "").strip()

        if not description or not subject_id:
            flash("Please provide all required fields including subject ID and description.", "danger")
            return redirect(url_for("main.submit_report"))

        user_id = current_user.id if current_user.is_authenticated else None

        report = UserReport(
            user_id=user_id,
            report_type=report_type,
            subject_type=subject_type,
            subject_id=subject_id,
            subject_name=subject_name,
            description=description,
            suggested_correction=suggested_correction,
            status="pending"
        )
        db.session.add(report)
        db.session.commit()

        flash("Thank you! Your correction report has been submitted to the editorial review team.", "success")
        return redirect(url_for("main.index"))

    # Prefill from query params if coming from a country/sea page
    prefill_type = request.args.get("type", "country")
    prefill_id = request.args.get("id", "")
    prefill_name = request.args.get("name", "")

    return render_template("report.html", prefill_type=prefill_type, prefill_id=prefill_id, prefill_name=prefill_name)
