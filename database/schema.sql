-- TerraNexus MySQL Database Schema
-- Character Set: utf8mb4
-- Collation: utf8mb4_unicode_ci

CREATE DATABASE IF NOT EXISTS terranexus_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE terranexus_db;

-- 1. Roles & Permissions
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_roles_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(64) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_permissions_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Users & User Roles
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(120),
    profile_image VARCHAR(255) DEFAULT 'default_avatar.png',
    preferred_language VARCHAR(10) DEFAULT 'en',
    theme_preference VARCHAR(20) DEFAULT 'dark',
    is_active_account BOOLEAN DEFAULT TRUE,
    is_suspended BOOLEAN DEFAULT FALSE,
    suspension_reason VARCHAR(255),
    deletion_requested BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at DATETIME NULL,
    INDEX idx_users_username (username),
    INDEX idx_users_email (email),
    INDEX idx_users_status (is_active_account, is_suspended)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS user_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_role (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    INDEX idx_ur_user (user_id),
    INDEX idx_ur_role (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Continents
CREATE TABLE IF NOT EXISTS continents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(60) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE,
    area_km2 BIGINT NULL,
    population BIGINT NULL,
    population_year INT DEFAULT 2024,
    countries_count INT DEFAULT 0,
    overview TEXT NULL,
    climate_zones VARCHAR(255) NULL,
    highest_point VARCHAR(100) NULL,
    lowest_point VARCHAR(100) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_continents_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Countries
CREATE TABLE IF NOT EXISTS countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iso_a2 CHAR(2) NOT NULL UNIQUE,
    iso_a3 CHAR(3) NOT NULL UNIQUE,
    iso_numeric CHAR(3) NULL,
    common_name VARCHAR(100) NOT NULL,
    official_name VARCHAR(200) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    continent_id INT NOT NULL,
    subregion VARCHAR(100) NULL,
    flag_emoji VARCHAR(16) NULL,
    flag_svg_url VARCHAR(255) NULL,
    capital_name VARCHAR(100) NULL,
    largest_city VARCHAR(100) NULL,
    area_km2 FLOAT NULL,
    area_sq_mi FLOAT NULL,
    land_area_km2 FLOAT NULL,
    water_area_km2 FLOAT NULL,
    population BIGINT NULL,
    population_year INT DEFAULT 2024,
    population_density FLOAT NULL,
    urban_population_pct FLOAT NULL,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    highest_point VARCHAR(120) NULL,
    highest_elevation_m INT NULL,
    lowest_point VARCHAR(120) NULL,
    lowest_elevation_m INT NULL,
    coastline_km FLOAT NULL,
    is_landlocked BOOLEAN DEFAULT FALSE,
    currency_code VARCHAR(10) NULL,
    currency_name VARCHAR(100) NULL,
    currency_symbol VARCHAR(10) NULL,
    official_languages VARCHAR(255) NULL,
    widely_spoken_languages VARCHAR(255) NULL,
    demonym VARCHAR(80) NULL,
    calling_code VARCHAR(20) NULL,
    tld VARCHAR(10) NULL,
    time_zones VARCHAR(150) NULL,
    driving_side VARCHAR(10) DEFAULT 'right',
    government_system VARCHAR(150) NULL,
    head_of_state VARCHAR(150) NULL,
    head_of_government VARCHAR(150) NULL,
    independence_date VARCHAR(100) NULL,
    gdp_usd_billions FLOAT NULL,
    gdp_per_capita_usd FLOAT NULL,
    gdp_reference_year INT DEFAULT 2024,
    major_industries TEXT NULL,
    natural_resources TEXT NULL,
    climate TEXT NULL,
    overview TEXT NULL,
    data_source VARCHAR(100) DEFAULT 'Natural Earth / World Bank / UN',
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (continent_id) REFERENCES continents(id),
    INDEX idx_countries_iso2 (iso_a2),
    INDEX idx_countries_iso3 (iso_a3),
    INDEX idx_countries_slug (slug),
    INDEX idx_countries_name (common_name),
    INDEX idx_countries_continent (continent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Country Names & Multilingual Alternate Names
CREATE TABLE IF NOT EXISTS country_names (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    language_code VARCHAR(10) DEFAULT 'en',
    name_type VARCHAR(30) DEFAULT 'alt',
    name_value VARCHAR(200) NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE,
    INDEX idx_cn_lookup (name_value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Capitals
CREATE TABLE IF NOT EXISTS capitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    capital_type VARCHAR(50) DEFAULT 'primary',
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    elevation_m INT NULL,
    population BIGINT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE,
    INDEX idx_capitals_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Borders (Land & Maritime)
CREATE TABLE IF NOT EXISTS borders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_a_iso CHAR(3) NOT NULL,
    country_b_iso CHAR(3) NOT NULL,
    border_type VARCHAR(30) DEFAULT 'land',
    length_km FLOAT NULL,
    UNIQUE KEY uq_border_pair (country_a_iso, country_b_iso, border_type),
    INDEX idx_border_a (country_a_iso),
    INDEX idx_border_b (country_b_iso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Administrative Divisions
CREATE TABLE IF NOT EXISTS administrative_divisions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    parent_division_id INT NULL,
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(180) NOT NULL,
    code VARCHAR(30) NULL,
    division_type VARCHAR(60) NOT NULL,
    capital_or_center VARCHAR(100) NULL,
    area_km2 FLOAT NULL,
    population BIGINT NULL,
    population_year INT DEFAULT 2024,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_division_id) REFERENCES administrative_divisions(id) ON DELETE CASCADE,
    INDEX idx_ad_country (country_id),
    INDEX idx_ad_parent (parent_division_id),
    INDEX idx_ad_slug (slug),
    INDEX idx_ad_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Cities
CREATE TABLE IF NOT EXISTS cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    division_id INT NULL,
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(150) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    population BIGINT NULL,
    elevation_m INT NULL,
    is_capital BOOLEAN DEFAULT FALSE,
    is_major_port BOOLEAN DEFAULT FALSE,
    airport_code VARCHAR(10) NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE,
    FOREIGN KEY (division_id) REFERENCES administrative_divisions(id) ON DELETE SET NULL,
    INDEX idx_cities_country (country_id),
    INDEX idx_cities_name (name),
    INDEX idx_cities_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Oceans
CREATE TABLE IF NOT EXISTS oceans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    area_km2 BIGINT NOT NULL,
    volume_km3 BIGINT NULL,
    avg_depth_m INT NULL,
    max_depth_m INT NULL,
    max_depth_location VARCHAR(120) NULL,
    surrounding_continents VARCHAR(255) NULL,
    major_marginal_seas TEXT NULL,
    major_currents TEXT NULL,
    major_trenches TEXT NULL,
    major_ridges TEXT NULL,
    overview TEXT NOT NULL,
    marine_biodiversity TEXT NULL,
    economic_importance TEXT NULL,
    environmental_challenges TEXT NULL,
    historical_exploration TEXT NULL,
    data_source VARCHAR(150) DEFAULT 'NOAA / IHO / GEBCO',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_oceans_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. Seas
CREATE TABLE IF NOT EXISTS seas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(120) NOT NULL UNIQUE,
    alternative_names VARCHAR(255) NULL,
    ocean_id INT NULL,
    sea_type VARCHAR(50) DEFAULT 'marginal',
    area_km2 FLOAT NULL,
    avg_depth_m INT NULL,
    max_depth_m INT NULL,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    surrounding_countries TEXT NULL,
    connected_water_bodies TEXT NULL,
    major_ports TEXT NULL,
    major_currents TEXT NULL,
    marine_life TEXT NULL,
    economic_importance TEXT NULL,
    environmental_concerns TEXT NULL,
    historical_significance TEXT NULL,
    overview TEXT NOT NULL,
    data_source VARCHAR(150) DEFAULT 'International Hydrographic Organization (IHO)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ocean_id) REFERENCES oceans(id) ON DELETE SET NULL,
    INDEX idx_seas_slug (slug),
    INDEX idx_seas_ocean (ocean_id),
    INDEX idx_seas_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. Geographic Features (Physical & Marine)
CREATE TABLE IF NOT EXISTS geographic_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(150) NOT NULL UNIQUE,
    alternative_names VARCHAR(255) NULL,
    feature_type VARCHAR(50) NOT NULL,
    continent_id INT NULL,
    primary_country_iso CHAR(3) NULL,
    countries_involved VARCHAR(255) NULL,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    elevation_m INT NULL,
    depth_m INT NULL,
    length_km FLOAT NULL,
    area_km2 FLOAT NULL,
    connected_features VARCHAR(255) NULL,
    overview TEXT NOT NULL,
    data_source VARCHAR(150) DEFAULT 'GeoNames / USGS / UNESCO',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (continent_id) REFERENCES continents(id) ON DELETE SET NULL,
    INDEX idx_gf_type (feature_type),
    INDEX idx_gf_slug (slug),
    INDEX idx_gf_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. User Favorites, Saved Locations, Collections
CREATE TABLE IF NOT EXISTS user_favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_type VARCHAR(32) NOT NULL,
    item_id VARCHAR(100) NOT NULL,
    item_title VARCHAR(150) NOT NULL,
    item_subtitle VARCHAR(150) NULL,
    item_flag VARCHAR(50) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_favorite (user_id, item_type, item_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_uf_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS saved_locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    zoom_level INT DEFAULT 6,
    notes TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sl_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS user_collections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_uc_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS collection_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    collection_id INT NOT NULL,
    item_type VARCHAR(32) NOT NULL,
    item_id VARCHAR(100) NOT NULL,
    item_title VARCHAR(150) NOT NULL,
    notes TEXT NULL,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (collection_id) REFERENCES user_collections(id) ON DELETE CASCADE,
    INDEX idx_ci_collection (collection_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 14. Data Sources, Reports & Audit Logs
CREATE TABLE IF NOT EXISTS data_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    category VARCHAR(60) NOT NULL,
    organization VARCHAR(150) NULL,
    url VARCHAR(255) NULL,
    license VARCHAR(100) NULL,
    description TEXT NULL,
    record_count INT DEFAULT 0,
    last_synced_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS user_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    report_type VARCHAR(50) NOT NULL,
    subject_type VARCHAR(50) NOT NULL,
    subject_id VARCHAR(100) NOT NULL,
    subject_name VARCHAR(150) NULL,
    description TEXT NOT NULL,
    suggested_correction TEXT NULL,
    status VARCHAR(30) DEFAULT 'pending',
    admin_notes TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_ur_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS admin_audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NULL,
    admin_username VARCHAR(80) NULL,
    action VARCHAR(80) NOT NULL,
    resource_type VARCHAR(80) NOT NULL,
    resource_id VARCHAR(100) NULL,
    details TEXT NULL,
    ip_address VARCHAR(45) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_al_action (action),
    INDEX idx_al_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `key` VARCHAR(100) NOT NULL UNIQUE,
    value TEXT NULL,
    description VARCHAR(255) NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_ss_key (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
