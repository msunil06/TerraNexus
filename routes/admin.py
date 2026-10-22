from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user, login_user
from models import db
from models.user import User, Role, UserRole, UserReport, AuditLog, SystemSetting, UserSession
from models.geography import Country, AdministrativeDivision, Continent
from models.marine_and_physical import Ocean, Sea, GeographicFeature, DataSource
from services.data_import_service import DataImportService
from server.connection_manager import ServerConnectionManager
from api.config import API_REGISTRY, update_api_url
from api.gateway import ApiGateway

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    """High-Security Dedicated Admin Login Portal."""
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
            log_admin_action("unauthorized_admin_attempt", "Security", user.id, f"Non-admin user '{user.username}' attempted admin portal login from IP {request.remote_addr}")
            flash("Access denied. High-security administrative privileges required.", "danger")
            return render_template("admin/login.html")

        if user.is_suspended:
            flash("This administrative account has been suspended.", "danger")
            return render_template("admin/login.html")

        # Success - log in and register server connection
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        login_user(user, remember=False)
        ServerConnectionManager.register_connection(user, request)

        log_admin_action("admin_login_success", "Security", user.id, f"Administrator '{user.username}' authenticated successfully from IP {request.remote_addr}")
        flash(f"Welcome to TerraNexus Secure Admin Command, {user.display_name or user.username}!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/login.html")

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Access denied. Administrative privileges are required.", "danger")
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

@admin_bp.route("")
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active_account=True, is_suspended=False).count()
    suspended_users = User.query.filter_by(is_suspended=True).count()
    pending_reports = UserReport.query.filter_by(status="pending").count()

    total_countries = Country.query.count()
    total_oceans = Ocean.query.count()
    total_seas = Sea.query.count()
    total_features = GeographicFeature.query.count()
    total_divisions = AdministrativeDivision.query.count()

    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8).all()
    recent_reports = UserReport.query.order_by(UserReport.created_at.desc()).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        active_users=active_users,
        suspended_users=suspended_users,
        pending_reports=pending_reports,
        total_countries=total_countries,
        total_oceans=total_oceans,
        total_seas=total_seas,
        total_features=total_features,
        total_divisions=total_divisions,
        recent_logs=recent_logs,
        recent_reports=recent_reports
    )

@admin_bp.route("/users")
@admin_required
def users():
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

    return render_template("admin/users.html", users=all_users, roles=roles, search=search, status_filter=status_filter)

@admin_bp.route("/users/<int:user_id>/toggle-suspend", methods=["POST"])
@admin_required
def toggle_suspend_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot suspend your own administrative account.", "danger")
        return redirect(url_for("admin.users"))

    user.is_suspended = not user.is_suspended
    action = "account_suspended" if user.is_suspended else "account_reactivated"
    reason = request.form.get("reason", "Administrative action")
    user.suspension_reason = reason if user.is_suspended else None

    log_admin_action(action, "User", user.id, f"User '{user.username}' was {action}. Reason: {reason}")
    db.session.commit()

    flash(f"User '{user.username}' has been {'suspended' if user.is_suspended else 'reactivated'}.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/users/<int:user_id>/update-role", methods=["POST"])
@admin_required
def update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role_id = request.form.get("role_id")
    role = Role.query.get(new_role_id)

    if not role:
        flash("Invalid role selected.", "danger")
        return redirect(url_for("admin.users"))

    # Remove existing roles and assign new role
    UserRole.query.filter_by(user_id=user.id).delete()
    db.session.add(UserRole(user_id=user.id, role_id=role.id))
    
    log_admin_action("role_changed", "User", user.id, f"Assigned role '{role.name}' to user '{user.username}'")
    db.session.commit()

    flash(f"Role for '{user.username}' updated to '{role.name}'.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/content")
@admin_required
def content_management():
    countries = Country.query.order_by(Country.common_name.asc()).all()
    oceans = Ocean.query.all()
    seas = Sea.query.order_by(Sea.name.asc()).all()
    features = GeographicFeature.query.order_by(GeographicFeature.name.asc()).all()

    return render_template(
        "admin/content.html",
        countries=countries,
        oceans=oceans,
        seas=seas,
        features=features
    )

@admin_bp.route("/reports")
@admin_required
def reports():
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

@admin_bp.route("/audit-logs")
@admin_required
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return render_template("admin/logs.html", logs=logs)

