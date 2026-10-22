# TerraNexus Database Setup Guide (MySQL & SQLite)

This document provides step-by-step instructions for provisioning, configuring, and migrating the database for TerraNexus.

---

## 1. Primary Database: MySQL 8.0+

TerraNexus uses MySQL with the `InnoDB` storage engine and `utf8mb4_unicode_ci` collation for multilingual support (country names in native scripts, diacritics, and emoji flags).

### A. Creating the Database and User

Connect to your MySQL server as `root` or an administrative user:

```bash
mysql -u root -p
```

Execute the following commands to create the database and a dedicated application user:

```sql
CREATE DATABASE IF NOT EXISTS terranexus_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'terranexus_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';

GRANT ALL PRIVILEGES ON terranexus_db.* TO 'terranexus_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### B. Applying the Schema DDL

Execute the provided schema file:

```bash
mysql -u terranexus_user -p terranexus_db < database/schema.sql
```

The schema creates all essential tables:
- `roles`, `permissions`, `role_permissions`
- `users`, `user_roles`, `user_favorites`, `saved_locations`, `user_collections`, `collection_items`
- `continents`, `countries`, `country_names`, `capitals`, `borders`, `administrative_divisions`, `cities`
- `oceans`, `seas`, `geographic_features`, `data_sources`
- `user_reports`, `admin_audit_logs`, `system_settings`

---

## 2. Configuration (`.env`)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set the database connection parameters in `.env`:

```ini
MYSQL_USER=terranexus_user
MYSQL_PASSWORD=StrongPassword123!
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=terranexus_db

# Or direct connection string:
DATABASE_URL=mysql+pymysql://terranexus_user:StrongPassword123!@localhost:3306/terranexus_db?charset=utf8mb4
```

---

## 3. Seeding Authoritative Data

Run the seed script to populate continents, verified countries, capitals, borders, Indian and world administrative divisions, oceans, seas, and physical landmarks:

```bash
python database/seed_data.py
```

Or using Flask CLI:

```bash
flask init-db
```

---

## 4. Local Development Fallback (SQLite)

If MySQL is not installed or configured, TerraNexus automatically falls back to a local SQLite database (`terranexus.db`) stored in the workspace directory. Both MySQL and SQLite schemas maintain identical ORM mapping and tests run in-memory for instant feedback.
