from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from models import db
from models.user import User, Role, UserRole, UserReport, AuditLog, SystemSetting
from models.geography import Country, AdministrativeDivision, Continent
from models.marine_and_physical import Ocean, Sea, GeographicFeature, DataSource
from services.data_import_service import DataImportService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

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