# -------------------------------------------------------------
# User Profile & Password Control by Administrator
# -------------------------------------------------------------
@admin_bp.route("/users/<int:user_id>/reset-password", methods=["POST"])
@admin_required
def reset_user_password(user_id):
    """Admin overrides and resets a user's password."""
    user = User.query.get_or_404(user_id)
    new_password = request.form.get("new_password", "").strip()

    if len(new_password) < 8:
        flash("Password must be at least 8 characters long for security compliance.", "danger")
        return redirect(url_for("admin.users"))

    user.set_password(new_password)
    # Revoke active server sessions for security so user must re-authenticate with new password
    ServerConnectionManager.disconnect_all_user_sessions(user.id, admin_user=current_user)
    db.session.commit()

    log_admin_action("password_reset_by_admin", "User", user.id, f"Admin '{current_user.username}' reset password for '{user.username}' and revoked active sessions.")
    flash(f"Password for user '{user.username}' was successfully reset. All active server sessions have been terminated.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/users/<int:user_id>/edit-profile", methods=["POST"])
@admin_required
def edit_user_profile(user_id):
    """Admin controls and updates all profile data of any user."""
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

    # Check uniqueness
    existing_user = User.query.filter((User.username == username) & (User.id != user.id)).first()
    if existing_user:
        flash(f"Username '{username}' is already taken by another account.", "danger")
        return redirect(url_for("admin.users"))

    existing_email = User.query.filter((User.email == email) & (User.id != user.id)).first()
    if existing_email:
        flash(f"Email '{email}' is already registered to another account.", "danger")
        return redirect(url_for("admin.users"))

    changes = []
    if user.username != username:
        changes.append(f"username: {user.username} -> {username}")
        user.username = username
    if user.email != email:
        changes.append(f"email: {user.email} -> {email}")
        user.email = email
    if user.display_name != display_name:
        changes.append("display_name updated")
        user.display_name = display_name
    if user.bio != bio:
        user.bio = bio
    if user.location != location:
        user.location = location
    if user.is_active_account != is_active_account:
        changes.append(f"active: {user.is_active_account} -> {is_active_account}")
        user.is_active_account = is_active_account

    db.session.commit()
    log_admin_action("profile_edited_by_admin", "User", user.id, f"Admin updated profile for '{user.username}': {', '.join(changes) if changes else 'saved'}")
    flash(f"Profile data for '{user.username}' updated successfully.", "success")
    return redirect(url_for("admin.users"))

# -------------------------------------------------------------
# Server Connection Manager & Remote Session Disconnect
# -------------------------------------------------------------
@admin_bp.route("/connections")
@admin_required
def server_connections():
    """Live Server Connections Monitor."""
    connections = ServerConnectionManager.get_all_connections(active_only=False)
    telemetry = ServerConnectionManager.get_server_telemetry()
    return render_template("admin/connections.html", connections=connections, telemetry=telemetry)

@admin_bp.route("/connections/<int:session_id>/disconnect", methods=["POST"])
@admin_required
def disconnect_session(session_id):
    """Admin disconnects an individual profile server connection."""
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
    """Admin terminates all active server connections for a user profile."""
    user = User.query.get_or_404(user_id)
    success, msg = ServerConnectionManager.disconnect_all_user_sessions(user.id, admin_user=current_user)
    log_admin_action("all_user_sessions_disconnected", "User", user.id, f"Admin severed all active server connection(s) for user '{user.username}'")
    flash(msg, "success" if success else "warning")
    return redirect(request.referrer or url_for("admin.server_connections"))

# -------------------------------------------------------------
# Centralized API Hub & Gateway Monitor
# -------------------------------------------------------------
@admin_bp.route("/apis")
@admin_required
def apis_hub():
    """Centralized API management dashboard - view, test, and swap APIs."""
    all_apis = API_REGISTRY
    return render_template("admin/apis.html", apis=all_apis)

@admin_bp.route("/apis/<api_id>/test", methods=["POST"])
@admin_required
def test_api_connection(api_id):
    """Benchmark and test live latency of any external API."""
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
        log_admin_action("api_endpoint_updated", "API", api_id, f"Admin updated API '{api_id}' endpoint to: {new_url}")
        flash(f"API '{api_id}' URL successfully replaced with: {new_url}", "success")
    else:
        flash(f"API identifier '{api_id}' was not found in registry.", "danger")

    return redirect(url_for("admin.apis_hub"))

