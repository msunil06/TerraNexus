from models.geography import Country, AdministrativeDivision, City, Continent
from models.marine_and_physical import Ocean, Sea, GeographicFeature

class SearchService:
    @staticmethod
    def global_search(query_str, limit=20):
        if not query_str or len(query_str.strip()) < 1:
            return []

        q = query_str.strip()
        term = f"%{q}%"
        results = []

        # 1. Countries
        countries = Country.query.filter(
            (Country.common_name.ilike(term)) |
            (Country.official_name.ilike(term)) |
            (Country.iso_a2.ilike(q)) |
            (Country.iso_a3.ilike(q)) |
            (Country.capital_name.ilike(term))
        ).limit(limit).all()

        for c in countries:
            results.append({
                "type": "Country",
                "title": c.common_name,
                "subtitle": f"Capital: {c.capital_name or 'N/A'} • {c.subregion or ''}",
                "flag": c.flag_emoji or "🌐",
                "url": f"/countries/{c.slug}",
                "lat": c.latitude,
                "lon": c.longitude,
                "badge": "Country"
            })

        # 2. Administrative Divisions (e.g., California, Maharashtra)
        divisions = AdministrativeDivision.query.filter(
            (AdministrativeDivision.name.ilike(term)) |
            (AdministrativeDivision.code.ilike(term))
        ).limit(limit).all()

        for d in divisions:
            parent_country = d.country.common_name if d.country else "Global"
            results.append({
                "type": "Division",
                "title": d.name,
                "subtitle": f"{d.division_type} in {parent_country}",
                "flag": d.country.flag_emoji if d.country else "📍",
                "url": f"/countries/{d.country.slug}/divisions/{d.slug}" if d.country else "#",
                "lat": d.latitude,
                "lon": d.longitude,
                "badge": d.division_type
            })

        # 3. Oceans
        oceans = Ocean.query.filter(Ocean.name.ilike(term)).limit(limit).all()
        for o in oceans:
            results.append({
                "type": "Ocean",
                "title": o.name,
                "subtitle": f"Area: {o.area_km2:,} km² • Max Depth: {o.max_depth_m:,} m",
                "flag": "🌊",
                "url": f"/oceans/{o.slug}",
                "lat": 0.0,
                "lon": 160.0 if "pacific" in o.slug else (0.0 if "atlantic" in o.slug else 80.0),
                "badge": "Ocean"
            })

        # 4. Seas
        seas = Sea.query.filter(
            (Sea.name.ilike(term)) |
            (Sea.alternative_names.ilike(term))
        ).limit(limit).all()

        for s in seas:
            results.append({
                "type": "Sea",
                "title": s.name,
                "subtitle": f"{s.sea_type.capitalize()} Sea • {s.surrounding_countries or ''}"[:80],
                "flag": "⛵",
                "url": f"/seas/{s.slug}",
                "lat": s.latitude,
                "lon": s.longitude,
                "badge": "Sea"
            })

        # 5. Continents
        continents = Continent.query.filter(Continent.name.ilike(term)).limit(limit).all()
        for cont in continents:
            results.append({
                "type": "Continent",
                "title": cont.name,
                "subtitle": f"{cont.countries_count} Countries • {cont.area_km2:,} km²",
                "flag": "🌍",
                "url": f"/continents/{cont.slug}",
                "lat": None,
                "lon": None,
                "badge": "Continent"
            })

        # 6. Physical Geographic Features (Mountains, Rivers, Deserts, etc.)
        features = GeographicFeature.query.filter(
            (GeographicFeature.name.ilike(term)) |
            (GeographicFeature.alternative_names.ilike(term)) |
            (GeographicFeature.feature_type.ilike(term))
        ).limit(limit).all()

        for f in features:
            f_type_label = f.feature_type.replace("_", " ").title()
            results.append({
                "type": "Feature",
                "title": f.name,
                "subtitle": f"{f_type_label} • {f.countries_involved or ''}"[:75],
                "flag": "🏔️" if "mountain" in f.feature_type else ("🌊" if "river" in f.feature_type or "strait" in f.feature_type else "🏜️"),
                "url": f"/features/{f.slug}",
                "lat": f.latitude,
                "lon": f.longitude,
                "badge": f_type_label
            })

        return results[:limit]
