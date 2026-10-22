import os
from datetime import datetime
from functools import wraps
from flask import render_template, request, flash, redirect, url_for, abort, jsonify, current_app
from flask_login import login_required, current_user, login_user, logout_user

from admin import admin_bp
from models import db
from models.user import User, Role, UserRole, UserReport, AuditLog, SystemSetting, UserSession
from models.geography import Country, AdministrativeDivision, Continent, Capital, City
from models.marine_and_physical import Ocean, Sea, GeographicFeature, DataSource
from services.data_import_service import DataImportService
from server.connection_manager import ServerConnectionManager
from api.config import API_REGISTRY, update_api_url
from api.gateway import ApiGateway

# -------------------------------------------------------------
# Authentication & Authorization Helpers
# -------------------------------------------------------------
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Access denied. High-security administrative privileges required.", "danger")
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def log_admin_action(action, resource_type, resource_id=None, details=None):
    try:
        log = AuditLog(
            admin_id=current_user.id if current_user.is_authenticated else None,
            admin_username=current_user.username if current_user.is_authenticated else "system",
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            details=details,
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()

# -------------------------------------------------------------
# Admin Login & Auth
# -------------------------------------------------------------
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    """Dedicated High-Security Administrator Login Portal."""
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter((User.username == login_id) | (User.email == login_id.lower())).first()

        if not user or not user.check_password(password):
            log_admin_action("admin_login_failed", "Security", details=f"Failed admin login attempt for '{login_id}' from IP {request.remote_addr}")
            flash("Invalid administrator credentials. Access attempt logged.", "danger")
            return render_template("admin/login.html")

        if not user.is_admin:
            log_admin_action("unauthorized_admin_attempt", "Security", user.id, f"Non-admin '{user.username}' attempted admin login from {request.remote_addr}")
            flash("Access denied. Administrative privileges are required.", "danger")
            return render_template("admin/login.html")

        if user.is_suspended:
            flash("This administrative account has been suspended.", "danger")
            return render_template("admin/login.html")

        # Success - log in & register server session
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        login_user(user, remember=False)
        ServerConnectionManager.register_connection(user, request)

        log_admin_action("admin_login_success", "Security", user.id, f"Administrator '{user.username}' authenticated successfully from {request.remote_addr}")
        flash(f"Welcome to TerraNexus Secure Admin Command, {user.display_name or user.username}!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/login.html")

@admin_bp.route("/logout")
@admin_required
def admin_logout():
    ServerConnectionManager.disconnect_all_user_sessions(current_user.id, admin_user=current_user)
    logout_user()
    flash("Administrator session closed successfully.", "info")
    return redirect(url_for("admin.admin_login"))

# -------------------------------------------------------------
# Admin Dashboard
# -------------------------------------------------------------
@admin_bp.route("")
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """Executive overview of platform health, metrics, users, and telemetry."""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active_account=True, is_suspended=False).count()
    suspended_users = User.query.filter_by(is_suspended=True).count()
    pending_reports = UserReport.query.filter_by(status="pending").count()

    total_countries = Country.query.count()
    total_continents = Continent.query.count()
    total_oceans = Ocean.query.count()
    total_seas = Sea.query.count()
    total_features = GeographicFeature.query.count()
    total_divisions = AdministrativeDivision.query.count()

    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8).all()
    recent_reports = UserReport.query.order_by(UserReport.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        active_users=active_users,
        suspended_users=suspended_users,
        pending_reports=pending_reports,
        total_countries=total_countries,
        total_continents=total_continents,
        total_oceans=total_oceans,
        total_seas=total_seas,
        total_features=total_features,
        total_divisions=total_divisions,
        recent_logs=recent_logs,
        recent_reports=recent_reports,
        recent_users=recent_users
    )

