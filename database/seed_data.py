"""
TerraNexus Authoritative Seed Data
Datasets sourced from:
- Natural Earth (Public Domain / CC0)
- GeoNames (CC BY 4.0)
- United Nations Statistics Division (UNSD)
- World Bank Open Data (CC BY 4.0)
- International Hydrographic Organization (IHO S-23)
- NOAA NCEI Bathymetric & Marine Data
"""

import os
import sys
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import db
from models.user import Role, Permission, User, UserRole, SystemSetting
from models.geography import Continent, Country, Capital, Border, AdministrativeDivision, City, CountryName
from models.marine_and_physical import Ocean, Sea, GeographicFeature, DataSource

def seed_roles_and_permissions(app):
    with app.app_context():
        roles_data = [
            ("Guest", "Can browse public geographic information and use public search"),
            ("Registered User", "Can browse public info, manage profile, save favorites and collections"),
            ("Moderator", "Can review reports and perform authorized moderation tasks"),
            ("Administrator", "Can manage users, content, geographic information and settings"),
            ("Super Administrator", "Full control over system, privileged administrative roles and settings")
        ]
        
        for name, desc in roles_data:
            existing = Role.query.filter_by(name=name).first()
            if not existing:
                db.session.add(Role(name=name, description=desc))
        
        db.session.commit()

        # Seed initial admin user if not exists
        super_role = Role.query.filter_by(name="Super Administrator").first()
        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@terranexus.internal",
                display_name="TerraNexus Admin",
                preferred_language="en",
                theme_preference="dark"
            )
            admin_user.set_password("Admin@TerraNexus2026!")
            db.session.add(admin_user)
            db.session.flush()

            db.session.add(UserRole(user_id=admin_user.id, role_id=super_role.id))

        # Seed sample registered explorer
        reg_role = Role.query.filter_by(name="Registered User").first()
        demo_user = User.query.filter_by(username="explorer").first()
        if not demo_user:
            demo_user = User(
                username="explorer",
                email="explorer@terranexus.internal",
                display_name="Global Explorer",
                preferred_language="en",
                theme_preference="dark"
            )
            demo_user.set_password("Explorer@2026!")
            db.session.add(demo_user)
            db.session.flush()

            db.session.add(UserRole(user_id=demo_user.id, role_id=reg_role.id))

        # Seed system settings
        default_settings = [
            ("site_name", "TerraNexus", "Platform primary brand name"),
            ("maintenance_mode", "false", "Whether site is in maintenance mode"),
            ("default_map_style", "dark", "Default base map layer style"),
            ("allow_registration", "true", "Whether new user signups are enabled")
        ]
        for key, val, desc in default_settings:
            if not SystemSetting.query.filter_by(key=key).first():
                db.session.add(SystemSetting(key=key, value=val, description=desc))

        db.session.commit()

def seed_continents(app):
    with app.app_context():
        continents_data = [
            {
                "name": "Asia", "slug": "asia", "code": "AS",
                "area_km2": 44579000, "population": 4750000000, "countries_count": 49,
                "overview": "Asia is Earth's largest and most populous continent, located primarily in the Eastern and Northern Hemispheres. It covers 30% of Earth's total land area and hosts roughly 60% of the world's human population.",
                "climate_zones": "Arctic tundra, subarctic taiga, temperate, arid desert, subtropical, tropical monsoon",
                "highest_point": "Mount Everest (8,848 m)", "lowest_point": "Dead Sea (-430 m)"
            },
            {
                "name": "Africa", "slug": "africa", "code": "AF",
                "area_km2": 30370000, "population": 1460000000, "countries_count": 54,
                "overview": "Africa is the world's second-largest and second-most populous continent. Straddling the equator and encompassing numerous climate zones, it is the only continent to stretch from the northern temperate to southern temperate zones.",
                "climate_zones": "Mediterranean, hyper-arid Sahara, Sahel semi-arid, tropical savanna, equatorial rainforest",
                "highest_point": "Mount Kilimanjaro (5,895 m)", "lowest_point": "Lake Assal (-155 m)"
            },
            {
                "name": "Europe", "slug": "europe", "code": "EU",
                "area_km2": 10180000, "population": 745000000, "countries_count": 44,
                "overview": "Europe is situated in the Northern Hemisphere and mostly in the Eastern Hemisphere. Bordered by the Arctic Ocean to the north, Atlantic Ocean to the west, and Mediterranean Sea to the south.",
                "climate_zones": "Subarctic, oceanic, continental, Mediterranean, alpine",
                "highest_point": "Mount Elbrus (5,642 m)", "lowest_point": "Caspian Sea shore (-28 m)"
            },
            {
                "name": "North America", "slug": "north-america", "code": "NA",
                "area_km2": 24709000, "population": 600000000, "countries_count": 23,
                "overview": "North America extends from the Arctic circle down through Central America and the Caribbean basin, bounded by the Pacific Ocean on the west and the Atlantic Ocean on the east.",
                "climate_zones": "Polar, subarctic, continental, oceanic, Mediterranean, desert, tropical wet-and-dry",
                "highest_point": "Denali (6,190 m)", "lowest_point": "Death Valley (-86 m)"
            },
            {
                "name": "South America", "slug": "south-america", "code": "SA",
                "area_km2": 17840000, "population": 435000000, "countries_count": 12,
                "overview": "South America is situated predominantly in the Southern Hemisphere, home to the Amazon Basin, the world's greatest river system by discharge, and the immense Andes Mountain chain.",
                "climate_zones": "Equatorial rainforest, tropical savanna, arid desert, Mediterranean, alpine, subpolar oceanic",
                "highest_point": "Aconcagua (6,961 m)", "lowest_point": "Laguna del Carbón (-105 m)"
            },
            {
                "name": "Antarctica", "slug": "antarctica", "code": "AN",
                "area_km2": 14200000, "population": 4000, "countries_count": 0,
                "overview": "Antarctica is Earth's southernmost continent, containing the geographic South Pole. It is virtually covered in ice, representing 90% of the world's ice and 70% of its fresh water reserves.",
                "climate_zones": "Polar ice cap, polar tundra (Antarctic Peninsula)",
                "highest_point": "Vinson Massif (4,892 m)", "lowest_point": "Deep Lake, Vestfold Hills (-50 m)"
            },
            {
                "name": "Oceania", "slug": "oceania", "code": "OC",
                "area_km2": 8525989, "population": 45000000, "countries_count": 14,
                "overview": "Oceania is a geographic region spanning the Eastern and Western Hemispheres, comprising Australasia, Melanesia, Micronesia, and Polynesia.",
                "climate_zones": "Tropical rainforest, tropical monsoon, arid desert, semi-arid, temperate oceanic",
                "highest_point": "Puncak Jaya (4,884 m)", "lowest_point": "Lake Eyre (-15 m)"
            }
        ]

        for item in continents_data:
            existing = Continent.query.filter_by(slug=item["slug"]).first()
            if not existing:
                db.session.add(Continent(**item))
            else:
                for k, v in item.items():
                    setattr(existing, k, v)
        
        db.session.commit()

