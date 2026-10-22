import os
from flask import Flask, render_template
from config import Config
from models import db, login_manager
from models.user import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.countries import countries_bp
    from routes.continents import continents_bp
    from routes.oceans import oceans_bp
    from routes.seas import seas_bp
    from routes.features import features_bp
    from routes.api import api_bp
    from routes.admin import admin_bp
    from routes.maps import maps_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(continents_bp)
    app.register_blueprint(oceans_bp)
    app.register_blueprint(seas_bp)
    app.register_blueprint(features_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(maps_bp)

    @app.before_request
    def check_server_connection():
        from flask_login import current_user, logout_user
        from flask import request, redirect, url_for, flash
        if current_user.is_authenticated:
            # Don't intercept static assets or auth logout
            if request.endpoint and (request.endpoint.startswith("static") or request.endpoint == "auth.logout"):
                return
            from server.connection_manager import ServerConnectionManager
            if not ServerConnectionManager.validate_connection(current_user):
                logout_user()
                flash("Your server session has been terminated by an administrator or has expired.", "warning")
                return redirect(url_for("auth.login"))

    # Context processors
    @app.context_processor
    def inject_global_data():
        return {
            "app_name": app.config.get("APP_NAME", "TerraNexus"),
            "tagline": app.config.get("TAGLINE", "Explore the World. Discover Every Connection."),
            "secondary_tagline": app.config.get("SECONDARY_TAGLINE", "One Planet. Every Place. Infinite Knowledge.")
        }

    # Custom Error Handlers
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # CLI command to initialize and seed database
    @app.cli.command("init-db")
    def init_db():
        """Initialize database tables and run verified seed data."""
        from database.seed_data import run_all_seeds
        db.create_all()
        run_all_seeds(app)
        print("Database initialized and seeded successfully.")

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        from database.seed_data import run_all_seeds
        # Seed if empty
        if User.query.count() == 0:
            run_all_seeds(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