# -------------------------------------------------------------
# 1. User Management & User Controls
# -------------------------------------------------------------
@admin_bp.route("/users")
@admin_required
def users():
    """Complete user registry with search, status filters, and administrative actions."""
    search = request.args.get("q", "").strip()
    status_filter = request.args.get("status")
    
    query = User.query
    if search:
        term = f"%{search}%"
        query = query.filter((User.username.ilike(term)) | (User.email.ilike(term)) | (User.display_name.ilike(term)))
    
    if status_filter == "suspended":
        query = query.filter_by(is_suspended=True)
    elif status_filter == "active":
        query = query.filter_by(is_suspended=False)
    elif status_filter == "deletion_requested":
        query = query.filter_by(deletion_requested=True)

    all_users = query.order_by(User.created_at.desc()).all()
    roles = Role.query.all()

    return render_template(
        "admin/users.html",
        users=all_users,
        roles=roles,
        search=search,
        status_filter=status_filter
    )

@admin_bp.route("/users/<int:user_id>/edit-profile", methods=["POST"])
@admin_required
def edit_user_profile(user_id):
    """Admin controls and modifies all profile details of any user."""
    user = User.query.get_or_404(user_id)
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    display_name = request.form.get("display_name", "").strip()
    bio = request.form.get("bio", "").strip()
    location = request.form.get("location", "").strip()
    is_active_account = request.form.get("is_active_account") == "on"

    if not username or not email:
        flash("Username and Email cannot be empty.", "danger")
        return redirect(url_for("admin.users"))

    # Uniqueness check
    existing_user = User.query.filter((User.username == username) & (User.id != user.id)).first()
    if existing_user:
        flash(f"Username '{username}' is already taken by another account.", "danger")
        return redirect(url_for("admin.users"))

    existing_email = User.query.filter((User.email == email) & (User.id != user.id)).first()
    if existing_email:
        flash(f"Email '{email}' is already registered to another account.", "danger")
        return redirect(url_for("admin.users"))

    user.username = username
    user.email = email
    user.display_name = display_name
    user.bio = bio
    user.location = location
    user.is_active_account = is_active_account

    db.session.commit()
    log_admin_action("profile_edited_by_admin", "User", user.id, f"Admin updated profile for '{user.username}'")
    flash(f"Profile data for user '{user.username}' updated successfully.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/users/<int:user_id>/reset-password", methods=["POST"])
@admin_required
def reset_user_password(user_id):
    """Admin resets a user password and terminates existing sessions for security."""
    user = User.query.get_or_404(user_id)
    new_password = request.form.get("new_password", "").strip()

    if len(new_password) < 8:
        flash("Password must be at least 8 characters long for security compliance.", "danger")
        return redirect(url_for("admin.users"))

    user.set_password(new_password)
    ServerConnectionManager.disconnect_all_user_sessions(user.id, admin_user=current_user)
    db.session.commit()

    log_admin_action("password_reset_by_admin", "User", user.id, f"Admin reset password for '{user.username}' and revoked active sessions.")
    flash(f"Password for user '{user.username}' was reset successfully. Active sessions revoked.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/users/<int:user_id>/toggle-suspend", methods=["POST"])
@admin_required
def toggle_suspend_user(user_id):
    """Suspend or reactivate any user account with optional reason."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot suspend your own administrative account.", "danger")
        return redirect(url_for("admin.users"))

    user.is_suspended = not user.is_suspended
    action = "account_suspended" if user.is_suspended else "account_reactivated"
    reason = request.form.get("reason", "Administrative action")
    user.suspension_reason = reason if user.is_suspended else None

    if user.is_suspended:
        ServerConnectionManager.disconnect_all_user_sessions(user.id, admin_user=current_user)

    log_admin_action(action, "User", user.id, f"User '{user.username}' {action}. Reason: {reason}")
    db.session.commit()

    flash(f"User '{user.username}' has been {'suspended' if user.is_suspended else 'reactivated'}.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/users/<int:user_id>/update-role", methods=["POST"])
@admin_required
def update_user_role(user_id):
    """Assign or modify system role for a user."""
    user = User.query.get_or_404(user_id)
    new_role_id = request.form.get("role_id")
    role = Role.query.get(new_role_id)

    if not role:
        flash("Invalid role selected.", "danger")
        return redirect(url_for("admin.users"))

    UserRole.query.filter_by(user_id=user.id).delete()
    db.session.add(UserRole(user_id=user.id, role_id=role.id))
    
    log_admin_action("role_changed", "User", user.id, f"Assigned role '{role.name}' to user '{user.username}'")
    db.session.commit()

    flash(f"Role for '{user.username}' updated to '{role.name}'.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    """Permanently delete a user account and associated data."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own administrative account.", "danger")
        return redirect(url_for("admin.users"))

    username = user.username
    ServerConnectionManager.disconnect_all_user_sessions(user.id, admin_user=current_user)
    db.session.delete(user)
    db.session.commit()

    log_admin_action("user_deleted", "User", user_id, f"Admin permanently deleted user account '{username}'")
    flash(f"User '{username}' was permanently removed.", "info")
    return redirect(url_for("admin.users"))