def seed_oceans(app):
    with app.app_context():
        oceans_data = [
            {
                "name": "Pacific Ocean",
                "slug": "pacific-ocean",
                "area_km2": 165250000,
                "volume_km3": 710000000,
                "avg_depth_m": 4280,
                "max_depth_m": 10994,
                "max_depth_location": "Challenger Deep, Mariana Trench",
                "surrounding_continents": "Asia, Australia, North America, South America, Antarctica",
                "major_marginal_seas": "South China Sea, Coral Sea, Bering Sea, Sea of Japan, Philippine Sea, East China Sea, Tasman Sea",
                "major_currents": "Kuroshio Current, California Current, North Equatorial Current, Humboldt (Peru) Current, Antarctic Circumpolar",
                "major_trenches": "Mariana Trench, Tonga Trench, Philippine Trench, Kuril–Kamchatka Trench",
                "major_ridges": "East Pacific Rise, Pacific-Antarctic Ridge",
                "overview": "The Pacific Ocean is the largest and deepest of Earth's oceanic divisions. Extending from the Arctic Ocean in the north to the Southern Ocean in the south, it encompasses about 46% of Earth's water surface and roughly 32% of its total surface area, larger than all Earth's land area combined.",
                "marine_biodiversity": "Home to the Great Barrier Reef, extensive coral triangles, hydrothermal vent communities, and vast pelagic migratory routes for whales, tuna, and sea turtles.",
                "economic_importance": "Critical global maritime shipping lanes connecting East Asia and the Americas; major fisheries providing over 60% of world marine harvest; offshore oil and gas.",
                "environmental_challenges": "Great Pacific Garbage Patch, ocean acidification affecting coral reefs, overfishing, deep-sea mining risks.",
                "historical_exploration": "Polynesian voyagers navigated vast expanses thousands of years ago; European navigation commenced with Vasco Núñez de Balboa (1513) and Ferdinand Magellan (1520-1521).",
                "data_source": "NOAA / IHO / GEBCO (2024)"
            },
            {
                "name": "Atlantic Ocean",
                "slug": "atlantic-ocean",
                "area_km2": 106460000,
                "volume_km3": 310410900,
                "avg_depth_m": 3646,
                "max_depth_m": 8376,
                "max_depth_location": "Milwaukee Deep, Puerto Rico Trench",
                "surrounding_continents": "North America, South America, Europe, Africa, Antarctica",
                "major_marginal_seas": "Caribbean Sea, Mediterranean Sea, Gulf of Mexico, North Sea, Baltic Sea, Norwegian Sea, Black Sea",
                "major_currents": "Gulf Stream, North Atlantic Drift, Canary Current, Brazil Current, Benguela Current",
                "major_trenches": "Puerto Rico Trench, South Sandwich Trench",
                "major_ridges": "Mid-Atlantic Ridge",
                "overview": "The Atlantic Ocean is the second-largest ocean, covering approximately 20% of Earth's surface. It connects the Old World and New World and drives the Atlantic Meridional Overturning Circulation (AMOC) regulating global climates.",
                "marine_biodiversity": "North Atlantic right whales, Sargasso Sea unique floating ecosystems, Caribbean coral reefs, and nutrient-rich cold-water upwelling zones.",
                "economic_importance": "Busiest oceanic transit routes, dense transatlantic telecommunications fiber networks, key offshore wind and hydrocarbon basins.",
                "environmental_challenges": "Weakening of the AMOC, plastic pollution, coastal runoff hypoxia, collapse of historical fisheries (such as Grand Banks cod).",
                "historical_exploration": "Viking voyages to Vinland (c. 1000 AD), Age of Discovery transits (Columbus 1492), early submarine cable layings (1858-1866).",
                "data_source": "NOAA / IHO / GEBCO (2024)"
            },
            {
                "name": "Indian Ocean",
                "slug": "indian-ocean",
                "area_km2": 70560000,
                "volume_km3": 264000000,
                "avg_depth_m": 3741,
                "max_depth_m": 7290,
                "max_depth_location": "Sunda (Java) Trench",
                "surrounding_continents": "Asia, Africa, Australia, Antarctica",
                "major_marginal_seas": "Arabian Sea, Bay of Bengal, Red Sea, Persian Gulf, Andaman Sea, Mozambique Channel",
                "major_currents": "Agulhas Current, Somali Current (reversing with monsoon), South Equatorial Current, West Australian Current",
                "major_trenches": "Java Trench, Diamantina Fracture Zone",
                "major_ridges": "Central Indian Ridge, Southwest Indian Ridge, Southeast Indian Ridge, Ninety East Ridge",
                "overview": "The Indian Ocean is the third-largest ocean, bounded by Asia to the north, Africa to the west, Australia to the east, and the Southern Ocean to the south. It is characterized by monsoon wind reversals and vital strategic choke points (Strait of Malacca, Bab-el-Mandeb, Strait of Hormuz).",
                "marine_biodiversity": "Extensive mangrove forests (Sundarbans), coral atolls in Maldives and Lakshadweep, dugongs, coelacanth living fossils off East Africa.",
                "economic_importance": "Handles around 40% of world offshore oil production and routes over 80% of global seaborne trade in oil through choke points.",
                "environmental_challenges": "Frequent cyclones, warming faster than other tropical oceans, sea-level rise threatening low-lying island nations (Maldives), coral bleaching.",
                "historical_exploration": "Austronesian sailors settled Madagascar (1st millennium CE); Monsoon navigation by Arab, Indian, Persian, and Chinese dhows; Vasco da Gama (1497-1498).",
                "data_source": "NOAA / IHO / GEBCO (2024)"
            },
            {
                "name": "Southern Ocean",
                "slug": "southern-ocean",
                "area_km2": 21960000,
                "volume_km3": 71800000,
                "avg_depth_m": 3270,
                "max_depth_m": 7434,
                "max_depth_location": "Factorian Deep, South Sandwich Trench",
                "surrounding_continents": "Antarctica",
                "major_marginal_seas": "Weddell Sea, Ross Sea, Amundsen Sea, Bellingshausen Sea, Davis Sea, Scotia Sea",
                "major_currents": "Antarctic Circumpolar Current (ACC) - largest ocean current by water volume",
                "major_trenches": "South Sandwich Trench",
                "major_ridges": "Pacific-Antarctic Ridge, Mid-Ocean Ridge spurs",
                "overview": "The Southern Ocean comprises the southernmost waters of the World Ocean, generally taken to be south of 60° S latitude and encircling Antarctica. It is defined by the Antarctic Circumpolar Current without northern continental barriers.",
                "marine_biodiversity": "Colossal Antarctic krill biomass forming the foundational keystone species for blue whales, orcas, leopard seals, and emperor penguins.",
                "economic_importance": "Scientific research, controlled krill and toothfish fisheries under CCAMLR, expedition tourism.",
                "environmental_challenges": "Rapid ice-shelf calving, Antarctic ozone hole impacts, warming circumpolar deep water destabilizing grounding lines.",
                "historical_exploration": "James Cook crossed Antarctic Circle (1773); Fabian Gottlieb von Bellingshausen (1820); Heroic Age of Antarctic Exploration (Amundsen, Scott, Shackleton).",
                "data_source": "NOAA / IHO / GEBCO (2024)"
            },
            {
                "name": "Arctic Ocean",
                "slug": "arctic-ocean",
                "area_km2": 14060000,
                "volume_km3": 18750000,
                "avg_depth_m": 1205,
                "max_depth_m": 5550,
                "max_depth_location": "Molloy Deep, Fram Strait",
                "surrounding_continents": "North America, Europe, Asia",
                "major_marginal_seas": "Barents Sea, Beaufort Sea, Chukchi Sea, East Siberian Sea, Kara Sea, Laptev Sea, Greenland Sea",
                "major_currents": "Beaufort Gyre, Transpolar Drift Stream, East Greenland Current",
                "major_trenches": "Litke Deep, Molloy Hole",
                "major_ridges": "Lomonosov Ridge, Gakkel Ridge",
                "overview": "The Arctic Ocean is the smallest and shallowest of the world's five major oceans. Recognized by some oceanographers as an estuary of the Atlantic, it is largely surrounded by Eurasia and North America and covered by sea ice year-round.",
                "marine_biodiversity": "Polar bears, ringed seals, narwhals, bowhead whales, belugas, and dense blooms of ice algae.",
                "economic_importance": "Opening Northern Sea Route and Northwest Passage maritime corridors, unexploited hydrocarbon reserves, commercial fisheries in Barents Sea.",
                "environmental_challenges": "Dramatic Arctic amplification of climate warming, rapid perennial multi-year sea ice loss, permafrost thaw release of methane.",
                "historical_exploration": "Centuries of Northwest Passage attempts (Franklin expedition 1845); Fridtjof Nansen's Fram drift (1893-1896); Roald Amundsen transit (1903-1906).",
                "data_source": "NOAA / IHO / GEBCO (2024)"
            }
        ]

        for item in oceans_data:
            existing = Ocean.query.filter_by(slug=item["slug"]).first()
            if not existing:
                db.session.add(Ocean(**item))
            else:
                for k, v in item.items():
                    setattr(existing, k, v)
        
        db.session.commit()

