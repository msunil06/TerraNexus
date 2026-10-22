"""
World Alliances & Geopolitical Groups Service
Provides rich intelligence on popular world groups for students:
- NATO (32 Nations)
- G7 (Group of Seven)
- BRICS / BRICS+ (10 Nations)
- G20 (Major Global Economies)
- European Union (EU - 27 Nations)
- ASEAN (10 Nations)
- QUAD (Quadrilateral Security Dialogue)
Calculates combined GDP, military personnel, population share, and key educational facts.
Zero API keys required.
"""

from models.geography import Country

class AllianceService:
    """Service to query world alliances and multinational economic/military groups."""

    @classmethod
    def get_all_alliances(cls):
        """Return full catalog of world groups with calculated aggregates and student study guides."""
        alliances = [
            {
                "id": "nato",
                "name": "NATO (North Atlantic Treaty Organization)",
                "type": "Military & Defense Alliance",
                "founded": 1949,
                "headquarters": "Brussels, Belgium",
                "secretary_general": "Mark Rutte",
                "core_treaty": "North Atlantic Treaty (Washington Treaty) - Article 5 Collective Defense",
                "member_count": 32,
                "combined_gdp_trillions": 49.5,
                "combined_military_active": 3400000,
                "global_gdp_share_pct": 47.5,
                "summary": "The premier Euro-Atlantic military alliance founded on the principle that an armed attack against one member is considered an attack against all (Article 5). Recently enlarged to 32 members with the historic accession of Finland (2023) and Sweden (2024).",
                "members": [
                    {"name": "United States", "flag": "🇺🇸", "iso": "USA", "active_troops": 1328000, "gdp_billions": 27360, "joined": 1949},
                    {"name": "United Kingdom", "flag": "🇬🇧", "iso": "GBR", "active_troops": 142500, "gdp_billions": 3340, "joined": 1949},
                    {"name": "France", "flag": "🇫🇷", "iso": "FRA", "active_troops": 203250, "gdp_billions": 3030, "joined": 1949},
                    {"name": "Germany", "flag": "🇩🇪", "iso": "DEU", "active_troops": 181500, "gdp_billions": 4460, "joined": 1955},
                    {"name": "Italy", "flag": "🇮🇹", "iso": "ITA", "active_troops": 165500, "gdp_billions": 2250, "joined": 1949},
                    {"name": "Canada", "flag": "🇨🇦", "iso": "CAN", "active_troops": 68000, "gdp_billions": 2140, "joined": 1949},
                    {"name": "Turkey", "flag": "🇹🇷", "iso": "TUR", "active_troops": 355200, "gdp_billions": 1150, "joined": 1952},
                    {"name": "Poland", "flag": "🇵🇱", "iso": "POL", "active_troops": 202100, "gdp_billions": 842, "joined": 1999},
                    {"name": "Spain", "flag": "🇪🇸", "iso": "ESP", "active_troops": 120000, "gdp_billions": 1580, "joined": 1982},
                    {"name": "Netherlands", "flag": "🇳🇱", "iso": "NLD", "active_troops": 41500, "gdp_billions": 1090, "joined": 1949},
                    {"name": "Norway", "flag": "🇳🇴", "iso": "NOR", "active_troops": 23250, "gdp_billions": 485, "joined": 1949},
                    {"name": "Sweden", "flag": "🇸🇪", "iso": "SWE", "active_troops": 24000, "gdp_billions": 593, "joined": 2024},
                    {"name": "Finland", "flag": "🇫🇮", "iso": "FIN", "active_troops": 21500, "gdp_billions": 300, "joined": 2023},
                    {"name": "Belgium", "flag": "🇧🇪", "iso": "BEL", "active_troops": 25000, "gdp_billions": 632, "joined": 1949},
                    {"name": "Denmark", "flag": "🇩🇰", "iso": "DNK", "active_troops": 15400, "gdp_billions": 404, "joined": 1949},
                    {"name": "Greece", "flag": "🇬🇷", "iso": "GRC", "active_troops": 130000, "gdp_billions": 238, "joined": 1952},
                    {"name": "Portugal", "flag": "🇵🇹", "iso": "PRT", "active_troops": 27200, "gdp_billions": 287, "joined": 1949},
                    {"name": "Czech Republic", "flag": "🇨🇿", "iso": "CZE", "active_troops": 26600, "gdp_billions": 330, "joined": 1999},
                    {"name": "Romania", "flag": "🇷🇴", "iso": "ROU", "active_troops": 67000, "gdp_billions": 351, "joined": 2004},
                    {"name": "Hungary", "flag": "🇭🇺", "iso": "HUN", "active_troops": 37650, "gdp_billions": 212, "joined": 1999}
                ],
                "student_takeaways": [
                    "Article 5 has only been invoked once in NATO history: following the September 11, 2001 terrorist attacks on the United States.",
                    "NATO member states target allocating at least 2.0% of their annual GDP to defense spending.",
                    "NATO features combined air policing over the Baltic and Iceland, and forward presence battle groups across Eastern Europe."
                ]
            },
            {
                "id": "g7",
                "name": "G7 (Group of Seven)",
                "type": "Economic & Democratic Forum",
                "founded": 1975,
                "headquarters": "Rotating Presidency (Annual Summits)",
                "secretary_general": "Presidency rotates annually among members",
                "core_treaty": "Informal Intergovernmental Political Forum of Advanced Economies",
                "member_count": 7,
                "combined_gdp_trillions": 47.1,
                "combined_military_active": 2270000,
                "global_gdp_share_pct": 44.8,
                "summary": "An informal coalition of the world's seven leading advanced industrial democracies, representing over half of global net wealth and key drivers of international financial policies, sanctions, and climate finance.",
                "members": [
                    {"name": "United States", "flag": "🇺🇸", "iso": "USA", "active_troops": 1328000, "gdp_billions": 27360},
                    {"name": "Japan", "flag": "🇯🇵", "iso": "JPN", "active_troops": 247150, "gdp_billions": 4210},
                    {"name": "Germany", "flag": "🇩🇪", "iso": "DEU", "active_troops": 181500, "gdp_billions": 4460},
                    {"name": "United Kingdom", "flag": "🇬🇧", "iso": "GBR", "active_troops": 142500, "gdp_billions": 3340},
                    {"name": "France", "flag": "🇫🇷", "iso": "FRA", "active_troops": 203250, "gdp_billions": 3030},
                    {"name": "Italy", "flag": "🇮🇹", "iso": "ITA", "active_troops": 165500, "gdp_billions": 2250},
                    {"name": "Canada", "flag": "🇨🇦", "iso": "CAN", "active_troops": 68000, "gdp_billions": 2140}
                ],
                "student_takeaways": [
                    "The European Union is also permanently represented at all G7 summit meetings as a non-enumerated member.",
                    "The group was previously called the G8 from 1997 to 2014 when Russia was included, prior to its suspension following the annexation of Crimea.",
                    "G7 ministers coordinate closely on global macroeconomic policy, AI regulation frameworks, and supply chain resiliency."
                ]
            },
            {
                "id": "brics",
                "name": "BRICS & BRICS+ (Emerging Powers)",
                "type": "Geopolitical & Economic Bloc",
                "founded": 2006,
                "headquarters": "New Development Bank (NDB) in Shanghai, China",
                "secretary_general": "Rotating Presidency (Dilma Rousseff heads NDB)",
                "core_treaty": "Fortaleza Declaration & Expanded Johannesburg Declaration",
                "member_count": 10,
                "combined_gdp_trillions": 30.8,
                "combined_military_active": 5400000,
                "global_gdp_share_pct": 36.5,
                "summary": "Originally formed by Brazil, Russia, India, China, and South Africa as the leading emerging economies to challenge Western-dominated Bretton Woods institutions. Expanded in 2024 to include Egypt, Ethiopia, Iran, and the United Arab Emirates.",
                "members": [
                    {"name": "China", "flag": "🇨🇳", "iso": "CHN", "active_troops": 2035000, "gdp_billions": 17790, "joined": 2006},
                    {"name": "India", "flag": "🇮🇳", "iso": "IND", "active_troops": 1455550, "gdp_billions": 3760, "joined": 2006},
                    {"name": "Brazil", "flag": "🇧🇷", "iso": "BRA", "active_troops": 360000, "gdp_billions": 2170, "joined": 2006},
                    {"name": "Russian Federation", "flag": "🇷🇺", "iso": "RUS", "active_troops": 1320000, "gdp_billions": 2020, "joined": 2006},
                    {"name": "South Africa", "flag": "🇿🇦", "iso": "ZAF", "active_troops": 73000, "gdp_billions": 377, "joined": 2010},
                    {"name": "Egypt", "flag": "🇪🇬", "iso": "EGY", "active_troops": 438500, "gdp_billions": 398, "joined": 2024},
                    {"name": "United Arab Emirates", "flag": "🇦🇪", "iso": "ARE", "active_troops": 63000, "gdp_billions": 504, "joined": 2024},
                    {"name": "Iran", "flag": "🇮🇷", "iso": "IRN", "active_troops": 610000, "gdp_billions": 403, "joined": 2024},
                    {"name": "Ethiopia", "flag": "🇪🇹", "iso": "ETH", "active_troops": 162000, "gdp_billions": 163, "joined": 2024},
                    {"name": "Saudi Arabia", "flag": "🇸🇦", "iso": "SAU", "active_troops": 257000, "gdp_billions": 1070, "joined": 2024}
                ],
                "student_takeaways": [
                    "In Purchasing Power Parity (PPP) terms, BRICS+ now accounts for approximately 37% of world GDP, exceeding the G7 (~30%).",
                    "BRICS established the New Development Bank (NDB) and the Contingent Reserve Arrangement (CRA) as alternatives to the World Bank and IMF.",
                    "Members are actively promoting local-currency cross-border settlement mechanisms to reduce reliance on the US Dollar."
                ]
            },
            {
                "id": "g20",
                "name": "G20 (Group of Twenty)",
                "type": "Premier Global Economic Forum",
                "founded": 1999,
                "headquarters": "Rotating Troika Presidency",
                "secretary_general": "Presidency rotates annually across world regions",
                "core_treaty": "G20 Leaders' Declaration on Global Financial Stability & Sustainable Development",
                "member_count": 21,
                "combined_gdp_trillions": 89.2,
                "combined_military_active": 9800000,
                "global_gdp_share_pct": 85.0,
                "summary": "The premier forum for international economic cooperation, comprising 19 sovereign states, the European Union, and the African Union (admitted 2023). Together, G20 members represent 85% of world GDP, 75% of global trade, and two-thirds of the world's population.",
                "members": [
                    {"name": "United States", "flag": "🇺🇸", "iso": "USA", "gdp_billions": 27360},
                    {"name": "China", "flag": "🇨🇳", "iso": "CHN", "gdp_billions": 17790},
                    {"name": "Germany", "flag": "🇩🇪", "iso": "DEU", "gdp_billions": 4460},
                    {"name": "Japan", "flag": "🇯🇵", "iso": "JPN", "gdp_billions": 4210},
                    {"name": "India", "flag": "🇮🇳", "iso": "IND", "gdp_billions": 3760},
                    {"name": "United Kingdom", "flag": "🇬🇧", "iso": "GBR", "gdp_billions": 3340},
                    {"name": "France", "flag": "🇫🇷", "iso": "FRA", "gdp_billions": 3030},
                    {"name": "Italy", "flag": "🇮🇹", "iso": "ITA", "gdp_billions": 2250},
                    {"name": "Brazil", "flag": "🇧🇷", "iso": "BRA", "gdp_billions": 2170},
                    {"name": "Canada", "flag": "🇨🇦", "iso": "CAN", "gdp_billions": 2140},
                    {"name": "Russian Federation", "flag": "🇷🇺", "iso": "RUS", "gdp_billions": 2020},
                    {"name": "Mexico", "flag": "🇲🇽", "iso": "MEX", "gdp_billions": 1790},
                    {"name": "South Korea", "flag": "🇰🇷", "iso": "KOR", "gdp_billions": 1710},
                    {"name": "Australia", "flag": "🇦🇺", "iso": "AUS", "gdp_billions": 1690},
                    {"name": "Indonesia", "flag": "🇮🇩", "iso": "IDN", "gdp_billions": 1370},
                    {"name": "Saudi Arabia", "flag": "🇸🇦", "iso": "SAU", "gdp_billions": 1070},
                    {"name": "Turkey", "flag": "🇹🇷", "iso": "TUR", "gdp_billions": 1150},
                    {"name": "Argentina", "flag": "🇦🇷", "iso": "ARG", "gdp_billions": 640},
                    {"name": "South Africa", "flag": "🇿🇦", "iso": "ZAF", "gdp_billions": 377},
                    {"name": "European Union", "flag": "🇪🇺", "iso": "EU", "gdp_billions": 18500},
                    {"name": "African Union", "flag": "🌍", "iso": "AU", "gdp_billions": 3100}
                ],
                "student_takeaways": [
                    "At the 2023 New Delhi Summit, the African Union (55 member states) was formally admitted as a permanent member of the G20.",
                    "The G20 does not have a permanent staff; its presidency rotates annually supported by the 'Troika' (previous, current, and incoming hosts).",
                    "Major agreements include the global minimum corporate tax rate (15%) and debt suspension frameworks for low-income countries."
                ]
            },
            {
                "id": "eu",
                "name": "European Union (EU)",
                "type": "Economic & Political Supranational Union",
                "founded": 1993,
                "headquarters": "Brussels, Belgium / Strasbourg, France / Luxembourg",
                "secretary_general": "Ursula von der Leyen (Commission) & António Costa (Council)",
                "core_treaty": "Treaty of Maastricht (1993) & Treaty of Lisbon (2009)",
                "member_count": 27,
                "combined_gdp_trillions": 18.5,
                "combined_military_active": 1450000,
                "global_gdp_share_pct": 17.6,
                "summary": "A unique political and economic partnership of 27 democratic European nations that operate an internal single market, free movement of people (Schengen Zone across 29 nations), and the Euro common currency used by 20 member states.",
                "members": [
                    {"name": "Germany", "flag": "🇩🇪", "iso": "DEU", "gdp_billions": 4460},
                    {"name": "France", "flag": "🇫🇷", "iso": "FRA", "gdp_billions": 3030},
                    {"name": "Italy", "flag": "🇮🇹", "iso": "ITA", "gdp_billions": 2250},
                    {"name": "Spain", "flag": "🇪🇸", "iso": "ESP", "gdp_billions": 1580},
                    {"name": "Netherlands", "flag": "🇳🇱", "iso": "NLD", "gdp_billions": 1090},
                    {"name": "Poland", "flag": "🇵🇱", "iso": "POL", "gdp_billions": 842},
                    {"name": "Belgium", "flag": "🇧🇪", "iso": "BEL", "gdp_billions": 632},
                    {"name": "Sweden", "flag": "🇸🇪", "iso": "SWE", "gdp_billions": 593},
                    {"name": "Ireland", "flag": "🇮🇪", "iso": "IRL", "gdp_billions": 546},
                    {"name": "Austria", "flag": "🇦🇹", "iso": "AUT", "gdp_billions": 516}
                ],
                "student_takeaways": [
                    "The four fundamental freedoms of the EU single market are the free movement of goods, services, capital, and persons.",
                    "The Schengen Area allows 450 million citizens to travel border-control-free between 29 European countries.",
                    "The European Central Bank (ECB) in Frankfurt manages monetary policy for the 20 nations of the Eurozone."
                ]
            },
            {
                "id": "asean",
                "name": "ASEAN (Association of Southeast Asian Nations)",
                "type": "Regional Economic & Political Integration",
                "founded": 1967,
                "headquarters": "Jakarta, Indonesia",
                "secretary_general": "Kao Kim Hourn (Cambodia)",
                "core_treaty": "ASEAN Declaration (Bangkok Declaration) & ASEAN Charter",
                "member_count": 10,
                "combined_gdp_trillions": 3.8,
                "combined_military_active": 1980000,
                "global_gdp_share_pct": 3.7,
                "summary": "An intergovernmental organization of ten Southeast Asian nations established to promote economic growth, social progress, regional peace, and neutrality in the Indo-Pacific region.",
                "members": [
                    {"name": "Indonesia", "flag": "🇮🇩", "iso": "IDN", "active_troops": 400000, "gdp_billions": 1370},
                    {"name": "Thailand", "flag": "🇹🇭", "iso": "THA", "active_troops": 360000, "gdp_billions": 512},
                    {"name": "Singapore", "flag": "🇸🇬", "iso": "SGP", "active_troops": 72000, "gdp_billions": 501},
                    {"name": "Malaysia", "flag": "🇲🇾", "iso": "MYS", "active_troops": 113000, "gdp_billions": 439},
                    {"name": "Vietnam", "flag": "🇻🇳", "iso": "VNM", "active_troops": 482000, "gdp_billions": 433},
                    {"name": "Philippines", "flag": "🇵🇭", "iso": "PHL", "active_troops": 143000, "gdp_billions": 436},
                    {"name": "Myanmar", "flag": "🇲🇲", "iso": "MMR", "active_troops": 350000, "gdp_billions": 65},
                    {"name": "Cambodia", "flag": "🇰🇭", "iso": "KHM", "active_troops": 125000, "gdp_billions": 32},
                    {"name": "Brunei", "flag": "🇧🇳", "iso": "BRN", "active_troops": 7200, "gdp_billions": 16},
                    {"name": "Laos", "flag": "🇱🇦", "iso": "LAO", "active_troops": 30000, "gdp_billions": 15}
                ],
                "student_takeaways": [
                    "The 'ASEAN Way' emphasizes non-interference in internal affairs, consensus-based decision making, and quiet diplomacy.",
                    "ASEAN anchors the Regional Comprehensive Economic Partnership (RCEP), the world's largest free trade agreement covering 30% of global GDP.",
                    "Timor-Leste was granted observer status in 2022 and is on track for full member accession."
                ]
            },
            {
                "id": "quad",
                "name": "QUAD (Quadrilateral Security Dialogue)",
                "type": "Strategic Indo-Pacific Partnership",
                "founded": 2007,
                "headquarters": "Rotational Summits (Canberra, Tokyo, New Delhi, Washington)",
                "secretary_general": "Consultative Partnership between 4 Sovereign Governments",
                "core_treaty": "Free and Open Indo-Pacific (FOIP) Joint Statement",
                "member_count": 4,
                "combined_gdp_trillions": 37.0,
                "combined_military_active": 3080000,
                "global_gdp_share_pct": 35.2,
                "summary": "A strategic diplomatic network between Australia, India, Japan, and the United States dedicated to supporting an open, stable, and prosperous Indo-Pacific region, maritime domain awareness, critical technologies, and humanitarian disaster relief.",
                "members": [
                    {"name": "United States", "flag": "🇺🇸", "iso": "USA", "active_troops": 1328000, "gdp_billions": 27360},
                    {"name": "India", "flag": "🇮🇳", "iso": "IND", "active_troops": 1455550, "gdp_billions": 3760},
                    {"name": "Japan", "flag": "🇯🇵", "iso": "JPN", "active_troops": 247150, "gdp_billions": 4210},
                    {"name": "Australia", "flag": "🇦🇺", "iso": "AUS", "active_troops": 57350, "gdp_billions": 1690}
                ],
                "student_takeaways": [
                    "The QUAD conducts annual Malabar joint naval exercises across the Indian Ocean and Philippine Sea.",
                    "Focuses heavily on non-military public goods: the Indo-Pacific Partnership for Maritime Domain Awareness (IPMDA), clean energy supply chains, and vaccine delivery.",
                    "Not a formal military alliance like NATO (there is no mutual defense treaty clause), but a minilateral strategic partnership."
                ]
            }
        ]

        # Link country slugs from database where possible
        for a in alliances:
            for m in a["members"]:
                iso = m.get("iso")
                if iso:
                    c = Country.query.filter_by(iso_a3=iso).first()
                    if c:
                        m["slug"] = c.slug
                        m["flag"] = c.flag_emoji or m["flag"]

        return alliances

    @classmethod
    def get_alliance_by_id(cls, alliance_id):
        """Retrieve a specific alliance profile by slug/id."""
        all_alliances = cls.get_all_alliances()
        for a in all_alliances:
            if a["id"].lower() == alliance_id.lower():
                return a
        return None