# -------------------------------------------------------------
# 2. Database Records Manager (Complete CRUD for all models)
# -------------------------------------------------------------
MODEL_MAP = {
    "countries": (Country, "Country", "common_name"),
    "continents": (Continent, "Continent", "name"),
    "divisions": (AdministrativeDivision, "Administrative Division", "name"),
    "features": (GeographicFeature, "Geographic Feature", "name"),
    "oceans": (Ocean, "Ocean", "name"),
    "seas": (Sea, "Sea", "name")
}

@admin_bp.route("/database")
@admin_bp.route("/database/<model_key>")
@admin_required
def database_records(model_key="countries"):
    """Interactive database browser with search, pagination, and edit/delete actions."""
    if model_key not in MODEL_MAP:
        model_key = "countries"

    model_cls, display_name, search_col = MODEL_MAP[model_key]
    search = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    query = model_cls.query
    if search:
        col_attr = getattr(model_cls, search_col)
        query = query.filter(col_attr.ilike(f"%{search}%"))

    # Order by display name
    order_col = getattr(model_cls, search_col)
    query = query.order_by(order_col.asc())

    pagination = query.paginate(page=page, per_page=20, error_out=False)

    return render_template(
        "admin/database.html",
        model_key=model_key,
        model_name=display_name,
        records=pagination.items,
        pagination=pagination,
        search=search,
        all_models=MODEL_MAP
    )