def seed_seas(app):
    with app.app_context():
        # Get ocean ids
        pacific = Ocean.query.filter_by(slug="pacific-ocean").first()
        atlantic = Ocean.query.filter_by(slug="atlantic-ocean").first()
        indian = Ocean.query.filter_by(slug="indian-ocean").first()
        southern = Ocean.query.filter_by(slug="southern-ocean").first()
        arctic = Ocean.query.filter_by(slug="arctic-ocean").first()

        seas_data = [
            {
                "name": "Arabian Sea",
                "slug": "arabian-sea",
                "alternative_names": "Sindhu Sagar, Bahr al-Arab",
                "ocean_id": indian.id if indian else None,
                "sea_type": "marginal",
                "area_km2": 3862000,
                "avg_depth_m": 2734,
                "max_depth_m": 4652,
                "latitude": 15.0, "longitude": 65.0,
                "surrounding_countries": "India, Pakistan, Oman, Yemen, Iran, United Arab Emirates, Maldives, Somalia",
                "connected_water_bodies": "Gulf of Oman, Persian Gulf (via Strait of Hormuz), Gulf of Aden, Red Sea (via Bab-el-Mandeb), Indian Ocean",
                "major_ports": "Mumbai (JNPT), Karachi, Gwadar, Salalah, Muscat, Kochi, Mormugao, Kandla",
                "major_currents": "West Indian Coastal Current, Somali Current (seasonally reversing)",
                "marine_life": "Dolphins, whale sharks, Arabian humpback whales, yellowfin tuna, extensive oxygen minimum zones (OMZ)",
                "economic_importance": "Critical energy transport route carrying crude petroleum from Gulf producers to Asia and Europe; lucrative commercial fisheries",
                "environmental_concerns": "Expanding thick oceanic oxygen minimum zone, maritime chemical discharge, maritime security and piracy corridors",
                "historical_significance": "Crucial trading basin since antiquity linking the Indus Valley Civilization, Mesopotamia, Roman Empire, Egypt, and Gujarat coast.",
                "overview": "The Arabian Sea is a northern region of the Indian Ocean bounded on the north by Pakistan and Iran, on the west by the Arabian Peninsula, on the east by India, and on the south by the open ocean. It has been a central crossroads of international maritime commerce for thousands of years."
            },
            {
                "name": "Mediterranean Sea",
                "slug": "mediterranean-sea",
                "alternative_names": "Mare Nostrum, White Sea (Akdeniz)",
                "ocean_id": atlantic.id if atlantic else None,
                "sea_type": "mediterranean",
                "area_km2": 2500000,
                "avg_depth_m": 1500,
                "max_depth_m": 5267,
                "latitude": 35.0, "longitude": 18.0,
                "surrounding_countries": "Spain, France, Monaco, Italy, Slovenia, Croatia, Bosnia and Herzegovina, Montenegro, Albania, Greece, Turkey, Syria, Lebanon, Israel, Palestine, Egypt, Libya, Tunisia, Algeria, Morocco, Malta, Cyprus",
                "connected_water_bodies": "Atlantic Ocean (Strait of Gibraltar), Sea of Marmara & Black Sea (Dardanelles/Bosporus), Red Sea (Suez Canal)",
                "major_ports": "Valencia, Barcelona, Marseille, Genoa, Piraeus, Alexandria, Port Said, Tangier Med",
                "major_currents": "North Atlantic Inflow Surface Current, Levantine Intermediate Water (LIW)",
                "marine_life": "Mediterranean monk seals, loggerhead sea turtles, bluefin tuna, Posidonia oceanica seagrass meadows",
                "economic_importance": "Key global shipping junction via Suez Canal, immense Mediterranean tourism economy, submarine communications hub",
                "environmental_concerns": "High microplastic accumulation, invasive species migration through Suez (Lessepsian migration), intensive coastal overdevelopment",
                "historical_significance": "Cradle of Western and Middle Eastern civilizations, including ancient Phoenicia, Greece, Carthage, Rome, Byzantine, and Islamic caliphates.",
                "overview": "The Mediterranean Sea is almost completely enclosed by land: on the north by Southern Europe and Anatolia, on the south by North Africa, and on the east by the Levant. It connects to the Atlantic Ocean through the narrow Strait of Gibraltar."
            },
            {
                "name": "South China Sea",
                "slug": "south-china-sea",
                "alternative_names": "East Sea (Vietnam), West Philippine Sea (Philippines)",
                "ocean_id": pacific.id if pacific else None,
                "sea_type": "marginal",
                "area_km2": 3500000,
                "avg_depth_m": 1212,
                "max_depth_m": 5559,
                "latitude": 12.0, "longitude": 114.0,
                "surrounding_countries": "China, Taiwan, Philippines, Malaysia, Brunei, Indonesia, Singapore, Vietnam",
                "connected_water_bodies": "East China Sea (Taiwan Strait), Philippine Sea (Luzon Strait), Java Sea (Karimata Strait), Indian Ocean (Strait of Malacca)",
                "major_ports": "Singapore, Shanghai-linked routes, Hong Kong, Shenzhen, Manila, Ho Chi Minh City, Port Klang",
                "major_currents": "South China Sea Warm Current, seasonal winter cyclonic gyre",
                "marine_life": "Diverse coral reefs across Paracel and Spratly archipelagos, dugongs, green sea turtles, immense pelagic fisheries",
                "economic_importance": "One-third of all global maritime shipping traverses this sea ($3.4 trillion in annual trade); vast undersea oil and gas reserves",
                "environmental_concerns": "Coral reef destruction from artificial island building, intense overfishing, territorial boundary disputes",
                "historical_significance": "Maritime Silk Road artery connecting imperial China with Southeast Asia, India, Arabia, and Europe for two millennia.",
                "overview": "The South China Sea is a marginal sea of the Western Pacific Ocean, bounded by Southeast and East Asian nations. It is of enormous geopolitical and economic significance, encompassing vital global shipping lanes and rich natural resources."
            },
            {
                "name": "Caribbean Sea",
                "slug": "caribbean-sea",
                "alternative_names": "Mar Caribe",
                "ocean_id": atlantic.id if atlantic else None,
                "sea_type": "marginal",
                "area_km2": 2754000,
                "avg_depth_m": 2200,
                "max_depth_m": 7686,
                "latitude": 15.0, "longitude": -75.0,
                "surrounding_countries": "Cuba, Jamaica, Haiti, Dominican Republic, Puerto Rico, Mexico, Belize, Guatemala, Honduras, Nicaragua, Costa Rica, Panama, Colombia, Venezuela, Trinidad and Tobago",
                "connected_water_bodies": "Gulf of Mexico (Yucatan Channel), Atlantic Ocean, Pacific Ocean (via Panama Canal)",
                "major_ports": "Colon, Kingston, Cartagena, San Juan, Havana, Santo Domingo",
                "major_currents": "Caribbean Current, Antillean Current",
                "marine_life": "Mesoamerican Barrier Reef (second largest worldwide), West Indian manatee, queen conch, spiny lobster",
                "economic_importance": "Major cruise and leisure tourism, maritime transit between Atlantic and Pacific oceans via the Panama Canal, petroleum refinery hubs",
                "environmental_concerns": "Frequent severe tropical hurricanes, stony coral tissue loss disease (SCTLD), sargassum weed inundation",
                "historical_significance": "First landing point of Christopher Columbus in 1492; Spanish treasure fleets; Golden Age of Piracy (17th-18th centuries).",
                "overview": "The Caribbean Sea is an American Mediterranean sea in the tropical Western Hemisphere, bounded by Central America to the west and southwest, the Greater Antilles to the north, and the Lesser Antilles to the east."
            },
            {
                "name": "Red Sea",
                "slug": "red-sea",
                "alternative_names": "Bahr al-Qulzum, Erythraean Sea",
                "ocean_id": indian.id if indian else None,
                "sea_type": "inland",
                "area_km2": 438000,
                "avg_depth_m": 490,
                "max_depth_m": 3040,
                "latitude": 22.0, "longitude": 38.0,
                "surrounding_countries": "Egypt, Sudan, Eritrea, Djibouti, Saudi Arabia, Yemen, Jordan, Israel",
                "connected_water_bodies": "Mediterranean Sea (via Suez Canal), Gulf of Aden and Arabian Sea (via Bab-el-Mandeb), Gulf of Aqaba, Gulf of Suez",
                "major_ports": "Jeddah, Port Sudan, Djibouti, Suez, Aqaba, Eilat, Yanbu",
                "major_currents": "Surface inflow from Gulf of Aden, deep saline outflow",
                "marine_life": "World's most heat-resilient coral reefs, 1,200+ fish species with 10% endemism, manta rays, hammerhead sharks",
                "economic_importance": "Crucial maritime trade corridor through the Suez Canal handling ~12% of total global cargo trade",
                "environmental_concerns": "Threats from abandoned tankers (such as FSO Safer), military conflict impacts on merchant shipping, desalination brine effluent",
                "historical_significance": "Biblical crossing narratives; ancient Egyptian and Roman trade routes to Punt and India; opening of Suez Canal in 1869.",
                "overview": "The Red Sea is a narrow seawater inlet of the Indian Ocean lying between Africa and the Arabian Peninsula. It occupies part of the Great Rift Valley system and features some of the warmest and saltiest marine waters on Earth."
            },
            {
                "name": "Black Sea",
                "slug": "black-sea",
                "alternative_names": "Euxine Sea, Karadeniz",
                "ocean_id": atlantic.id if atlantic else None,
                "sea_type": "inland",
                "area_km2": 436402,
                "avg_depth_m": 1253,
                "max_depth_m": 2212,
                "latitude": 44.0, "longitude": 35.0,
                "surrounding_countries": "Turkey, Bulgaria, Romania, Ukraine, Russia, Georgia",
                "connected_water_bodies": "Sea of Azov (via Kerch Strait), Sea of Marmara (via Bosporus), Aegean and Mediterranean Seas",
                "major_ports": "Istanbul, Constanța, Odesa, Novorossiysk, Batumi, Varna, Sevastopol",
                "major_currents": "Rim Current (anti-clockwise basin cyclonic loop)",
                "marine_life": "Black Sea harbor porpoise, sturgeon species, unique anoxic microbial communities below 150-200 meters",
                "economic_importance": "Major export corridor for grain, oil, and mineral fertilizers from Eastern Europe and Central Asia",
                "environmental_concerns": "Largest meromictic water body (90% volume is anoxic with hydrogen sulfide), eutrophication from Danube runoff",
                "historical_significance": "Ancient Greek colonization (Pontus Euxinus); Silk Road terminus; Genoese and Byzantine trade; Crimean War.",
                "overview": "The Black Sea is an inland marginal sea located between Eastern Europe, the Caucasus, and Western Asia. It is famous for its stratified structure, with oxygenated surface waters resting on an immense reservoir of anoxic, hydrogen sulfide-rich deep water."
            },
            {
                "name": "Baltic Sea",
                "slug": "baltic-sea",
                "alternative_names": "Ostsee, Läänemeri, Östersjön",
                "ocean_id": atlantic.id if atlantic else None,
                "sea_type": "marginal",
                "area_km2": 377000,
                "avg_depth_m": 55,
                "max_depth_m": 459,
                "latitude": 58.0, "longitude": 20.0,
                "surrounding_countries": "Sweden, Finland, Russia, Estonia, Latvia, Lithuania, Poland, Germany, Denmark",
                "connected_water_bodies": "North Sea (via Danish Straits: Kattegat, Skagerrak, Great Belt, Øresund)",
                "major_ports": "Saint Petersburg, Stockholm, Helsinki, Copenhagen, Gdansk, Klaipeda, Tallinn, Rostock",
                "major_currents": "Brackish surface outflow, saline bottom inflow through Danish Straits",
                "marine_life": "Baltic grey seal, ringed seal, Baltic cod, Atlantic herring adapted to brackish water",
                "economic_importance": "High-density European ferry, cargo, and energy transmission networks; major offshore wind energy parks",
                "environmental_concerns": "Severe agricultural runoff eutrophication causing recurring summer algal blooms; historic dumped chemical munitions",
                "historical_significance": "Dominion of the Hanseatic League in the Middle Ages; Northern Crusades; Swedish Empire period (Dominium maris baltici).",
                "overview": "The Baltic Sea is a semi-enclosed arm of the Atlantic Ocean in Northern Europe. It is the largest body of brackish water in the world, with low salinity due to abundant freshwater river inflow and limited oceanic exchange."
            },
            {
                "name": "North Sea",
                "slug": "north-sea",
                "alternative_names": "Mer du Nord, Noordzee, Nordsee",
                "ocean_id": atlantic.id if atlantic else None,
                "sea_type": "marginal",
                "area_km2": 570000,
                "avg_depth_m": 95,
                "max_depth_m": 700,
                "latitude": 56.0, "longitude": 3.0,
                "surrounding_countries": "United Kingdom, Norway, Denmark, Germany, Netherlands, Belgium, France",
                "connected_water_bodies": "Atlantic Ocean, Norwegian Sea, English Channel (Strait of Dover), Baltic Sea (via Skagerrak)",
                "major_ports": "Rotterdam, Antwerp, Hamburg, Bremerhaven, London, Felixstowe, Bergen",
                "major_currents": "North Atlantic inflow, Norwegian Coastal Current",
                "marine_life": "Atlantic cod, haddock, mackerel, harbour porpoises, grey seals, minke whales",
                "economic_importance": "Massive offshore wind farm installations (Dogger Bank), historic Brent crude oil and gas production, major global ports",
                "environmental_concerns": "Intensive seabed trawling damage, decommissioning of offshore drilling platforms, heavy commercial shipping emissions",
                "historical_significance": "Viking migrations; British naval supremacy; Battle of Jutland (1916); European maritime merchant networks.",
                "overview": "The North Sea is a marginal sea of the Atlantic Ocean located on the European continental shelf, connecting to the ocean through the English Channel in the south and the Norwegian Sea in the north."
            },
            {
                "name": "Coral Sea",
                "slug": "coral-sea",
                "alternative_names": "Mer de Corail",
                "ocean_id": pacific.id if pacific else None,
                "sea_type": "marginal",
                "area_km2": 4791000,
                "avg_depth_m": 2400,
                "max_depth_m": 9140,
                "latitude": -18.0, "longitude": 152.0,
                "surrounding_countries": "Australia, Papua New Guinea, Solomon Islands, Vanuatu, New Caledonia (France)",
                "connected_water_bodies": "Pacific Ocean, Tasman Sea, Solomon Sea, Arafura Sea (via Torres Strait)",
                "major_ports": "Cairns, Townsville, Port Moresby, Nouméa",
                "major_currents": "East Australian Current (EAC)",
                "marine_life": "Great Barrier Reef (2,900+ individual reefs, 900+ islands), dwarf minke whales, green and hawksbill turtles",
                "economic_importance": "World heritage eco-tourism, Coral Sea Marine Park (one of the world's largest marine protected areas)",
                "environmental_concerns": "Repeated mass coral bleaching events driven by elevated sea surface temperatures, crown-of-thorns starfish outbreaks",
                "historical_significance": "Battle of the Coral Sea (May 1942), the first naval aircraft carrier battle in history preventing invasion of Port Moresby.",
                "overview": "The Coral Sea is a marginal sea of the South Pacific off the northeast coast of Australia. It contains the Great Barrier Reef, the world's largest coral reef system and a UNESCO World Heritage site."
            },
            {
                "name": "Bering Sea",
                "slug": "bering-sea",
                "alternative_names": "Imarpik",
                "ocean_id": pacific.id if pacific else None,
                "sea_type": "marginal",
                "area_km2": 2000000,
                "avg_depth_m": 1600,
                "max_depth_m": 4151,
                "latitude": 58.0, "longitude": -175.0,
                "surrounding_countries": "United States (Alaska), Russia (Siberia)",
                "connected_water_bodies": "Arctic Ocean (via Bering Strait), Pacific Ocean (via Aleutian passes), Chukchi Sea",
                "major_ports": "Dutch Harbor (Unalaska), Nome, Petropavlovsk-Kamchatsky, Provideniya",
                "major_currents": "Bering Slope Current, Anadyr Current",
                "marine_life": "Alaska pollock (world's largest food fishery), king crab, walruses, bowhead whales, sea otters, millions of seabirds",
                "economic_importance": "Supplies roughly half of the commercial fish and shellfish catch in the United States; gateway to Arctic sea routes",
                "environmental_concerns": "Disappearing winter sea ice extent, northward shift of subarctic and arctic fish distributions, coastal permafrost erosion",
                "historical_significance": "Bering Land Bridge (Beringia) allowed first human migrations into the Americas; explored by Vitus Bering (1728, 1741).",
                "overview": "The Bering Sea is a marginal sea of the Pacific Ocean separating Asia from North America. Comprising a deep basin in the southwest and an expansive shallow continental shelf in the northeast, it is one of the world's most productive marine ecosystems."
            },
            {
                "name": "Caspian Sea",
                "slug": "caspian-sea",
                "alternative_names": "Khazar Sea, Mazandaran Sea, Kaspiy",
                "ocean_id": None, # Endorheic basin / inland sea
                "sea_type": "inland",
                "area_km2": 371000,
                "avg_depth_m": 211,
                "max_depth_m": 1025,
                "latitude": 42.0, "longitude": 50.0,
                "surrounding_countries": "Azerbaijan, Iran, Kazakhstan, Russia, Turkmenistan",
                "connected_water_bodies": "Endorheic lake/sea (fed by Volga, Ural, and Kura rivers; connected to Black & Baltic Seas via Russian canal systems)",
                "major_ports": "Baku, Aktau, Turkmenbashi, Anzali, Astrakhan",
                "major_currents": "Cyclonic surface circulation fed by northern Volga inflow",
                "marine_life": "Caspian seal (endemic), wild Beluga sturgeon (producer of world-renowned caviar), Caspian salmon",
                "economic_importance": "Vast offshore petroleum and natural gas fields (Kashagan, Shah Deniz, Tengiz), Trans-Caspian International Transport Route",
                "environmental_concerns": "Drastic drop in sea water levels due to river damming and climate evaporation, pollution from hydrocarbon extraction",
                "historical_significance": "Historical borderland of Persian, Russian, Turkic, and nomadic empires; Silk Road transit point.",
                "overview": "The Caspian Sea is the world's largest inland body of water, often classified as the world's largest lake or a full-fledged inland sea. It possesses a salinity of roughly 1.2% (one-third that of seawater) and has no natural surface outlets."
            },
            {
                "name": "Sea of Japan",
                "slug": "sea-of-japan",
                "alternative_names": "East Sea (Korea)",
                "ocean_id": pacific.id if pacific else None,
                "sea_type": "marginal",
                "area_km2": 978000,
                "avg_depth_m": 1752,
                "max_depth_m": 3742,
                "latitude": 40.0, "longitude": 135.0,
                "surrounding_countries": "Japan, South Korea, North Korea, Russia",
                "connected_water_bodies": "Pacific Ocean (Tsugaru Strait, Kanmon Strait), East China Sea (Korea Strait), Sea of Okhotsk (La Pérouse/Soya Strait, Tatar Strait)",
                "major_ports": "Busan, Vladivostok, Niigata, Maizuru, Pohang, Wonsan",
                "major_currents": "Tsushima Warm Current, Liman Cold Current",
                "marine_life": "Giant Pacific octopus, snow crab, Japanese flying squid, Pacific bluefin tuna",
                "economic_importance": "High-volume cargo shipping between Asian industrial powers, rich squid and crab fisheries",
                "environmental_concerns": "Microplastics concentration, maritime boundary contestations, declining deep-water dissolved oxygen",
                "historical_significance": "Battle of Tsushima (1905) in the Russo-Japanese War; ancient maritime cultural exchange between Korean peninsula and Yamato Japan.",
                "overview": "The Sea of Japan is a marginal sea of the western Pacific Ocean, bounded by Japan, Sakhalin, the Korean Peninsula, and mainland Russia. It is almost entirely enclosed from open ocean waters, resulting in nearly absent tidal fluctuations."
            },
            {
                "name": "Andaman Sea",
                "slug": "andaman-sea",
                "alternative_names": "Burma Sea",
                "ocean_id": indian.id if indian else None,
                "sea_type": "marginal",
                "area_km2": 797700,
                "avg_depth_m": 1096,
                "max_depth_m": 4400,
                "latitude": 10.0, "longitude": 96.0,
                "surrounding_countries": "India (Andaman and Nicobar Islands), Myanmar, Thailand, Malaysia, Indonesia (Sumatra)",
                "connected_water_bodies": "Bay of Bengal, Indian Ocean (via Ten Degree Channel, Great Channel), Strait of Malacca",
                "major_ports": "Port Blair, Yangon, Phuket, George Town (Penang), Belawan",
                "major_currents": "Monsoonal reversing surface currents",
                "marine_life": "Dugongs, Irrawaddy dolphins, olive ridley sea turtles, coral reefs of Similan and Surin islands",
                "economic_importance": "Tourism industry (Phuket, Langkawi, Havelock Island), maritime passage leading into the Strait of Malacca, offshore gas production (Yadana field)",
                "environmental_concerns": "Tsunami vulnerability (epicenter of devastating 2004 Indian Ocean earthquake and tsunami), overfishing by commercial trawlers",
                "historical_significance": "Historic spice and trading routes between India, the Straits Settlements, and the Kingdom of Siam.",
                "overview": "The Andaman Sea is a body of water in the northeastern Indian Ocean, bounded by the coastlines of Myanmar and Thailand on the east, the Andaman and Nicobar Islands on the west, and the Strait of Malacca to the southeast."
            }
        ]

        for item in seas_data:
            existing = Sea.query.filter_by(slug=item["slug"]).first()
            if not existing:
                db.session.add(Sea(**item))
            else:
                for k, v in item.items():
                    setattr(existing, k, v)
        
        db.session.commit()

