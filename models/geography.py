from datetime import datetime
from models import db

class Continent(db.Model):
    __tablename__ = "continents"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(60), unique=True, nullable=False, index=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    area_km2 = db.Column(db.BigInteger, nullable=True)
    population = db.Column(db.BigInteger, nullable=True)
    population_year = db.Column(db.Integer, default=2024)
    countries_count = db.Column(db.Integer, default=0)
    overview = db.Column(db.Text, nullable=True)
    climate_zones = db.Column(db.String(255), nullable=True)
    highest_point = db.Column(db.String(100), nullable=True)
    lowest_point = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    countries = db.relationship("Country", backref="continent_rel", lazy="dynamic")

    def __repr__(self):
        return f"<Continent {self.name}>"

class Country(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    iso_a2 = db.Column(db.String(2), unique=True, nullable=False, index=True)
    iso_a3 = db.Column(db.String(3), unique=True, nullable=False, index=True)
    iso_numeric = db.Column(db.String(3), nullable=True)
    common_name = db.Column(db.Unicode(150), nullable=False, index=True)
    official_name = db.Column(db.Unicode(255), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    
    continent_id = db.Column(db.Integer, db.ForeignKey("continents.id"), nullable=False, index=True)
    subregion = db.Column(db.Unicode(100), nullable=True)
    
    flag_emoji = db.Column(db.Unicode(32), nullable=True)
    flag_svg_url = db.Column(db.String(255), nullable=True)
    
    capital_name = db.Column(db.Unicode(150), nullable=True)
    largest_city = db.Column(db.Unicode(150), nullable=True)
    
    area_km2 = db.Column(db.Float, nullable=True)
    area_sq_mi = db.Column(db.Float, nullable=True)
    land_area_km2 = db.Column(db.Float, nullable=True)
    water_area_km2 = db.Column(db.Float, nullable=True)
    
    population = db.Column(db.BigInteger, nullable=True)
    population_year = db.Column(db.Integer, default=2024)
    population_density = db.Column(db.Float, nullable=True)
    urban_population_pct = db.Column(db.Float, nullable=True)
    
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    highest_point = db.Column(db.Unicode(120), nullable=True)
    highest_elevation_m = db.Column(db.Integer, nullable=True)
    lowest_point = db.Column(db.Unicode(120), nullable=True)
    lowest_elevation_m = db.Column(db.Integer, nullable=True)
    coastline_km = db.Column(db.Float, nullable=True)
    is_landlocked = db.Column(db.Boolean, default=False)
    
    currency_code = db.Column(db.String(10), nullable=True)
    currency_name = db.Column(db.Unicode(100), nullable=True)
    currency_symbol = db.Column(db.Unicode(32), nullable=True)
    
    official_languages = db.Column(db.String(255), nullable=True)
    widely_spoken_languages = db.Column(db.String(255), nullable=True)
    demonym = db.Column(db.String(80), nullable=True)
    
    calling_code = db.Column(db.String(20), nullable=True)
    tld = db.Column(db.String(10), nullable=True)
    time_zones = db.Column(db.String(150), nullable=True)
    driving_side = db.Column(db.String(10), default="right")
    
    government_system = db.Column(db.String(150), nullable=True)
    head_of_state = db.Column(db.String(150), nullable=True)
    head_of_government = db.Column(db.String(150), nullable=True)
    independence_date = db.Column(db.String(100), nullable=True)
    
    gdp_usd_billions = db.Column(db.Float, nullable=True)
    gdp_per_capita_usd = db.Column(db.Float, nullable=True)
    gdp_reference_year = db.Column(db.Integer, default=2024)
    major_industries = db.Column(db.Text, nullable=True)
    natural_resources = db.Column(db.Text, nullable=True)
    climate = db.Column(db.Text, nullable=True)
    
    overview = db.Column(db.Text, nullable=True)
    data_source = db.Column(db.String(100), default="Natural Earth / World Bank / UN")
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    alt_names = db.relationship("CountryName", backref="country", cascade="all, delete-orphan", lazy="dynamic")
    capitals = db.relationship("Capital", backref="country", cascade="all, delete-orphan", lazy="dynamic")
    divisions = db.relationship("AdministrativeDivision", backref="country", cascade="all, delete-orphan", lazy="dynamic")
    cities = db.relationship("City", backref="country", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f"<Country {self.common_name} ({self.iso_a2})>"

class CountryName(db.Model):
    __tablename__ = "country_names"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True)
    language_code = db.Column(db.String(10), default="en")
    name_type = db.Column(db.String(30), default="alt") # common, official, native, alt
    name_value = db.Column(db.String(200), nullable=False, index=True)

class Capital(db.Model):
    __tablename__ = "capitals"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    capital_type = db.Column(db.String(50), default="primary") # primary, administrative, legislative, judicial
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    elevation_m = db.Column(db.Integer, nullable=True)
    population = db.Column(db.BigInteger, nullable=True)

class Border(db.Model):
    __tablename__ = "borders"

    id = db.Column(db.Integer, primary_key=True)
    country_a_iso = db.Column(db.String(3), nullable=False, index=True)
    country_b_iso = db.Column(db.String(3), nullable=False, index=True)
    border_type = db.Column(db.String(30), default="land") # land, maritime, strait
    length_km = db.Column(db.Float, nullable=True)

    __table_args__ = (
        db.UniqueConstraint("country_a_iso", "country_b_iso", "border_type", name="uq_border_pair"),
    )

class AdministrativeDivision(db.Model):
    __tablename__ = "administrative_divisions"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_division_id = db.Column(db.Integer, db.ForeignKey("administrative_divisions.id", ondelete="NO ACTION"), nullable=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    slug = db.Column(db.String(180), nullable=False, index=True)
    code = db.Column(db.String(30), nullable=True) # e.g. IN-MH, US-CA
    division_type = db.Column(db.String(60), nullable=False) # State, Union Territory, Province, District, County
    capital_or_center = db.Column(db.String(100), nullable=True)
    area_km2 = db.Column(db.Float, nullable=True)
    population = db.Column(db.BigInteger, nullable=True)
    population_year = db.Column(db.Integer, default=2024)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    subdivisions = db.relationship("AdministrativeDivision", backref=db.backref("parent", remote_side=[id]))
    cities = db.relationship("City", backref="division", lazy="dynamic")

    def __repr__(self):
        return f"<AdministrativeDivision {self.name} ({self.division_type})>"

class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True)
    division_id = db.Column(db.Integer, db.ForeignKey("administrative_divisions.id", ondelete="NO ACTION"), nullable=True, index=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    slug = db.Column(db.String(150), nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    population = db.Column(db.BigInteger, nullable=True)
    elevation_m = db.Column(db.Integer, nullable=True)
    is_capital = db.Column(db.Boolean, default=False)
    is_major_port = db.Column(db.Boolean, default=False)
    airport_code = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"<City {self.name}>"
