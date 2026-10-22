from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User, Role, UserRole, UserFavorite, SavedLocation
from server.connection_manager import ServerConnectionManager

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        display_name = request.form.get("display_name", "").strip() or username

        # Validations
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        if len(username) < 3:
            flash("Username must be at least 3 characters long.", "danger")
            return render_template("auth/register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        # Check existing user (generic message for privacy where needed)
        if User.query.filter_by(username=username).first():
            flash("That username is already taken. Please choose another.", "warning")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "warning")
            return render_template("auth/register.html")

        new_user = User(
            username=username,
            email=email,
            display_name=display_name,
            preferred_language="en",
            theme_preference="dark"
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()

        # Assign Registered User role
        reg_role = Role.query.filter_by(name="Registered User").first()
        if reg_role:
            db.session.add(UserRole(user_id=new_user.id, role_id=reg_role.id))

        db.session.commit()

        login_user(new_user)
        ServerConnectionManager.register_connection(new_user, request)
        flash(f"Welcome to TerraNexus, {new_user.display_name}! Your exploration begins now.", "success")
        return redirect(url_for("main.index"))

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        # Allow login by username or email
        user = User.query.filter((User.username == login_id) | (User.email == login_id.lower())).first()

        if user and user.check_password(password):
            if user.is_suspended:
                flash("Your account has been suspended by an administrator. Please contact support.", "danger")
                return render_template("auth/login.html")

            user.last_login_at = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=remember)
            ServerConnectionManager.register_connection(user, request)

            flash(f"Welcome back, {user.display_name or user.username}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))
        else:
            flash("Invalid credentials. Please verify your login and password.", "danger")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    token = session.get("tn_session_token")
    if token:
        from models.user import UserSession
        s = UserSession.query.filter_by(session_token=token).first()
        if s:
            s.is_active = False
            db.session.commit()
        session.pop("tn_session_token", None)
    logout_user()
    flash("You have successfully signed out.", "info")
    return redirect(url_for("main.index"))

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        preferred_lang = request.form.get("preferred_language", "en")
        theme_pref = request.form.get("theme_preference", "dark")

        if display_name:
            current_user.display_name = display_name
        current_user.preferred_language = preferred_lang
        current_user.theme_preference = theme_pref
        db.session.commit()

        flash("Profile preferences updated successfully.", "success")
        return redirect(url_for("auth.profile"))

    favorites_count = current_user.favorites.count()
    saved_locations_count = current_user.saved_locations.count()
    return render_template(
        "auth/profile.html",
        favorites_count=favorites_count,
        saved_locations_count=saved_locations_count
    )

@auth_bp.route("/favorites")
@login_required
def favorites():
    all_favorites = current_user.favorites.order_by(UserFavorite.created_at.desc()).all()
    return render_template("auth/favorites.html", favorites=all_favorites)

@auth_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "change_password":
            current_pw = request.form.get("current_password", "")
            new_pw = request.form.get("new_password", "")
            confirm_new_pw = request.form.get("confirm_new_password", "")

            if not current_user.check_password(current_pw):
                flash("Current password is incorrect.", "danger")
            elif len(new_pw) < 8:
                flash("New password must be at least 8 characters.", "danger")
            elif new_pw != confirm_new_pw:
                flash("New passwords do not match.", "danger")
            else:
                current_user.set_password(new_pw)
                db.session.commit()
                flash("Password updated successfully.", "success")
        elif action == "update_appearance":
            theme = request.form.get("theme_preference", "dark")
            current_user.theme_preference = theme
            db.session.commit()
            flash(f"Appearance theme switched to {'Dark Cosmos' if theme == 'dark' else 'Light Atlas'}.", "success")
        elif action == "delete_account_request":
            current_user.deletion_requested = True
            db.session.commit()
            flash("Your account deletion request has been submitted to system administrators.", "warning")

        return redirect(url_for("auth.settings"))

    return render_template("auth/settings.html")

@auth_bp.route("/api/theme", methods=["POST"])
def update_theme_api():
    data = request.get_json(silent=True) or request.form
    theme = data.get("theme", "dark")
    if theme in ("dark", "light") and current_user.is_authenticated:
        current_user.theme_preference = theme
        db.session.commit()
        return {"status": "success", "theme": theme}
    return {"status": "ok", "theme": theme}
