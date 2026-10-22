# First Administrator Setup Guide

TerraNexus enforces role-based authorization in the Python backend. Public registration grants the **Registered User** role by default. Administrative access is strictly restricted.

---

## 1. Initial Administrator Account Provisioning

During database initialization, an administrative account is provisioned using parameters defined in your environment:

- **Username**: Configured via `ADMIN_USERNAME` in `.env` (default: `admin`)
- **Email**: Configured via `ADMIN_EMAIL` in `.env` (default: `admin@terranexus.internal`)
- **Password**: Configured securely via `ADMIN_DEFAULT_PASSWORD` in `.env`
- **Assigned Role**: `Super Administrator`

> [!IMPORTANT]
> Always define strong credentials in `.env` and never commit production credentials to public version control.

---

## 2. Promoting a User via Python CLI

To promote any registered user to an Administrator or Super Administrator via Python terminal without exposing credentials in HTTP traffic:

```python
from app import create_app
from models import db
from models.user import User, Role, UserRole

app = create_app()
with app.app_context():
    # Find user by username
    user = User.query.filter_by(username="your_username").first()
    admin_role = Role.query.filter_by(name="Super Administrator").first()
    
    if user and admin_role:
        # Check if already assigned
        existing = UserRole.query.filter_by(user_id=user.id, role_id=admin_role.id).first()
        if not existing:
            db.session.add(UserRole(user_id=user.id, role_id=admin_role.id))
            db.session.commit()
            print(f"User '{user.username}' successfully promoted to Super Administrator.")
```

---

## 3. Administrative Roles Hierarchy

1. **Guest**: Unauthenticated public visitors (can browse map, encyclopedia, search).
2. **Registered User**: Can save favorite countries, bookmark map locations, and submit correction reports.
3. **Moderator**: Can review and triage user correction reports.
4. **Administrator**: Can manage users, suspend accounts, and view audit logs.
5. **Super Administrator**: Full administrative authority, role elevation, and system configuration.