def seed_countries(app):
    with app.app_context():
        # Continents
        asia = Continent.query.filter_by(slug="asia").first()
        europe = Continent.query.filter_by(slug="europe").first()
        north_america = Continent.query.filter_by(slug="north-america").first()
        south_america = Continent.query.filter_by(slug="south-america").first()
        africa = Continent.query.filter_by(slug="africa").first()
        oceania = Continent.query.filter_by(slug="oceania").first()

        countries_data = [
            {
                "iso_a2": "IN", "iso_a3": "IND", "iso_numeric": "356",
                "common_name": "India", "official_name": "Republic of India", "slug": "india",
                "continent_id": asia.id if asia else 1, "subregion": "Southern Asia",
                "flag_emoji": "🇮🇳", "flag_svg_url": "https://flagcdn.com/in.svg",
                "capital_name": "New Delhi", "largest_city": "Mumbai",
                "area_km2": 3287263, "area_sq_mi": 1269219, "land_area_km2": 2973190, "water_area_km2": 314073,
                "population": 1428627663, "population_year": 2024, "population_density": 435.0, "urban_population_pct": 36.4,
                "latitude": 20.5937, "longitude": 78.9629,
                "highest_point": "Kangchenjunga (8,586 m)", "highest_elevation_m": 8586,
                "lowest_point": "Kuttanad (-2.2 m)", "lowest_elevation_m": -2,
                "coastline_km": 7516.6, "is_landlocked": False,
                "currency_code": "INR", "currency_name": "Indian Rupee", "currency_symbol": "₹",
                "official_languages": "Hindi, English (Union level); 22 Eighth Schedule languages",
                "widely_spoken_languages": "Bengali, Marathi, Telugu, Tamil, Gujarati, Urdu, Kannada, Odia, Malayalam, Punjabi",
                "demonym": "Indian", "calling_code": "+91", "tld": ".in",
                "time_zones": "UTC+05:30 (IST)", "driving_side": "left",
                "government_system": "Federal parliamentary constitutional republic",
                "head_of_state": "President of India", "head_of_government": "Prime Minister of India",
                "independence_date": "August 15, 1947",
                "gdp_usd_billions": 3937.0, "gdp_per_capita_usd": 2730, "gdp_reference_year": 2024,
                "major_industries": "Information technology, pharmaceuticals, textiles, steel, chemicals, automotive, agriculture",
                "natural_resources": "Coal, iron ore, manganese, mica, bauxite, rare earth elements, titanium ore, arable land",
                "climate": "Ranges from alpine tundra and glaciers in the northern Himalayas to humid tropical rainforests in the southwest and arid desert in Rajasthan.",
                "overview": "India is the world's most populous nation and the seventh-largest by land area. Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan, China, Nepal, Bhutan, Bangladesh, and Myanmar."
            },
            {
                "iso_a2": "US", "iso_a3": "USA", "iso_numeric": "840",
                "common_name": "United States", "official_name": "United States of America", "slug": "united-states",
                "continent_id": north_america.id if north_america else 4, "subregion": "Northern America",
                "flag_emoji": "🇺🇸", "flag_svg_url": "https://flagcdn.com/us.svg",
                "capital_name": "Washington, D.C.", "largest_city": "New York City",
                "area_km2": 9833517, "area_sq_mi": 3796742, "land_area_km2": 9147593, "water_area_km2": 685924,
                "population": 339996563, "population_year": 2024, "population_density": 37.0, "urban_population_pct": 83.1,
                "latitude": 37.0902, "longitude": -95.7129,
                "highest_point": "Denali (6,190 m)", "highest_elevation_m": 6190,
                "lowest_point": "Badwater Basin, Death Valley (-86 m)", "lowest_elevation_m": -86,
                "coastline_km": 19924.0, "is_landlocked": False,
                "currency_code": "USD", "currency_name": "United States Dollar", "currency_symbol": "$",
                "official_languages": "None at federal level; English is the national language",
                "widely_spoken_languages": "Spanish, Chinese, Tagalog, Vietnamese, French",
                "demonym": "American", "calling_code": "+1", "tld": ".us",
                "time_zones": "UTC-04:00 to UTC-12:00 (multiple zones)", "driving_side": "right",
                "government_system": "Federal presidential constitutional republic",
                "head_of_state": "President of the United States", "head_of_government": "President of the United States",
                "independence_date": "July 4, 1776",
                "gdp_usd_billions": 28780.0, "gdp_per_capita_usd": 85370, "gdp_reference_year": 2024,
                "major_industries": "High technology, financial services, aerospace, petroleum, motor vehicles, pharmaceuticals",
                "natural_resources": "Petroleum, natural gas, coal, timber, iron ore, copper, uranium, fertile agricultural land",
                "climate": "Mostly temperate, but tropical in Hawaii and Florida, arctic in Alaska, semiarid in the great plains, and arid in the Southwest.",
                "overview": "The United States of America is a country primarily located in North America, consisting of 50 states, a federal district, five major self-governing territories, and various possessions. It is the world's third-largest country by land area and the largest economy."
            },
            {
                "iso_a2": "JP", "iso_a3": "JPN", "iso_numeric": "392",
                "common_name": "Japan", "official_name": "Japan (Nihon-koku)", "slug": "japan",
                "continent_id": asia.id if asia else 1, "subregion": "Eastern Asia",
                "flag_emoji": "🇯🇵", "flag_svg_url": "https://flagcdn.com/jp.svg",
                "capital_name": "Tokyo", "largest_city": "Tokyo",
                "area_km2": 377975, "area_sq_mi": 145937, "land_area_km2": 364499, "water_area_km2": 13430,
                "population": 124500000, "population_year": 2024, "population_density": 332.0, "urban_population_pct": 91.8,
                "latitude": 36.2048, "longitude": 138.2529,
                "highest_point": "Mount Fuji (3,776 m)", "highest_elevation_m": 3776,
                "lowest_point": "Hachirogata (-4 m)", "lowest_elevation_m": -4,
                "coastline_km": 29751.0, "is_landlocked": False,
                "currency_code": "JPY", "currency_name": "Japanese Yen", "currency_symbol": "¥",
                "official_languages": "Japanese",
                "widely_spoken_languages": "Ryukyuan languages, Ainu",
                "demonym": "Japanese", "calling_code": "+81", "tld": ".jp",
                "time_zones": "UTC+09:00 (JST)", "driving_side": "left",
                "government_system": "Unitary parliamentary constitutional monarchy",
                "head_of_state": "Emperor of Japan", "head_of_government": "Prime Minister of Japan",
                "independence_date": "660 BC (Traditional founding)",
                "gdp_usd_billions": 4110.0, "gdp_per_capita_usd": 33130, "gdp_reference_year": 2024,
                "major_industries": "Automobiles, consumer electronics, machine tools, steel, robotics, semiconductors",
                "natural_resources": "Fish, minerals (negligible domestic deposits), volcanic thermal energy",
                "climate": "Varies from humid continental in the north (Hokkaido) with cold snowy winters to humid subtropical in the south (Kyushu/Okinawa).",
                "overview": "Japan is an island country in East Asia situated in the northwest Pacific Ocean. It is an archipelago of 14,125 islands, with the five main islands being Hokkaido, Honshu, Shikoku, Kyushu, and Okinawa."
            },
            {
                "iso_a2": "BR", "iso_a3": "BRA", "iso_numeric": "076",
                "common_name": "Brazil", "official_name": "Federative Republic of Brazil", "slug": "brazil",
                "continent_id": south_america.id if south_america else 5, "subregion": "South America",
                "flag_emoji": "🇧🇷", "flag_svg_url": "https://flagcdn.com/br.svg",
                "capital_name": "Brasília", "largest_city": "São Paulo",
                "area_km2": 8515767, "area_sq_mi": 3287957, "land_area_km2": 8460415, "water_area_km2": 55352,
                "population": 216422446, "population_year": 2024, "population_density": 25.4, "urban_population_pct": 87.6,
                "latitude": -14.2350, "longitude": -51.9253,
                "highest_point": "Pico da Neblina (2,995 m)", "highest_elevation_m": 2995,
                "lowest_point": "Atlantic Ocean (0 m)", "lowest_elevation_m": 0,
                "coastline_km": 7491.0, "is_landlocked": False,
                "currency_code": "BRL", "currency_name": "Brazilian Real", "currency_symbol": "R$",
                "official_languages": "Portuguese",
                "widely_spoken_languages": "Indigenous languages (Guarani, Ticuna), German dialects",
                "demonym": "Brazilian", "calling_code": "+55", "tld": ".br",
                "time_zones": "UTC-02:00 to UTC-05:00", "driving_side": "right",
                "government_system": "Federal presidential constitutional republic",
                "head_of_state": "President of Brazil", "head_of_government": "President of Brazil",
                "independence_date": "September 7, 1822",
                "gdp_usd_billions": 2330.0, "gdp_per_capita_usd": 10820, "gdp_reference_year": 2024,
                "major_industries": "Agriculture (soybeans, coffee, beef, sugar), iron ore mining, aircraft manufacturing (Embraer), petroleum",
                "natural_resources": "Iron ore, manganese, bauxite, nickel, uranium, timber, hydropower, petroleum",
                "climate": "Mostly tropical (Amazon basin), with semiarid conditions in the northeast and temperate conditions in the south.",
                "overview": "Brazil is the largest country in both South America and Latin America. Spanning over 8.5 million square kilometers, it contains around 60% of the Amazon Rainforest and borders all other South American countries except Chile and Ecuador."
            },
            {
                "iso_a2": "DE", "iso_a3": "DEU", "iso_numeric": "276",
                "common_name": "Germany", "official_name": "Federal Republic of Germany", "slug": "germany",
                "continent_id": europe.id if europe else 3, "subregion": "Western Europe",
                "flag_emoji": "🇩🇪", "flag_svg_url": "https://flagcdn.com/de.svg",
                "capital_name": "Berlin", "largest_city": "Berlin",
                "area_km2": 357022, "area_sq_mi": 137847, "land_area_km2": 348672, "water_area_km2": 8350,
                "population": 84400000, "population_year": 2024, "population_density": 236.0, "urban_population_pct": 77.7,
                "latitude": 51.1657, "longitude": 10.4515,
                "highest_point": "Zugspitze (2,962 m)", "highest_elevation_m": 2962,
                "lowest_point": "Neuendorf-Sachsenbande (-3.5 m)", "lowest_elevation_m": -3.5,
                "coastline_km": 2389.0, "is_landlocked": False,
                "currency_code": "EUR", "currency_name": "Euro", "currency_symbol": "€",
                "official_languages": "German",
                "widely_spoken_languages": "Low German, Sorbian, Romani, Frisian, Turkish",
                "demonym": "German", "calling_code": "+49", "tld": ".de",
                "time_zones": "UTC+01:00 (CET), UTC+02:00 (CEST)", "driving_side": "right",
                "government_system": "Federal parliamentary republic",
                "head_of_state": "Federal President of Germany", "head_of_government": "Chancellor of Germany",
                "independence_date": "January 18, 1871 (Unification); October 3, 1990 (Reunification)",
                "gdp_usd_billions": 4590.0, "gdp_per_capita_usd": 54290, "gdp_reference_year": 2024,
                "major_industries": "Automotive engineering, machinery and equipment, chemicals, electronics, precision engineering",
                "natural_resources": "Coal, lignite, natural gas, iron ore, copper, nickel, timber, arable land",
                "climate": "Temperate seasonal climate, with humid westerly winds moderating winter and summer temperatures.",
                "overview": "Germany is a country in Central Europe. It is the second-most populous country in Europe after Russia, and the most populous member state of the European Union, situated between the Baltic and North Seas to the north and the Alps to the south."
            },
            {
                "iso_a2": "EG", "iso_a3": "EGY", "iso_numeric": "818",
                "common_name": "Egypt", "official_name": "Arab Republic of Egypt", "slug": "egypt",
                "continent_id": africa.id if africa else 2, "subregion": "Northern Africa",
                "flag_emoji": "🇪🇬", "flag_svg_url": "https://flagcdn.com/eg.svg",
                "capital_name": "Cairo", "largest_city": "Cairo",
                "area_km2": 1002450, "area_sq_mi": 387050, "land_area_km2": 995450, "water_area_km2": 6000,
                "population": 112716598, "population_year": 2024, "population_density": 112.0, "urban_population_pct": 43.1,
                "latitude": 26.8206, "longitude": 30.8025,
                "highest_point": "Mount Catherine (2,629 m)", "highest_elevation_m": 2629,
                "lowest_point": "Qattara Depression (-133 m)", "lowest_elevation_m": -133,
                "coastline_km": 2450.0, "is_landlocked": False,
                "currency_code": "EGP", "currency_name": "Egyptian Pound", "currency_symbol": "E£",
                "official_languages": "Arabic",
                "widely_spoken_languages": "Egyptian Arabic, Sa'idi Arabic, Bedawi Arabic, Siwi Berber, Nubian",
                "demonym": "Egyptian", "calling_code": "+20", "tld": ".eg",
                "time_zones": "UTC+02:00, UTC+03:00 (DST)", "driving_side": "right",
                "government_system": "Unitary semi-presidential republic",
                "head_of_state": "President of Egypt", "head_of_government": "Prime Minister of Egypt",
                "independence_date": "February 28, 1922",
                "gdp_usd_billions": 380.0, "gdp_per_capita_usd": 3410, "gdp_reference_year": 2024,
                "major_industries": "Tourism, Suez Canal maritime services, textiles, hydrocarbons, food processing, chemicals",
                "natural_resources": "Petroleum, natural gas, iron ore, phosphates, manganese, limestone, gypsum, talc",
                "climate": "Hyper-arid desert climate throughout most of the country, with mild Mediterranean conditions along the northern coastal strip.",
                "overview": "Egypt is a transcontinental country spanning the northeast corner of Africa and southwest corner of Asia via the Sinai Peninsula. The Nile River valley and delta are home to one of the world's oldest continuous civilizations."
            },
            {
                "iso_a2": "AU", "iso_a3": "AUS", "iso_numeric": "036",
                "common_name": "Australia", "official_name": "Commonwealth of Australia", "slug": "australia",
                "continent_id": oceania.id if oceania else 7, "subregion": "Australia and New Zealand",
                "flag_emoji": "🇦🇺", "flag_svg_url": "https://flagcdn.com/au.svg",
                "capital_name": "Canberra", "largest_city": "Sydney",
                "area_km2": 7692024, "area_sq_mi": 2969907, "land_area_km2": 7682300, "water_area_km2": 58924,
                "population": 26800000, "population_year": 2024, "population_density": 3.5, "urban_population_pct": 86.4,
                "latitude": -25.2744, "longitude": 133.7751,
                "highest_point": "Mount Kosciuszko (2,228 m)", "highest_elevation_m": 2228,
                "lowest_point": "Lake Eyre (-15 m)", "lowest_elevation_m": -15,
                "coastline_km": 25760.0, "is_landlocked": False,
                "currency_code": "AUD", "currency_name": "Australian Dollar", "currency_symbol": "A$",
                "official_languages": "English",
                "widely_spoken_languages": "Mandarin, Arabic, Vietnamese, Cantonese, Indigenous Australian languages",
                "demonym": "Australian", "calling_code": "+61", "tld": ".au",
                "time_zones": "UTC+08:00 to UTC+10:30", "driving_side": "left",
                "government_system": "Federal parliamentary constitutional monarchy",
                "head_of_state": "Monarch of Australia", "head_of_government": "Prime Minister of Australia",
                "independence_date": "January 1, 1901 (Federation)",
                "gdp_usd_billions": 1790.0, "gdp_per_capita_usd": 66580, "gdp_reference_year": 2024,
                "major_industries": "Mining (iron ore, coal, gold, lithium), financial services, agriculture (wheat, wool, beef), higher education",
                "natural_resources": "Bauxite, coal, iron ore, copper, tin, gold, silver, uranium, nickel, tungsten, rare earths, mineral sands, lead, zinc, diamonds, natural gas, petroleum",
                "climate": "Mostly arid to semi-arid in the interior (Outback), with temperate climates in the south and east, and tropical climates in the north.",
                "overview": "Australia is a sovereign country comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands. It is the largest country by area in Oceania and the world's sixth-largest country."
            },
            {
                "iso_a2": "CA", "iso_a3": "CAN", "iso_numeric": "124",
                "common_name": "Canada", "official_name": "Canada", "slug": "canada",
                "continent_id": north_america.id if north_america else 4, "subregion": "Northern America",
                "flag_emoji": "🇨🇦", "flag_svg_url": "https://flagcdn.com/ca.svg",
                "capital_name": "Ottawa", "largest_city": "Toronto",
                "area_km2": 9984670, "area_sq_mi": 3855100, "land_area_km2": 9093507, "water_area_km2": 891163,
                "population": 40100000, "population_year": 2024, "population_density": 4.2, "urban_population_pct": 81.7,
                "latitude": 56.1304, "longitude": -106.3468,
                "highest_point": "Mount Logan (5,959 m)", "highest_elevation_m": 5959,
                "lowest_point": "Atlantic Ocean (0 m)", "lowest_elevation_m": 0,
                "coastline_km": 202080.0, "is_landlocked": False,
                "currency_code": "CAD", "currency_name": "Canadian Dollar", "currency_symbol": "C$",
                "official_languages": "English, French",
                "widely_spoken_languages": "Inuktitut, Cree, Punjabi, Cantonese, Spanish",
                "demonym": "Canadian", "calling_code": "+1", "tld": ".ca",
                "time_zones": "UTC-03:30 to UTC-08:00", "driving_side": "right",
                "government_system": "Federal parliamentary constitutional monarchy",
                "head_of_state": "Monarch of Canada", "head_of_government": "Prime Minister of Canada",
                "independence_date": "July 1, 1867 (Confederation)",
                "gdp_usd_billions": 2240.0, "gdp_per_capita_usd": 55520, "gdp_reference_year": 2024,
                "major_industries": "Natural resources, energy (crude petroleum, natural gas), automotive, aerospace, chemicals, telecommunications",
                "natural_resources": "Iron ore, nickel, zinc, copper, gold, lead, rare earth elements, potash, diamonds, silver, fish, timber, wildlife, coal, petroleum, natural gas, hydro power",
                "climate": "Varies from temperate on the west coast to subarctic and arctic in the north.",
                "overview": "Canada is a country in North America. Its ten provinces and three territories extend from the Atlantic to the Pacific and northward into the Arctic Ocean, covering nearly 10 million square kilometers, making it the world's second-largest country by total area."
            },
            {
                "iso_a2": "CN", "iso_a3": "CHN", "iso_numeric": "156",
                "common_name": "China", "official_name": "People's Republic of China", "slug": "china",
                "continent_id": asia.id if asia else 1, "subregion": "Eastern Asia",
                "flag_emoji": "🇨🇳", "flag_svg_url": "https://flagcdn.com/cn.svg",
                "capital_name": "Beijing", "largest_city": "Shanghai",
                "area_km2": 9596961, "area_sq_mi": 3705407, "land_area_km2": 9326410, "water_area_km2": 270550,
                "population": 1409670000, "population_year": 2024, "population_density": 150.0, "urban_population_pct": 65.2,
                "latitude": 35.8617, "longitude": 104.1954,
                "highest_point": "Mount Everest (8,848 m)", "highest_elevation_m": 8848,
                "lowest_point": "Ayding Lake (-154 m)", "lowest_elevation_m": -154,
                "coastline_km": 14500.0, "is_landlocked": False,
                "currency_code": "CNY", "currency_name": "Chinese Yuan (Renminbi)", "currency_symbol": "¥",
                "official_languages": "Standard Chinese (Mandarin)",
                "widely_spoken_languages": "Cantonese (Yue), Wu (Shanghainese), Min, Xiang, Hakka, Tibetan, Uyghur, Mongolian",
                "demonym": "Chinese", "calling_code": "+86", "tld": ".cn",
                "time_zones": "UTC+08:00 (CST)", "driving_side": "right",
                "government_system": "Unitary one-party socialist republic",
                "head_of_state": "President of China", "head_of_government": "Premier of China",
                "independence_date": "October 1, 1949",
                "gdp_usd_billions": 18530.0, "gdp_per_capita_usd": 13140, "gdp_reference_year": 2024,
                "major_industries": "Manufacturing, electronics, steel, solar panels, electric vehicles, chemicals, textiles",
                "natural_resources": "Coal, iron ore, petroleum, natural gas, mercury, tin, tungsten, antimony, manganese, molybdenum, vanadium, magnetite, aluminum, lead, zinc, rare earths, uranium",
                "climate": "Extremely diverse, ranging from subarctic in the north to tropical in the south, and alpine in the Tibetan Plateau.",
                "overview": "China is a country in East Asia. It is the world's second-most populous country and the third-largest by land area. Covering five geographical time zones and bordering 14 countries by land, China has one of the world's earliest civilizations."
            },
            {
                "iso_a2": "GB", "iso_a3": "GBR", "iso_numeric": "826",
                "common_name": "United Kingdom", "official_name": "United Kingdom of Great Britain and Northern Ireland", "slug": "united-kingdom",
                "continent_id": europe.id if europe else 3, "subregion": "Northern Europe",
                "flag_emoji": "🇬🇧", "flag_svg_url": "https://flagcdn.com/gb.svg",
                "capital_name": "London", "largest_city": "London",
                "area_km2": 242495, "area_sq_mi": 93628, "land_area_km2": 241930, "water_area_km2": 1680,
                "population": 68265209, "population_year": 2024, "population_density": 281.0, "urban_population_pct": 84.4,
                "latitude": 55.3781, "longitude": -3.4360,
                "highest_point": "Ben Nevis (1,345 m)", "highest_elevation_m": 1345,
                "lowest_point": "The Fens (-4 m)", "lowest_elevation_m": -4,
                "coastline_km": 12429.0, "is_landlocked": False,
                "currency_code": "GBP", "currency_name": "British Pound Sterling", "currency_symbol": "£",
                "official_languages": "English",
                "widely_spoken_languages": "Welsh, Scots, Scottish Gaelic, Irish, Cornish",
                "demonym": "British", "calling_code": "+44", "tld": ".uk",
                "time_zones": "UTC+00:00 (GMT), UTC+01:00 (BST)", "driving_side": "left",
                "government_system": "Unitary parliamentary constitutional monarchy",
                "head_of_state": "Monarch of the United Kingdom", "head_of_government": "Prime Minister of the United Kingdom",
                "independence_date": "May 1, 1707 (Act of Union)",
                "gdp_usd_billions": 3500.0, "gdp_per_capita_usd": 51070, "gdp_reference_year": 2024,
                "major_industries": "Financial services, aerospace, pharmaceuticals, automotive, creative media, North Sea oil and gas",
                "natural_resources": "Coal, petroleum, natural gas, iron ore, salt, clay, chalk, gypsum, lead, silica",
                "climate": "Temperate oceanic climate, with abundant rainfall all year round, cool summers and mild winters.",
                "overview": "The United Kingdom of Great Britain and Northern Ireland is an island country situated off the northwestern coast of continental Europe. The country includes the island of Great Britain, the northeastern part of the island of Ireland, and many smaller islands."
            }
        ]

        for item in countries_data:
            existing = Country.query.filter_by(slug=item["slug"]).first()
            if not existing:
                db.session.add(Country(**item))
            else:
                for k, v in item.items():
                    setattr(existing, k, v)
        
        db.session.commit()

        # Seed capitals
        capitals_data = [
            ("IND", "New Delhi", 28.6139, 77.2090, 216, 33000000),
            ("USA", "Washington, D.C.", 38.9072, -77.0369, 7, 712000),
            ("JPN", "Tokyo", 35.6762, 139.6503, 40, 37400000),
            ("BRA", "Brasília", -15.7975, -47.8919, 1172, 3055149),
            ("DEU", "Berlin", 52.5200, 13.4050, 34, 3850809),
            ("EGY", "Cairo", 30.0444, 31.2357, 23, 22183200),
            ("AUS", "Canberra", -35.2809, 149.1300, 580, 456652),
            ("CAN", "Ottawa", 45.4215, -75.6972, 70, 1017449),
            ("CHN", "Beijing", 39.9042, 116.4074, 43, 21893095),
            ("GBR", "London", 51.5074, -0.1278, 11, 9648000)
        ]
        for iso3, cname, lat, lon, elev, pop in capitals_data:
            country = Country.query.filter_by(iso_a3=iso3).first()
            if country and not Capital.query.filter_by(country_id=country.id, name=cname).first():
                db.session.add(Capital(country_id=country.id, name=cname, latitude=lat, longitude=lon, elevation_m=elev, population=pop))

        # Seed Borders
        borders_data = [
            ("IND", "PAK", "land", 3323.0),
            ("IND", "CHN", "land", 3488.0),
            ("IND", "NPL", "land", 1751.0),
            ("IND", "BTN", "land", 699.0),
            ("IND", "BGD", "land", 4096.7),
            ("IND", "MMR", "land", 1643.0),
            ("IND", "LKA", "maritime", 30.0), # Palk Strait
            ("USA", "CAN", "land", 8891.0),
            ("USA", "MEX", "land", 3145.0),
            ("DEU", "FRA", "land", 451.0),
            ("DEU", "POL", "land", 467.0),
            ("DEU", "AUT", "land", 784.0),
            ("BRA", "ARG", "land", 1261.0),
            ("BRA", "COL", "land", 1644.0),
            ("EGY", "LBY", "land", 1115.0),
            ("EGY", "SDN", "land", 1275.0),
            ("EGY", "ISR", "land", 208.0)
        ]
        for c1, c2, btype, blen in borders_data:
            exists = Border.query.filter_by(country_a_iso=c1, country_b_iso=c2, border_type=btype).first()
            if not exists:
                db.session.add(Border(country_a_iso=c1, country_b_iso=c2, border_type=btype, length_km=blen))

        db.session.commit()