@admin_bp.route("/database/<model_key>/create", methods=["GET", "POST"])
@admin_required
def create_database_record(model_key):
    """Create a new database record for any geographical entity."""
    if model_key not in MODEL_MAP:
        abort(404)

    model_cls, display_name, _ = MODEL_MAP[model_key]

    if request.method == "POST":
        try:
            if model_key == "countries":
                common_name = request.form.get("common_name", "").strip()
                official_name = request.form.get("official_name", "").strip() or common_name
                iso_a2 = request.form.get("iso_a2", "").strip().upper()
                iso_a3 = request.form.get("iso_a3", "").strip().upper()
                slug = request.form.get("slug", "").strip() or common_name.lower().replace(" ", "-")
                continent_id = int(request.form.get("continent_id", 1))
                capital_name = request.form.get("capital_name", "").strip()
                population = int(request.form.get("population", 0) or 0)
                area_km2 = float(request.form.get("area_km2", 0) or 0)
                currency_code = request.form.get("currency_code", "").strip()
                flag_emoji = request.form.get("flag_emoji", "").strip() or "🌐"

                new_country = Country(
                    common_name=common_name,
                    official_name=official_name,
                    iso_a2=iso_a2,
                    iso_a3=iso_a3,
                    slug=slug,
                    continent_id=continent_id,
                    capital_name=capital_name,
                    population=population,
                    area_km2=area_km2,
                    currency_code=currency_code,
                    flag_emoji=flag_emoji,
                    overview=request.form.get("overview", "")
                )
                db.session.add(new_country)
                db.session.commit()
                log_admin_action("record_created", "Country", new_country.id, f"Created country '{common_name}'")
                flash(f"Country '{common_name}' created successfully.", "success")

            elif model_key == "features":
                name = request.form.get("name", "").strip()
                slug = request.form.get("slug", "").strip() or name.lower().replace(" ", "-")
                feature_type = request.form.get("feature_type", "island")
                primary_iso = request.form.get("primary_country_iso", "").strip().upper()
                admin_center = request.form.get("administrative_center", "").strip()
                area_km2 = float(request.form.get("area_km2", 0) or 0)
                elevation_m = int(request.form.get("elevation_m", 0) or 0)
                lat = float(request.form.get("latitude", 0) or 0)
                lon = float(request.form.get("longitude", 0) or 0)
                waters = request.form.get("connected_features", "").strip()

                new_feature = GeographicFeature(
                    name=name,
                    slug=slug,
                    feature_type=feature_type,
                    primary_country_iso=primary_iso,
                    administrative_center=admin_center,
                    area_km2=area_km2,
                    elevation_m=elevation_m,
                    latitude=lat,
                    longitude=lon,
                    connected_features=waters,
                    overview=request.form.get("overview", "")
                )
                db.session.add(new_feature)
                db.session.commit()
                log_admin_action("record_created", "GeographicFeature", new_feature.id, f"Created feature '{name}'")
                flash(f"Geographic feature '{name}' created successfully.", "success")

            elif model_key == "divisions":
                name = request.form.get("name", "").strip()
                country_id = int(request.form.get("country_id", 1))
                slug = request.form.get("slug", "").strip() or name.lower().replace(" ", "-")
                div_type = request.form.get("division_type", "state")
                center = request.form.get("capital_or_center", "").strip()
                lat = float(request.form.get("latitude", 0) or 0)
                lon = float(request.form.get("longitude", 0) or 0)

                new_div = AdministrativeDivision(
                    name=name,
                    country_id=country_id,
                    slug=slug,
                    division_type=div_type,
                    capital_or_center=center,
                    latitude=lat,
                    longitude=lon
                )
                db.session.add(new_div)
                db.session.commit()
                log_admin_action("record_created", "AdministrativeDivision", new_div.id, f"Created division '{name}'")
                flash(f"Division '{name}' created successfully.", "success")

            return redirect(url_for("admin.database_records", model_key=model_key))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating record: {str(e)}", "danger")

    continents = Continent.query.all()
    countries = Country.query.order_by(Country.common_name.asc()).all()
    return render_template("admin/database_create.html", model_key=model_key, model_name=display_name, continents=continents, countries=countries)

