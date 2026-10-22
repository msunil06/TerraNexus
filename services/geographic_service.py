from models import db
from models.geography import Continent, Country, Capital, Border, AdministrativeDivision, City, CountryName
from models.marine_and_physical import Ocean, Sea, GeographicFeature, DataSource

class GeographicService:
    @staticmethod
    def get_global_statistics():
        """Compute real, verified global statistics from the database."""
        countries_count = Country.query.count()
        continents_count = Continent.query.count()
        oceans_count = Ocean.query.count()
        seas_count = Sea.query.count()
        features_count = GeographicFeature.query.count()
        divisions_count = AdministrativeDivision.query.count()
        cities_count = City.query.count()

        return {
            "countries_count": countries_count,
            "continents_count": continents_count,
            "oceans_count": oceans_count,
            "seas_count": seas_count,
            "features_count": features_count,
            "divisions_count": divisions_count,
            "cities_count": cities_count,
            "classification_notes": "Countries count covers sovereign states and territories cataloged per ISO 3166-1 standards."
        }

    @staticmethod
    def get_all_countries(continent_slug=None, search_query=None, sort_by="name"):
        query = Country.query
        if continent_slug:
            continent = Continent.query.filter_by(slug=continent_slug).first()
            if continent:
                query = query.filter_by(continent_id=continent.id)
        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(
                (Country.common_name.ilike(term)) |
                (Country.official_name.ilike(term)) |
                (Country.capital_name.ilike(term)) |
                (Country.iso_a2.ilike(term)) |
                (Country.iso_a3.ilike(term))
            )
        if sort_by == "population":
            query = query.order_by(Country.population.desc())
        elif sort_by == "area":
            query = query.order_by(Country.area_km2.desc())
        else:
            query = query.order_by(Country.common_name.asc())
        return query.all()

    @staticmethod
    def get_country_by_slug(slug):
        return Country.query.filter((Country.slug == slug) | (Country.iso_a3 == slug.upper()) | (Country.iso_a2 == slug.upper())).first()

    @staticmethod
    def get_country_neighbors(country):
        """Retrieve verified land and maritime neighbors using border dataset."""
        borders = Border.query.filter(
            (Border.country_a_iso == country.iso_a3) | (Border.country_b_iso == country.iso_a3)
        ).all()
        
        neighbor_list = []
        for b in borders:
            neighbor_iso = b.country_b_iso if b.country_a_iso == country.iso_a3 else b.country_a_iso
            neighbor_country = Country.query.filter_by(iso_a3=neighbor_iso).first()
            if neighbor_country:
                neighbor_list.append({
                    "country": neighbor_country,
                    "border_type": b.border_type,
                    "length_km": b.length_km
                })
        return neighbor_list

    @staticmethod
    def get_country_divisions(country):
        # Return top-level divisions (where parent_division_id is null)
        return AdministrativeDivision.query.filter_by(country_id=country.id, parent_division_id=None).order_by(AdministrativeDivision.name.asc()).all()

    @staticmethod
    def get_division_by_slug(country_slug, division_slug):
        country = GeographicService.get_country_by_slug(country_slug)
        if not country:
            return None, None
        division = AdministrativeDivision.query.filter_by(country_id=country.id, slug=division_slug).first()
        return country, division

    @staticmethod
    def get_all_continents():
        return Continent.query.order_by(Continent.area_km2.desc()).all()

    @staticmethod
    def get_continent_by_slug(slug):
        return Continent.query.filter_by(slug=slug).first()

    @staticmethod
    def get_all_oceans():
        return Ocean.query.order_by(Ocean.area_km2.desc()).all()

    @staticmethod
    def get_ocean_by_slug(slug):
        return Ocean.query.filter_by(slug=slug).first()

    @staticmethod
    def get_all_seas(ocean_slug=None):
        query = Sea.query
        if ocean_slug:
            ocean = Ocean.query.filter_by(slug=ocean_slug).first()
            if ocean:
                query = query.filter_by(ocean_id=ocean.id)
        return query.order_by(Sea.name.asc()).all()

    @staticmethod
    def get_sea_by_slug(slug):
        return Sea.query.filter_by(slug=slug).first()

    @staticmethod
    def get_all_features(feature_type=None):
        query = GeographicFeature.query
        if feature_type:
            query = query.filter_by(feature_type=feature_type)
        return query.order_by(GeographicFeature.name.asc()).all()

    @staticmethod
    def get_feature_by_slug(slug):
        return GeographicFeature.query.filter_by(slug=slug).first()

    @staticmethod
    def get_all_data_sources():
        return DataSource.query.order_by(DataSource.name.asc()).all()