def seed_administrative_divisions(app):
    with app.app_context():
        india = Country.query.filter_by(iso_a3="IND").first()
        usa = Country.query.filter_by(iso_a3="USA").first()
        japan = Country.query.filter_by(iso_a3="JPN").first()
        germany = Country.query.filter_by(iso_a3="DEU").first()

        # India States and Union Territories with districts
        if india:
            india_states = [
                ("Maharashtra", "maharashtra", "IN-MH", "State", "Mumbai", 307713, 112374333, 19.7515, 75.7139, [
                    ("Mumbai City", "mumbai-city", "District", "Mumbai", 157, 3085411, 18.9388, 72.8354),
                    ("Pune", "pune", "District", "Pune", 15643, 9429408, 18.5204, 73.8567),
                    ("Nagpur", "nagpur", "District", "Nagpur", 9892, 4653570, 21.1458, 79.0882),
                    ("Thane", "thane", "District", "Thane", 4214, 11060148, 19.2183, 72.9781)
                ]),
                ("Uttar Pradesh", "uttar-pradesh", "IN-UP", "State", "Lucknow", 240928, 199812341, 26.8467, 80.9462, [
                    ("Lucknow", "lucknow", "District", "Lucknow", 2528, 4589838, 26.8467, 80.9462),
                    ("Varanasi", "varanasi", "District", "Varanasi", 1535, 3676841, 25.3176, 82.9739),
                    ("Kanpur Nagar", "kanpur-nagar", "District", "Kanpur", 3155, 4581268, 26.4499, 80.3319),
                    ("Agra", "agra", "District", "Agra", 4027, 4418797, 27.1767, 78.0081)
                ]),
                ("Karnataka", "karnataka", "IN-KA", "State", "Bengaluru", 191791, 61095297, 15.3173, 75.7139, [
                    ("Bengaluru Urban", "bengaluru-urban", "District", "Bengaluru", 2196, 9621551, 12.9716, 77.5946),
                    ("Mysuru", "mysuru", "District", "Mysuru", 6854, 3001127, 12.2958, 76.6394)
                ]),
                ("Tamil Nadu", "tamil-nadu", "IN-TN", "State", "Chennai", 130060, 72147030, 11.1271, 78.6569, [
                    ("Chennai", "chennai", "District", "Chennai", 426, 7088000, 13.0827, 80.2707),
                    ("Coimbatore", "coimbatore", "District", "Coimbatore", 4723, 3458045, 11.0168, 76.9558)
                ]),
                ("Gujarat", "gujarat", "IN-GJ", "State", "Gandhinagar", 196024, 60439692, 22.2587, 71.1924, [
                    ("Ahmedabad", "ahmedabad", "District", "Ahmedabad", 8707, 7214225, 23.0225, 72.5714),
                    ("Surat", "surat", "District", "Surat", 4418, 6081322, 21.1702, 72.8311)
                ]),
                ("Delhi", "delhi", "IN-DL", "Union Territory", "New Delhi", 1484, 16787941, 28.7041, 77.1025, [
                    ("New Delhi", "new-delhi-district", "District", "Connaught Place", 35, 142004, 28.6139, 77.2090),
                    ("Central Delhi", "central-delhi", "District", "Daryaganj", 25, 582320, 28.6450, 77.2400)
                ])
            ]

            for sname, sslug, scode, stype, scap, sarea, spop, slat, slon, districts in india_states:
                st = AdministrativeDivision.query.filter_by(country_id=india.id, slug=sslug).first()
                if not st:
                    st = AdministrativeDivision(
                        country_id=india.id, name=sname, slug=sslug, code=scode,
                        division_type=stype, capital_or_center=scap, area_km2=sarea,
                        population=spop, latitude=slat, longitude=slon
                    )
                    db.session.add(st)
                    db.session.flush()

                for dname, dslug, dtype, dcap, darea, dpop, dlat, dlon in districts:
                    if not AdministrativeDivision.query.filter_by(country_id=india.id, slug=dslug).first():
                        db.session.add(AdministrativeDivision(
                            country_id=india.id, parent_division_id=st.id, name=dname, slug=dslug,
                            code=f"{scode}-{dslug.upper()[:3]}", division_type=dtype,
                            capital_or_center=dcap, area_km2=darea, population=dpop,
                            latitude=dlat, longitude=dlon
                        ))

        # USA States
        if usa:
            usa_states = [
                ("California", "california", "US-CA", "State", "Sacramento", 423970, 39029342, 36.7783, -119.4179),
                ("Texas", "texas", "US-TX", "State", "Austin", 695662, 30029572, 31.9686, -99.9018),
                ("New York", "new-york", "US-NY", "State", "Albany", 141300, 19677151, 40.7128, -74.0060),
                ("Florida", "florida", "US-FL", "State", "Tallahassee", 170312, 22244823, 27.6648, -81.5158)
            ]
            for sname, sslug, scode, stype, scap, sarea, spop, slat, slon in usa_states:
                if not AdministrativeDivision.query.filter_by(country_id=usa.id, slug=sslug).first():
                    db.session.add(AdministrativeDivision(
                        country_id=usa.id, name=sname, slug=sslug, code=scode,
                        division_type=stype, capital_or_center=scap, area_km2=sarea,
                        population=spop, latitude=slat, longitude=slon
                    ))

        # Japan Prefectures
        if japan:
            japan_pref = [
                ("Tokyo", "tokyo-prefecture", "JP-13", "Metropolis", "Shinjuku", 2194, 14094034, 35.6895, 139.6917),
                ("Osaka", "osaka-prefecture", "JP-27", "Prefecture", "Osaka", 1905, 8823458, 34.6937, 135.5023),
                ("Kyoto", "kyoto-prefecture", "JP-26", "Prefecture", "Kyoto", 4612, 2583140, 35.0116, 135.7681)
            ]
            for sname, sslug, scode, stype, scap, sarea, spop, slat, slon in japan_pref:
                if not AdministrativeDivision.query.filter_by(country_id=japan.id, slug=sslug).first():
                    db.session.add(AdministrativeDivision(
                        country_id=japan.id, name=sname, slug=sslug, code=scode,
                        division_type=stype, capital_or_center=scap, area_km2=sarea,
                        population=spop, latitude=slat, longitude=slon
                    ))

        # Germany States (Länder)
        if germany:
            de_states = [
                ("Bavaria", "bavaria", "DE-BY", "State (Land)", "Munich", 70550, 13369393, 48.7904, 11.4979),
                ("Berlin", "berlin-state", "DE-BE", "City-State (Land)", "Berlin", 891, 3850809, 52.5200, 13.4050)
            ]
            for sname, sslug, scode, stype, scap, sarea, spop, slat, slon in de_states:
                if not AdministrativeDivision.query.filter_by(country_id=germany.id, slug=sslug).first():
                    db.session.add(AdministrativeDivision(
                        country_id=germany.id, name=sname, slug=sslug, code=scode,
                        division_type=stype, capital_or_center=scap, area_km2=sarea,
                        population=spop, latitude=slat, longitude=slon
                    ))

        db.session.commit()