@admin_bp.route("/database/<model_key>/<int:record_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_database_record(model_key, record_id):
    """Edit existing database record attributes."""
    if model_key not in MODEL_MAP:
        abort(404)

    model_cls, display_name, _ = MODEL_MAP[model_key]
    record = model_cls.query.get_or_404(record_id)

    if request.method == "POST":
        try:
            for field, val in request.form.items():
                if hasattr(record, field) and field != "id":
                    col_prop = getattr(model_cls, field).property
                    col_type = type(col_prop.columns[0].type).__name__
                    
                    if col_type in ("Integer", "BigInteger"):
                        setattr(record, field, int(val) if val.strip() else None)
                    elif col_type in ("Float", "Numeric"):
                        setattr(record, field, float(val) if val.strip() else None)
                    elif col_type == "Boolean":
                        setattr(record, field, val.lower() in ("true", "1", "on"))
                    else:
                        setattr(record, field, val.strip())

            db.session.commit()
            log_admin_action("record_edited", display_name, record.id, f"Admin edited {display_name} #{record.id}")
            flash(f"{display_name} record updated successfully.", "success")
            return redirect(url_for("admin.database_records", model_key=model_key))
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving changes: {str(e)}", "danger")

    continents = Continent.query.all()
    countries = Country.query.order_by(Country.common_name.asc()).all()
    return render_template(
        "admin/database_edit.html",
        model_key=model_key,
        model_name=display_name,
        record=record,
        continents=continents,
        countries=countries
    )

@admin_bp.route("/database/<model_key>/<int:record_id>/delete", methods=["POST"])
@admin_required
def delete_database_record(model_key, record_id):
    """Permanently delete a database record."""
    if model_key not in MODEL_MAP:
        abort(404)

    model_cls, display_name, _ = MODEL_MAP[model_key]
    record = model_cls.query.get_or_404(record_id)
    rec_title = getattr(record, "name", None) or getattr(record, "common_name", f"#{record_id}")

    db.session.delete(record)
    db.session.commit()

    log_admin_action("record_deleted", display_name, record_id, f"Admin deleted {display_name} '{rec_title}'")
    flash(f"{display_name} '{rec_title}' was deleted successfully.", "info")
    return redirect(url_for("admin.database_records", model_key=model_key))

# -------------------------------------------------------------
# 3. Website Content Management
# -------------------------------------------------------------
@admin_bp.route("/content", methods=["GET", "POST"])
@admin_required
def content_management():
    """Manage homepage notices, headlines, featured items, and datasets."""
    if request.method == "POST":
        action = request.form.get("action")
        if action == "update_branding":
            tagline = request.form.get("tagline", "").strip()
            sec_tagline = request.form.get("secondary_tagline", "").strip()
            announcement = request.form.get("announcement_banner", "").strip()

            def set_setting(k, v):
                s = SystemSetting.query.filter_by(key=k).first()
                if not s:
                    s = SystemSetting(key=k, value=v)
                    db.session.add(s)
                else:
                    s.value = v

            if tagline: set_setting("tagline", tagline)
            if sec_tagline: set_setting("secondary_tagline", sec_tagline)
            set_setting("announcement_banner", announcement)
            db.session.commit()
            flash("Website content settings updated successfully.", "success")

    tagline_setting = SystemSetting.query.filter_by(key="tagline").first()
    sec_tagline_setting = SystemSetting.query.filter_by(key="secondary_tagline").first()
    announcement_setting = SystemSetting.query.filter_by(key="announcement_banner").first()

    countries = Country.query.order_by(Country.common_name.asc()).limit(15).all()
    islands = GeographicFeature.query.filter_by(feature_type="island").limit(10).all()

    return render_template(
        "admin/content.html",
        tagline=tagline_setting.value if tagline_setting else current_app.config.get("TAGLINE"),
        sec_tagline=sec_tagline_setting.value if sec_tagline_setting else current_app.config.get("SECONDARY_TAGLINE"),
        announcement=announcement_setting.value if announcement_setting else "",
        countries=countries,
        islands=islands
    )

@admin_bp.route("/reports")
@admin_required
def reports():
    """Review and action user submitted feedback and geographical correction reports."""
    status_filter = request.args.get("status", "pending")
    query = UserReport.query
    if status_filter != "all":
        query = query.filter_by(status=status_filter)

    all_reports = query.order_by(UserReport.created_at.desc()).all()
    return render_template("admin/reports.html", reports=all_reports, current_status=status_filter)

@admin_bp.route("/reports/<int:report_id>/update", methods=["POST"])
@admin_required
def update_report_status(report_id):
    report = UserReport.query.get_or_404(report_id)
    new_status = request.form.get("status")
    admin_notes = request.form.get("admin_notes")

    if new_status in ("pending", "in_review", "resolved", "dismissed"):
        report.status = new_status
        report.admin_notes = admin_notes
        if new_status == "resolved":
            report.resolved_at = datetime.utcnow()

        log_admin_action("report_status_updated", "UserReport", report.id, f"Report #{report.id} set to {new_status}")
        db.session.commit()
        flash(f"Report #{report.id} status updated to {new_status}.", "success")

    return redirect(url_for("admin.reports"))

@admin_bp.route("/imports", methods=["GET", "POST"])
@admin_required
def data_imports():
    """GeoJSON data importer and verification engine."""
    validation_result = None
    if request.method == "POST":
        geojson_content = request.form.get("geojson_content")
        if geojson_content:
            validation_result = DataImportService.validate_and_import_geojson(geojson_content, admin_user=current_user)
            if validation_result["success"]:
                flash(f"Successfully validated {validation_result['validated_count']} features!", "success")
            else:
                flash(f"Validation failed: {validation_result['error']}", "danger")

    data_sources = DataSource.query.all()
    return render_template("admin/imports.html", validation_result=validation_result, data_sources=data_sources)

# -------------------------------------------------------------
# 4. System Settings & API Key Configuration
# -------------------------------------------------------------
@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def system_settings():
    """Complete platform configuration, security toggles, theme defaults, and map API keys."""
    settings_keys = [
        "app_name", "maintenance_mode", "allow_registration", "default_theme",
        "default_map_style", "mapbox_access_token", "google_maps_api_key",
        "opencage_api_key", "maptiler_api_key", "custom_tile_url"
    ]

    if request.method == "POST":
        for k in settings_keys:
            val = request.form.get(k, "").strip()
            s = SystemSetting.query.filter_by(key=k).first()
            if not s:
                s = SystemSetting(key=k, value=val)
                db.session.add(s)
            else:
                s.value = val

        db.session.commit()
        log_admin_action("system_settings_updated", "SystemSetting", details="Admin updated platform configuration and API keys")
        flash("System settings and API keys updated successfully.", "success")
        return redirect(url_for("admin.system_settings"))

    # Load all settings
    current_settings = {}
    for s in SystemSetting.query.all():
        current_settings[s.key] = s.value

    return render_template("admin/settings.html", settings=current_settings)

# -------------------------------------------------------------
# 5. Centralized API Gateway Hub
# -------------------------------------------------------------
@admin_bp.route("/apis")
@admin_required
def apis_hub():
    """Centralized API management dashboard - view, benchmark latency, and hot-swap URLs."""
    all_apis = API_REGISTRY
    return render_template("admin/apis.html", apis=all_apis)

@admin_bp.route("/apis/<api_id>/test", methods=["POST"])
@admin_required
def test_api_connection(api_id):
    """Test live ping latency for any external API."""
    result = ApiGateway.test_single_api(api_id)
    return jsonify(result)

@admin_bp.route("/apis/<api_id>/update-url", methods=["POST"])
@admin_required
def update_api_url_route(api_id):
    """Replace an API endpoint with a new URL."""
    new_url = request.form.get("new_url", "").strip()
    if not new_url:
        flash("New API URL cannot be empty.", "danger")
        return redirect(url_for("admin.apis_hub"))

    success = update_api_url(api_id, new_url)
    if success:
        log_admin_action("api_endpoint_updated", "API", api_id, f"Admin updated API '{api_id}' to: {new_url}")
        flash(f"API '{api_id}' URL replaced with: {new_url}", "success")
    else:
        flash(f"API identifier '{api_id}' not found.", "danger")

    return redirect(url_for("admin.apis_hub"))

# -------------------------------------------------------------
# 6. Live Server Connections Monitor
# -------------------------------------------------------------
@admin_bp.route("/connections")
@admin_required
def server_connections():
    """Live Server Connections Monitor & active telemetry."""
    connections = ServerConnectionManager.get_all_connections(active_only=False)
    telemetry = ServerConnectionManager.get_server_telemetry()
    return render_template("admin/connections.html", connections=connections, telemetry=telemetry)

@admin_bp.route("/connections/<int:session_id>/disconnect", methods=["POST"])
@admin_required
def disconnect_session(session_id):
    """Admin disconnects an individual server session."""
    success, msg = ServerConnectionManager.disconnect_session(session_id, admin_user=current_user)
    if success:
        log_admin_action("session_disconnected", "UserSession", session_id, f"Admin terminated server session #{session_id}")
        flash(msg, "success")
    else:
        flash(msg, "warning")
    return redirect(url_for("admin.server_connections"))

@admin_bp.route("/users/<int:user_id>/disconnect-all", methods=["POST"])
@admin_required
def disconnect_user_connections(user_id):
    """Admin terminates all active server connections for a user."""
    user = User.query.get_or_404(user_id)
    success, msg = ServerConnectionManager.disconnect_all_user_sessions(user.id, admin_user=current_user)
    log_admin_action("all_user_sessions_disconnected", "User", user.id, f"Admin severed all active connection(s) for '{user.username}'")
    flash(msg, "success" if success else "warning")
    return redirect(request.referrer or url_for("admin.server_connections"))

# -------------------------------------------------------------
# 7. Audit Logs
# -------------------------------------------------------------
@admin_bp.route("/audit-logs")
@admin_required
def audit_logs():
    """Full chronological audit trail of all administrative actions."""
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(150).all()
    return render_template("admin/logs.html", logs=logs)
