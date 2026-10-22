from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models import db

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Permission {self.code}>"

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("UserRole", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role {self.name}>"

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120))
    profile_image = db.Column(db.String(255), default="default_avatar.png")
    preferred_language = db.Column(db.String(10), default="en")
    theme_preference = db.Column(db.String(20), default="dark") # 'dark' or 'light'
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(120), nullable=True)
    
    is_active_account = db.Column(db.Boolean, default=True)
    is_suspended = db.Column(db.Boolean, default=False)
    suspension_reason = db.Column(db.String(255), nullable=True)
    deletion_requested = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)

    roles = db.relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    favorites = db.relationship("UserFavorite", backref="user", cascade="all, delete-orphan", lazy="dynamic")
    saved_locations = db.relationship("SavedLocation", backref="user", cascade="all, delete-orphan", lazy="dynamic")
    collections = db.relationship("UserCollection", backref="user", cascade="all, delete-orphan", lazy="dynamic")
    reports = db.relationship("UserReport", backref="user", lazy="dynamic")

    @property
    def is_active(self):
        return self.is_active_account and not self.is_suspended

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return any(ur.role.name.lower() == role_name.lower() for ur in self.roles if ur.role)

    @property
    def is_admin(self):
        return any(ur.role and ("admin" in ur.role.name.lower()) for ur in self.roles)

    @property
    def is_moderator(self):
        return self.is_admin or self.has_role("moderator")

    def __repr__(self):
        return f"<User {self.username}>"

class UserRole(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="roles")
    role = db.relationship("Role", back_populates="users")

class UserFavorite(db.Model):
    __tablename__ = "user_favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    item_type = db.Column(db.String(32), nullable=False) # 'country', 'ocean', 'sea', 'continent', 'feature'
    item_id = db.Column(db.String(100), nullable=False)  # code or slug
    item_title = db.Column(db.String(150), nullable=False)
    item_subtitle = db.Column(db.String(150), nullable=True)
    item_flag = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "item_type", "item_id", name="uq_user_favorite_item"),
    )

class SavedLocation(db.Model):
    __tablename__ = "saved_locations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    zoom_level = db.Column(db.Integer, default=6)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserCollection(db.Model):
    __tablename__ = "user_collections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("CollectionItem", backref="collection", cascade="all, delete-orphan", lazy="dynamic")

class CollectionItem(db.Model):
    __tablename__ = "collection_items"

    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("user_collections.id", ondelete="CASCADE"), nullable=False, index=True)
    item_type = db.Column(db.String(32), nullable=False)
    item_id = db.Column(db.String(100), nullable=False)
    item_title = db.Column(db.String(150), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserReport(db.Model):
    __tablename__ = "user_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    report_type = db.Column(db.String(50), nullable=False) # 'incorrect_info', 'missing_feature', 'boundary_issue', 'translation', 'outdated_stat'
    subject_type = db.Column(db.String(50), nullable=False) # 'country', 'ocean', 'sea', 'division', 'feature'
    subject_id = db.Column(db.String(100), nullable=False)
    subject_name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=False)
    suggested_correction = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default="pending", index=True) # pending, in_review, resolved, dismissed
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

class AuditLog(db.Model):
    __tablename__ = "admin_audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    admin_username = db.Column(db.String(80))
    action = db.Column(db.String(80), nullable=False, index=True) # e.g., 'role_changed', 'account_suspended', 'content_updated'
    resource_type = db.Column(db.String(80), nullable=False)
    resource_id = db.Column(db.String(100), nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class SystemSetting(db.Model):
    __tablename__ = "system_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(128), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    device_type = db.Column(db.String(50), default="Desktop / Mobile")
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("sessions", cascade="all, delete-orphan", lazy="dynamic"))

    def __repr__(self):
        return f"<UserSession {self.session_token[:8]} (User {self.user_id}) Active={self.is_active}>"
