# TerraNexus

<p align="center">
  <img src="static/images/logo.png" alt="TerraNexus Logo" width="120" height="120" style="border-radius: 50%;">
</p>

<p align="center">
  <strong>"Explore the World. Discover Every Connection."</strong><br>
  <em>One Planet. Every Place. Infinite Knowledge.</em>
</p>

---

## 🌍 Overview

**TerraNexus** is an open, global geography exploration platform built with Python Flask, MySQL, and Leaflet.js. It allows users to explore planet Earth through an interactive world map and discover verified encyclopedic data regarding countries, capitals, currencies, languages, administrative divisions, cities, oceans, seas, islands, rivers, and mountains.

---

## ✨ Key Features

1. **Interactive World Map**: Built with Leaflet.js, featuring CartoDB dark matter and OpenStreetMap standard tiles, GeoJSON boundary highlighting, coordinate tracking, custom marker overlays (capitals, seas, physical features), and interactive slideout dossier panels.
2. **Countries Encyclopedia**: Comprehensive dossiers for world nations featuring ISO codes, official names, capitals, currencies, official and regional languages, areas, population metrics, elevations, and administrative hierarchies.
3. **Indian & Global Administrative Divisions**: Country-specific administrative structures including Indian States & Union Territories with district hierarchies (e.g., Maharashtra with Mumbai, Pune, Nagpur, Thane), US States, Japanese Prefectures, and German Bundesländer.
4. **Hydrographic Encyclopedia**: Dedicated sections for Earth's 5 major oceans and cataloged seas (Arabian Sea, Mediterranean, Caribbean, South China Sea, Red Sea, Black Sea, Caspian Sea, etc.) with depths, sounding trenches, and littoral nations.
5. **Physical Geomorphological Formations**: Mountains (Mount Everest, K2), mountain ranges (Himalayas, Andes), rivers (Nile, Amazon, Ganga), deserts (Sahara), straits (Strait of Gibraltar), and trenches (Mariana Trench).
6. **Global Search Engine**: High-performance debounced live search with autocomplete, category chips, keyboard navigation, and disambiguation (e.g., distinguishing the country of Georgia from the US state of Georgia).
7. **Secure Authentication & Roles**: Role-based access control (Guest, Registered User, Moderator, Administrator, Super Administrator) with password hashing via Werkzeug, session protection, and CSRF security.
8. **User Profiles & Personal Favorites**: Save favorite countries, oceans, seas, and geographical features with one-click toggling.
9. **Administrator Dashboard**: Full management console at `/admin` for user management (suspension toggles, role assignments), geographic content review, GeoJSON ingestion validation, correction report review, and security audit logs.
10. **Installable PWA**: Progressive Web App with `manifest.json`, service worker offline shell caching, and responsive design across desktop, tablet, and mobile devices.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.12+, Flask 3.1+, Flask-SQLAlchemy, Flask-Login, Flask-WTF, PyMySQL
- **Database**: MySQL 8.0+ (with automatic SQLite fallback for local development)
- **Frontend**: HTML5, CSS3 (custom glassmorphic theme with Dark Cosmos and Light Atlas themes), Vanilla JavaScript (ES6+)
- **Mapping**: Leaflet.js 1.9.4 & GeoJSON
- **PWA**: Web App Manifest, Service Worker (`sw.js`)

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.10+
- MySQL 8.0+ (optional, will fallback to local SQLite if omitted)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/msunil06/TerraNexus.git
cd TerraNexus

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optionally enter your MySQL credentials into `.env`, or leave as is to run on SQLite)*

### 4. Database Initialization & Seeding
```bash
python database/seed_data.py
```

### 5. Running the Application
```bash
python app.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 🛡️ Administrative Access Control

Administrative access is managed via environment configuration and role-based access control (RBAC). Authorized administrators configure accounts and credentials privately via their environment configuration (`.env`). Default credentials are not distributed in repository commits.

---

## 🧪 Automated Test Suite

TerraNexus includes comprehensive unit, integration, and end-to-end journey tests. Run the test suite:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

All 12 automated test suites verify search normalization, country code translations, missing data handling, cryptographic password hashing, role permissions, routes, and end-to-end user lifecycles.

---

## 📚 Project Documentation

- [Database Setup Guide](docs/DATABASE_SETUP.md)
- [REST API Documentation](docs/API_DOCUMENTATION.md)
- [Authoritative Data Sources & Licenses](docs/DATA_SOURCES.md)
- [Production Deployment Guide](docs/DEPLOYMENT.md)
- [Backup and Disaster Recovery](docs/BACKUP_AND_RECOVERY.md)
- [First Administrator Setup](docs/ADMIN_SETUP.md)
- [External APIs & Tile Providers](docs/EXTERNAL_APIS.md)
- [Limitations & Roadmap](docs/LIMITATIONS.md)
- [MySQL Schema DDL](database/schema.sql)

---

## 📄 License & Attribution

- Platform code is open source under the MIT License.
- Geographic boundaries and vector layers are derived from **Natural Earth** (Public Domain / CC0).
- Placename gazetteers are derived from **GeoNames** (CC BY 4.0).
- Economic and demographic indicators are derived from **World Bank Open Data** (CC BY 4.0).
- Marine limits are cataloged per **International Hydrographic Organization (IHO S-23)** standards.