def seed_geographic_features(app):
    with app.app_context():
        asia = Continent.query.filter_by(slug="asia").first()
        africa = Continent.query.filter_by(slug="africa").first()
        europe = Continent.query.filter_by(slug="europe").first()
        north_america = Continent.query.filter_by(slug="north-america").first()
        south_america = Continent.query.filter_by(slug="south-america").first()
        oceania = Continent.query.filter_by(slug="oceania").first()

        features_data = [
            {
                "name": "Himalayas", "slug": "himalayas",
                "alternative_names": "Abode of Snow, Himalaya Parvat",
                "feature_type": "mountain_range",
                "continent_id": asia.id if asia else 1,
                "primary_country_iso": "IND",
                "countries_involved": "India, Nepal, Bhutan, China, Pakistan",
                "latitude": 27.9881, "longitude": 86.9250,
                "elevation_m": 8848, "length_km": 2400.0, "area_km2": 595000,
                "connected_features": "Tibetan Plateau, Karakoram, Hindu Kush",
                "overview": "The Himalayas form an immense mountain range in Asia separating the plains of the Indian subcontinent from the Tibetan Plateau. The range includes over 50 mountains exceeding 7,200 m (23,600 ft) in elevation, including Mount Everest.",
                "data_source": "USGS / Survey of India (2024)"
            },
            {
                "name": "Mount Everest", "slug": "mount-everest",
                "alternative_names": "Sagarmatha, Chomolungma",
                "feature_type": "mountain",
                "continent_id": asia.id if asia else 1,
                "primary_country_iso": "NPL",
                "countries_involved": "Nepal, China",
                "latitude": 27.9881, "longitude": 86.9250,
                "elevation_m": 8848,
                "connected_features": "Himalayas, Khumbu Glacier, South Col",
                "overview": "Mount Everest is Earth's highest mountain above sea level, located in the Mahalangur Himal sub-range of the Himalayas. The international border between China and Nepal runs across its summit point.",
                "data_source": "Survey of Nepal / National Geographic (2020 official remeasurement 8,848.86 m)"
            },
            {
                "name": "Ganga (Ganges)", "slug": "ganges-river",
                "alternative_names": "Ganga, Jahnavi, Bhagirathi-Hooghly",
                "feature_type": "river",
                "continent_id": asia.id if asia else 1,
                "primary_country_iso": "IND",
                "countries_involved": "India, Bangladesh",
                "latitude": 25.3176, "longitude": 83.0000,
                "length_km": 2525.0, "area_km2": 1086000,
                "connected_features": "Gangotri Glacier, Yamuna, Brahmaputra, Bay of Bengal (Sundarbans)",
                "overview": "The Ganga is a trans-boundary river of Asia which flows through India and Bangladesh. Rising in the western Himalayas in the Indian state of Uttarakhand, it flows south and east through the Gangetic Plain of India into Bangladesh, where it empties into the Bay of Bengal.",
                "data_source": "Central Water Commission (India)"
            },
            {
                "name": "Nile River", "slug": "nile-river",
                "alternative_names": "An-Nil, White Nile & Blue Nile",
                "feature_type": "river",
                "continent_id": africa.id if africa else 2,
                "primary_country_iso": "EGY",
                "countries_involved": "Egypt, Sudan, South Sudan, Ethiopia, Uganda, Congo, Kenya, Tanzania, Rwanda, Burundi",
                "latitude": 30.1667, "longitude": 31.2500,
                "length_km": 6650.0, "area_km2": 3400000,
                "connected_features": "Lake Victoria, Lake Tana, Mediterranean Sea, Aswan High Dam",
                "overview": "The Nile is traditionally regarded as the longest river in the world. Flowing northward through northeastern Africa, it is the primary water source of Egypt and Sudan, sustaining civilizations for millennia.",
                "data_source": "FAO / Nile Basin Initiative"
            },
            {
                "name": "Amazon River", "slug": "amazon-river",
                "alternative_names": "Rio Amazonas",
                "feature_type": "river",
                "continent_id": south_america.id if south_america else 5,
                "primary_country_iso": "BRA",
                "countries_involved": "Brazil, Peru, Colombia, Bolivia, Ecuador, Venezuela",
                "latitude": -3.4653, "longitude": -58.3800,
                "length_km": 6400.0, "area_km2": 7050000,
                "connected_features": "Amazon Rainforest, Andes Mountains, Atlantic Ocean",
                "overview": "The Amazon River in South America is the largest river by discharge volume of water in the world, holding greater water flow than the next seven largest rivers combined, and accounting for roughly one-fifth of the world's total river flow.",
                "data_source": "ANA Brazil / UNESCO Hydrology"
            },
            {
                "name": "Sahara Desert", "slug": "sahara-desert",
                "alternative_names": "Al-Sahra al-Kubra",
                "feature_type": "desert",
                "continent_id": africa.id if africa else 2,
                "primary_country_iso": "DZA",
                "countries_involved": "Algeria, Chad, Egypt, Libya, Mali, Mauritania, Morocco, Niger, Sudan, Tunisia",
                "latitude": 23.4162, "longitude": 25.6628,
                "area_km2": 9200000,
                "connected_features": "Atlas Mountains, Sahel, Red Sea, Atlantic Ocean",
                "overview": "The Sahara is the largest hot desert in the world and the third largest desert overall, smaller only than the cold polar deserts of Antarctica and the Arctic. Its area of 9,200,000 square kilometers is comparable to the area of China or the United States.",
                "data_source": "UNEP World Conservation Monitoring Centre"
            },
            {
                "name": "Strait of Gibraltar", "slug": "strait-of-gibraltar",
                "alternative_names": "Estrecho de Gibraltar, Pillars of Hercules",
                "feature_type": "strait",
                "continent_id": europe.id if europe else 3,
                "primary_country_iso": "ESP",
                "countries_involved": "Spain, Morocco, United Kingdom (Gibraltar)",
                "latitude": 35.9611, "longitude": -5.5889,
                "length_km": 58.0, "depth_m": 900,
                "connected_features": "Atlantic Ocean, Mediterranean Sea, Alboran Sea, Rock of Gibraltar",
                "overview": "The Strait of Gibraltar is a narrow strait that connects the Atlantic Ocean to the Mediterranean Sea and separates the Iberian Peninsula in Europe from Morocco in Africa. It spans approximately 13 km (8.1 mi) of width at its narrowest point.",
                "data_source": "International Hydrographic Organization"
            },
            {
                "name": "Mariana Trench", "slug": "mariana-trench",
                "alternative_names": "Challenger Deep",
                "feature_type": "trench",
                "continent_id": asia.id if asia else 1,
                "primary_country_iso": None,
                "countries_involved": "Micronesia, Northern Mariana Islands (US)",
                "latitude": 11.3493, "longitude": 142.1996,
                "depth_m": 10994, "length_km": 2550.0,
                "connected_features": "Pacific Ocean, Philippine Sea, Izu–Bonin–Mariana Arc",
                "overview": "The Mariana Trench is an oceanic trench located in the western Pacific Ocean, about 200 kilometres (124 mi) east of the Mariana Islands; it is the deepest oceanic trench on Earth, reaching a maximum known depth of 10,994 meters at Challenger Deep.",
                "data_source": "NOAA / GEBCO (2021 multibeam bathymetric surveys)"
            },
            # Major World Islands & Archipelagos
            {
                "name": "Greenland", "slug": "greenland-island",
                "alternative_names": "Kalaallit Nunaat",
                "feature_type": "island",
                "continent_id": north_america.id if north_america else 4,
                "primary_country_iso": "GRL",
                "countries_involved": "Greenland (Autonomous territory within the Kingdom of Denmark)",
                "latitude": 71.7069, "longitude": -42.6043,
                "area_km2": 2166086, "elevation_m": 3694,
                "connected_features": "Arctic Ocean, Atlantic Ocean, Baffin Bay, Greenland Ice Sheet",
                "overview": "Greenland is the world's largest island, located between the Arctic and Atlantic oceans, east of the Canadian Arctic Archipelago. About 80% of its surface is covered by the massive Greenland ice sheet.",
                "data_source": "National Park Service / GEUS Denmark"
            },
            {
                "name": "Madagascar", "slug": "madagascar-island",
                "alternative_names": "Nosy Madagasikara, Red Island",
                "feature_type": "island",
                "continent_id": africa.id if africa else 2,
                "primary_country_iso": "MDG",
                "countries_involved": "Madagascar",
                "latitude": -18.7669, "longitude": 46.8691,
                "area_km2": 587041, "elevation_m": 2876,
                "connected_features": "Indian Ocean, Mozambique Channel",
                "overview": "Madagascar is an island country in the Indian Ocean, approximately 400 kilometres off the coast of East Africa. It is the fourth largest island in the world, renowned for extraordinary endemic biodiversity.",
                "data_source": "WWF / UNESCO World Heritage"
            },
            {
                "name": "Borneo", "slug": "borneo-island",
                "alternative_names": "Kalimantan",
                "feature_type": "island",
                "continent_id": asia.id if asia else 1,
                "primary_country_iso": "IDN",
                "countries_involved": "Indonesia, Malaysia, Brunei",
                "latitude": 0.9619, "longitude": 114.5548,
                "area_km2": 748168, "elevation_m": 4095,
                "connected_features": "Pacific Ocean, South China Sea, Celebes Sea, Java Sea",
                "overview": "Borneo is the third-largest island in the world and the largest in Asia. It is politically divided among three countries: Malaysia and Brunei in the north, and Indonesia to the south.",
                "data_source": "ASEAN Centre for Biodiversity"
            },
            {
                "name": "New Guinea", "slug": "new-guinea-island",
                "alternative_names": "Papua",
                "feature_type": "island",
                "continent_id": oceania.id if oceania else 6,
                "primary_country_iso": "PNG",
                "countries_involved": "Papua New Guinea, Indonesia (Western New Guinea)",
                "latitude": -4.2699, "longitude": 138.0804,
                "area_km2": 785753, "elevation_m": 4884,
                "connected_features": "Pacific Ocean, Coral Sea, Arafura Sea, Puncak Jaya",
                "overview": "New Guinea is the world's second-largest island, located in the southwest Pacific Ocean, separated from the Australian continent by the shallow Torres Strait.",
                "data_source": "UNESCO / Geoscience Australia"
            },
            {
                "name": "Hawaii Archipelago", "slug": "hawaii-archipelago",
                "alternative_names": "Hawaiian Islands, Mokupuni o Hawai'i",
                "feature_type": "archipelago",
                "continent_id": north_america.id if north_america else 4,
                "primary_country_iso": "USA",
                "countries_involved": "United States",
                "latitude": 19.8968, "longitude": -155.5828,
                "area_km2": 28311, "elevation_m": 4207,
                "connected_features": "North Pacific Ocean, Mauna Kea, Mauna Loa",
                "overview": "The Hawaiian Archipelago is an isolated volcanic island chain in the central Pacific Ocean, formed by a mantle plume hotspot and home to towering active shield volcanoes.",
                "data_source": "USGS Hawaiian Volcano Observatory"
            },
            {
                "name": "Maldives Archipelago", "slug": "maldives-archipelago",
                "alternative_names": "Dhivehi Raajje, Maldivian Atolls",
                "feature_type": "archipelago",
                "continent_id": asia.id if asia else 1,
                "primary_country_iso": "MDV",
                "countries_involved": "Maldives",
                "latitude": 3.2028, "longitude": 73.2207,
                "area_km2": 298, "elevation_m": 2,
                "connected_features": "Indian Ocean, Arabian Sea, Laccadive Sea",
                "overview": "The Maldives is an archipelagic nation of 26 natural coral atolls encompassing 1,192 coral islands in the Indian Ocean, famous for its barrier reefs, turquoise lagoons, and low-lying topography.",
                "data_source": "Ministry of Environment Maldives / GEBCO"
            },
            {
                "name": "Iceland", "slug": "iceland-island",
                "alternative_names": "Ísland",
                "feature_type": "island",
                "continent_id": europe.id if europe else 3,
                "primary_country_iso": "ISL",
                "countries_involved": "Iceland",
                "latitude": 64.9631, "longitude": -19.0208,
                "area_km2": 103000, "elevation_m": 2110,
                "connected_features": "Atlantic Ocean, Arctic Ocean, Mid-Atlantic Ridge",
                "overview": "Iceland is a Nordic island country in the North Atlantic situated on the Mid-Atlantic Ridge, famous for dramatic volcanic activity, geothermal geysers, glaciers, and black sand beaches.",
                "data_source": "National Land Survey of Iceland"
            }
        ]

        for item in features_data:
            existing = GeographicFeature.query.filter_by(slug=item["slug"]).first()
            if not existing:
                db.session.add(GeographicFeature(**item))
            else:
                for k, v in item.items():
                    setattr(existing, k, v)
        
        db.session.commit()

