from datetime import datetime
from models import db

class Ocean(db.Model):
    __tablename__ = "oceans"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    area_km2 = db.Column(db.BigInteger, nullable=False)
    volume_km3 = db.Column(db.BigInteger, nullable=True)
    avg_depth_m = db.Column(db.Integer, nullable=True)
    max_depth_m = db.Column(db.Integer, nullable=True)
    max_depth_location = db.Column(db.String(120), nullable=True) # e.g. 'Mariana Trench (Challenger Deep)'
    
    surrounding_continents = db.Column(db.String(255), nullable=True)
    major_marginal_seas = db.Column(db.Text, nullable=True)
    major_currents = db.Column(db.Text, nullable=True)
    major_trenches = db.Column(db.Text, nullable=True)
    major_ridges = db.Column(db.Text, nullable=True)
    
    overview = db.Column(db.Text, nullable=False)
    marine_biodiversity = db.Column(db.Text, nullable=True)
    economic_importance = db.Column(db.Text, nullable=True)
    environmental_challenges = db.Column(db.Text, nullable=True)
    historical_exploration = db.Column(db.Text, nullable=True)
    
    data_source = db.Column(db.String(150), default="NOAA / IHO / GEBCO")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    seas = db.relationship("Sea", backref="ocean", lazy="dynamic")

    def __repr__(self):
        return f"<Ocean {self.name}>"

class Sea(db.Model):
    __tablename__ = "seas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    alternative_names = db.Column(db.String(255), nullable=True)
    
    ocean_id = db.Column(db.Integer, db.ForeignKey("oceans.id", ondelete="SET NULL"), nullable=True, index=True)
    sea_type = db.Column(db.String(50), default="marginal") # marginal, inland, mediterranean, enclosed, gulf/bay
    
    area_km2 = db.Column(db.Float, nullable=True)
    avg_depth_m = db.Column(db.Integer, nullable=True)
    max_depth_m = db.Column(db.Integer, nullable=True)
    
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    surrounding_countries = db.Column(db.Text, nullable=True)
    connected_water_bodies = db.Column(db.Text, nullable=True)
    major_ports = db.Column(db.Text, nullable=True)
    major_currents = db.Column(db.Text, nullable=True)
    
    marine_life = db.Column(db.Text, nullable=True)
    economic_importance = db.Column(db.Text, nullable=True)
    environmental_concerns = db.Column(db.Text, nullable=True)
    historical_significance = db.Column(db.Text, nullable=True)
    
    overview = db.Column(db.Text, nullable=False)
    data_source = db.Column(db.String(150), default="International Hydrographic Organization (IHO)")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Sea {self.name}>"

class GeographicFeature(db.Model):
    __tablename__ = "geographic_features"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    alternative_names = db.Column(db.String(255), nullable=True)
    
    feature_type = db.Column(db.String(50), nullable=False, index=True) 
    # 'mountain', 'mountain_range', 'river', 'lake', 'desert', 'island', 'archipelago', 'peninsula', 'strait', 'gulf', 'bay', 'trench', 'waterfall', 'plateau', 'reef'
    
    continent_id = db.Column(db.Integer, db.ForeignKey("continents.id", ondelete="SET NULL"), nullable=True, index=True)
    primary_country_iso = db.Column(db.String(3), nullable=True, index=True)
    countries_involved = db.Column(db.String(255), nullable=True)
    
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    elevation_m = db.Column(db.Integer, nullable=True)
    depth_m = db.Column(db.Integer, nullable=True)
    length_km = db.Column(db.Float, nullable=True)
    area_km2 = db.Column(db.Float, nullable=True)
    
    connected_features = db.Column(db.String(255), nullable=True)
    overview = db.Column(db.Text, nullable=False)
    data_source = db.Column(db.String(150), default="GeoNames / USGS / UNESCO")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<GeographicFeature {self.name} ({self.feature_type})>"

class DataSource(db.Model):
    __tablename__ = "data_sources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(60), nullable=False) # 'Boundaries', 'Statistics', 'Marine', 'Physical', 'Gazetteer'
    organization = db.Column(db.String(150), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    license = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    record_count = db.Column(db.Integer, default=0)
    last_synced_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DataSource {self.name}>"
