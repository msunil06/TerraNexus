import uuid
from datetime import datetime
from flask import session, request
from models import db
from models.user import UserSession, User, AuditLog

class ServerConnectionManager:
    """
    Manages client-server connections and user sessions.
    Allows administrators to monitor all active profile sessions and
    terminate/disconnect any connection in real-time.
    """

    @staticmethod
    def register_connection(user, req):
        """Register a new active server connection for an authenticated user."""
        try:
            token = str(uuid.uuid4())
            ip_addr = req.headers.get("X-Forwarded-For", req.remote_addr)
            user_agent = req.headers.get("User-Agent", "Unknown Device")[:250]

            # Detect basic device type
            ua_lower = user_agent.lower()
            if "mobile" in ua_lower or "android" in ua_lower or "iphone" in ua_lower:
                device_type = "📱 Mobile"
            elif "tablet" in ua_lower or "ipad" in ua_lower:
                device_type = "📲 Tablet"
            else:
                device_type = "💻 Desktop"

            user_session = UserSession(
                session_token=token,
                user_id=user.id,
                ip_address=ip_addr,
                user_agent=user_agent,
                device_type=device_type,
                is_active=True,
                created_at=datetime.utcnow(),
                last_activity=datetime.utcnow()
            )
            db.session.add(user_session)
            db.session.commit()

            session["tn_session_token"] = token
            return token
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def validate_connection(user):
        """
        Check if the current user's session token is still active.
        If an administrator has disconnected the server connection, return False.
        """
        token = session.get("tn_session_token")
        if not token:
            return True # Session cookie not set yet, fallback to normal Flask-Login

        user_session = UserSession.query.filter_by(session_token=token, user_id=user.id).first()
        if not user_session or not user_session.is_active:
            return False

        # Update last activity timestamp periodically
        try:
            user_session.last_activity = datetime.utcnow()
            db.session.commit()
        except Exception:
            db.session.rollback()

        return True

    @staticmethod
    def get_all_connections(active_only=True):
        """Retrieve list of server connections and sessions."""
        query = UserSession.query
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(UserSession.last_activity.desc()).all()

    @staticmethod
    def disconnect_session(session_id, admin_user=None):
        """Admin force-disconnect a specific session by ID."""
        user_session = UserSession.query.get(session_id)
        if not user_session:
            return False, "Session connection not found"

        user_session.is_active = False
        target_user = user_session.user

        # Audit log the action
        if admin_user:
            try:
                log = AuditLog(
                    admin_id=admin_user.id,
                    admin_username=admin_user.username,
                    action="server_connection_terminated",
                    resource_type="UserSession",
                    resource_id=str(session_id),
                    details=f"Admin disconnected active session for user '{target_user.username}' (IP: {user_session.ip_address})"
                )
                db.session.add(log)
            except Exception:
                pass

        db.session.commit()
        return True, f"Server connection for '{target_user.username}' terminated successfully."

    @staticmethod
    def disconnect_all_user_sessions(user_id, admin_user=None):
        """Admin force-disconnect all active server connections for a specific user profile."""
        user = User.query.get(user_id)
        if not user:
            return False, "User profile not found"

        sessions = UserSession.query.filter_by(user_id=user.id, is_active=True).all()
        for s in sessions:
            s.is_active = False

        if admin_user:
            try:
                log = AuditLog(
                    admin_id=admin_user.id,
                    admin_username=admin_user.username,
                    action="all_user_connections_terminated",
                    resource_type="User",
                    resource_id=str(user.id),
                    details=f"Admin disconnected ALL active server connections for profile '{user.username}' ({len(sessions)} connections terminated)"
                )
                db.session.add(log)
            except Exception:
                pass

        db.session.commit()
        return True, f"All {len(sessions)} active server connections for '{user.username}' have been disconnected."

    @staticmethod
    def get_server_telemetry():
        """Get live server telemetry stats for admin dashboard."""
        import platform
        import os

        active_count = UserSession.query.filter_by(is_active=True).count()
        total_sessions = UserSession.query.count()

        return {
            "server_os": f"{platform.system()} {platform.release()}",
            "python_version": platform.python_version(),
            "active_connections": active_count,
            "total_historical_sessions": total_sessions,
            "process_id": os.getpid(),
            "server_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