def seed_data_sources(app):
    with app.app_context():
        sources = [
            {
                "name": "Natural Earth", "category": "Boundaries & Vectors",
                "organization": "Natural Earth Project / NACIS",
                "url": "https://www.naturalearthdata.com", "license": "Public Domain (CC0)",
                "description": "Public domain map dataset available at 1:10m, 1:50m, and 1:110m scales containing integrated vector and raster data."
            },
            {
                "name": "GeoNames", "category": "Gazetteer & Places",
                "organization": "GeoNames.org",
                "url": "https://www.geonames.org", "license": "Creative Commons Attribution 4.0 (CC BY 4.0)",
                "description": "Geographical database covering all countries with over 11 million placenames that are available for download free of charge."
            },
            {
                "name": "World Bank Open Data", "category": "Economic & Demographics",
                "organization": "The World Bank Group",
                "url": "https://data.worldbank.org", "license": "Creative Commons Attribution 4.0 (CC BY 4.0)",
                "description": "Authoritative global economic, population, and development indicators across member countries."
            },
            {
                "name": "International Hydrographic Organization (IHO)", "category": "Marine & Oceans",
                "organization": "IHO Secretariat (Monaco)",
                "url": "https://iho.int", "license": "Open Data / Official Standard (S-23)",
                "description": "Limits of Oceans and Seas (Special Publication S-23) defining global marine boundaries and nomenclature."
            },
            {
                "name": "General Bathymetric Chart of the Oceans (GEBCO)", "category": "Bathymetry & Ocean Depths",
                "organization": "GEBCO / IHO / IOC UNESCO",
                "url": "https://www.gebco.net", "license": "Public Access / Scientific Attribution",
                "description": "Authoritative global terrain models for ocean bathymetry and land elevations."
            }
        ]

        for s in sources:
            if not DataSource.query.filter_by(name=s["name"]).first():
                db.session.add(DataSource(**s))
        
        db.session.commit()

def run_all_seeds(app):
    print("Seeding roles and permissions...")
    seed_roles_and_permissions(app)
    print("Seeding continents...")
    seed_continents(app)
    print("Seeding oceans...")
    seed_oceans(app)
    print("Seeding seas...")
    seed_seas(app)
    print("Seeding countries, capitals, and borders...")
    seed_countries(app)
    print("Seeding administrative divisions...")
    seed_administrative_divisions(app)
    print("Seeding geographic physical features...")
    seed_geographic_features(app)
    print("Seeding data sources & metadata...")
    seed_data_sources(app)
    print("All seed data successfully committed!")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        db.create_all()
        run_all_seeds(app)
