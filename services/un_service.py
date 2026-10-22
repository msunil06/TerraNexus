"""
United Nations (UN) Intelligence & Structure Service
Comprehensive student-friendly intelligence on:
- General Assembly & Secretariat
- P5 Permanent Security Council Members (Veto Power, Nuclear Status, Military Telemetry)
- 10 Non-Permanent / Temporary Security Council Members (Terms & Regional Blocs)
- Specialized UN Agencies & Connected Member Countries (WHO, UNESCO, UNICEF, WTO, IMF, World Bank, IAEA, FAO, UNHCR, WFP, ILO, etc.)
- Active UN Peacekeeping Operations & Live Telemetry
Zero API keys required.
"""

from services.live_data_service import LiveDataService

class UNService:
    """Service providing detailed United Nations structural and military intelligence."""

    @classmethod
    def get_un_overview(cls):
        """Core metadata regarding the United Nations structure."""
        return {
            "name": "United Nations (UN)",
            "official_charter_date": "October 24, 1945 (San Francisco, United States)",
            "headquarters": "New York City, New York, United States (International Territory)",
            "secretary_general": "António Guterres (Portugal)",
            "deputy_secretary_general": "Amina J. Mohammed (Nigeria)",
            "general_assembly_president": "Philémon Yang (Cameroon)",
            "official_languages": ["Arabic", "Chinese", "English", "French", "Russian", "Spanish"],
            "total_members": 193,
            "observer_states": ["Holy See (Vatican City)", "State of Palestine"],
            "principal_organs": [
                {"name": "General Assembly (UNGA)", "desc": "Main deliberative, policymaking, and representative organ comprising all 193 member states with 1 vote each."},
                {"name": "Security Council (UNSC)", "desc": "Responsible for international peace and security. Comprises 5 permanent members (P5) with veto power and 10 elected non-permanent members."},
                {"name": "Economic and Social Council (ECOSOC)", "desc": "Coordinates the economic, social, and environmental work of 14 UN specialized agencies and functional commissions."},
                {"name": "International Court of Justice (ICJ)", "desc": "The principal judicial organ located in The Hague, Netherlands, settling legal disputes submitted by states."},
                {"name": "Secretariat", "desc": "Carries out the day-to-day work of the UN as mandated by the General Assembly and the other principal organs."}
            ]
        }

    @classmethod
    def get_p5_permanent_members(cls):
        """
        The 5 Permanent Members of the UN Security Council (UNSC).
        Includes veto power, nuclear warheads estimate, military size, defense budget, and live World Bank defense telemetry.
        """
        p5 = [
            {
                "country_name": "United States of America",
                "iso_a3": "USA",
                "iso_a2": "US",
                "flag": "🇺🇸",
                "slug": "united-states",
                "veto_power": True,
                "veto_status": "Permanent Veto Power (Founding 1945)",
                "vetoes_cast_history": 86,
                "nuclear_status": "Recognized Nuclear-Weapon State (NPT P5)",
                "nuclear_warheads": 5244,
                "active_military": 1328000,
                "reserve_military": 799500,
                "defense_budget_usd": "$842.0 Billion",
                "live_military_pct_gdp": 3.4,
                "live_gdp_billions": 27360.0,
                "key_alliance": "NATO (Founding Leader)"
            },
            {
                "country_name": "People's Republic of China",
                "iso_a3": "CHN",
                "iso_a2": "CN",
                "flag": "🇨🇳",
                "slug": "china",
                "veto_power": True,
                "veto_status": "Permanent Veto Power (ROC 1945 / PRC 1971)",
                "vetoes_cast_history": 19,
                "nuclear_status": "Recognized Nuclear-Weapon State (NPT P5)",
                "nuclear_warheads": 500,
                "active_military": 2035000,
                "reserve_military": 510000,
                "defense_budget_usd": "$296.0 Billion",
                "live_military_pct_gdp": 1.6,
                "live_gdp_billions": 17790.0,
                "key_alliance": "BRICS+ / SCO"
            },
            {
                "country_name": "Russian Federation",
                "iso_a3": "RUS",
                "iso_a2": "RU",
                "flag": "🇷🇺",
                "slug": "russia",
                "veto_power": True,
                "veto_status": "Permanent Veto Power (USSR Successor 1991)",
                "vetoes_cast_history": 128,
                "nuclear_status": "Recognized Nuclear-Weapon State (NPT P5)",
                "nuclear_warheads": 5580,
                "active_military": 1320000,
                "reserve_military": 2000000,
                "defense_budget_usd": "$109.0 Billion",
                "live_military_pct_gdp": 5.9,
                "live_gdp_billions": 2020.0,
                "key_alliance": "CSTO / BRICS+"
            },
            {
                "country_name": "United Kingdom",
                "iso_a3": "GBR",
                "iso_a2": "GB",
                "flag": "🇬🇧",
                "slug": "united-kingdom",
                "veto_power": True,
                "veto_status": "Permanent Veto Power (Founding 1945)",
                "vetoes_cast_history": 32,
                "nuclear_status": "Recognized Nuclear-Weapon State (NPT P5)",
                "nuclear_warheads": 225,
                "active_military": 142500,
                "reserve_military": 37000,
                "defense_budget_usd": "$68.5 Billion",
                "live_military_pct_gdp": 2.3,
                "live_gdp_billions": 3340.0,
                "key_alliance": "NATO / G7 / AUKUS"
            },
            {
                "country_name": "French Republic",
                "iso_a3": "FRA",
                "iso_a2": "FR",
                "flag": "🇫🇷",
                "slug": "france",
                "veto_power": True,
                "veto_status": "Permanent Veto Power (Founding 1945)",
                "vetoes_cast_history": 18,
                "nuclear_status": "Recognized Nuclear-Weapon State (NPT P5)",
                "nuclear_warheads": 290,
                "active_military": 203250,
                "reserve_military": 41000,
                "defense_budget_usd": "$53.6 Billion",
                "live_military_pct_gdp": 2.1,
                "live_gdp_billions": 3030.0,
                "key_alliance": "NATO / European Union"
            }
        ]

        return p5

    @classmethod
    def get_temporary_security_council_members(cls):
        """
        The 10 Non-Permanent (Temporary) Members of the UN Security Council.
        Elected by the UN General Assembly for staggered two-year terms based on geographic distribution.
        """
        return [
            {
                "country_name": "Algeria",
                "iso_a3": "DZA",
                "flag": "🇩🇿",
                "slug": "algeria",
                "term_years": "2024–2025",
                "regional_group": "African Group",
                "active_military": 139000,
                "defense_budget_usd": "$21.6 Billion",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Ecuador",
                "iso_a3": "ECU",
                "flag": "🇪🇨",
                "slug": "ecuador",
                "term_years": "2023–2024 / 2025 Transition",
                "regional_group": "Latin American and Caribbean Group (GRULAC)",
                "active_military": 41500,
                "defense_budget_usd": "$2.5 Billion",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Guyana",
                "iso_a3": "GUY",
                "flag": "🇬🇾",
                "slug": "guyana",
                "term_years": "2024–2025",
                "regional_group": "Latin American and Caribbean Group (GRULAC)",
                "active_military": 4600,
                "defense_budget_usd": "$120 Million",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Japan",
                "iso_a3": "JPN",
                "flag": "🇯🇵",
                "slug": "japan",
                "term_years": "2023–2024 / 2025 Transition",
                "regional_group": "Asia-Pacific Group",
                "active_military": 247150,
                "defense_budget_usd": "$54.0 Billion",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Republic of Korea (South Korea)",
                "iso_a3": "KOR",
                "flag": "🇰🇷",
                "slug": "south-korea",
                "term_years": "2024–2025",
                "regional_group": "Asia-Pacific Group",
                "active_military": 500000,
                "defense_budget_usd": "$47.9 Billion",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Malta",
                "iso_a3": "MLT",
                "flag": "🇲🇹",
                "slug": "malta",
                "term_years": "2023–2024 / 2025 Transition",
                "regional_group": "Western European and Others Group (WEOG)",
                "active_military": 1950,
                "defense_budget_usd": "$110 Million",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Mozambique",
                "iso_a3": "MOZ",
                "flag": "🇲🇿",
                "slug": "mozambique",
                "term_years": "2023–2024 / 2025 Transition",
                "regional_group": "African Group",
                "active_military": 11200,
                "defense_budget_usd": "$340 Million",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Sierra Leone",
                "iso_a3": "SLE",
                "flag": "🇸🇱",
                "slug": "sierra-leone",
                "term_years": "2024–2025",
                "regional_group": "African Group",
                "active_military": 8500,
                "defense_budget_usd": "$75 Million",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Slovenia",
                "iso_a3": "SVN",
                "flag": "🇸🇮",
                "slug": "slovenia",
                "term_years": "2024–2025",
                "regional_group": "Eastern European Group",
                "active_military": 7100,
                "defense_budget_usd": "$1.02 Billion",
                "status": "Elected Non-Permanent"
            },
            {
                "country_name": "Switzerland",
                "iso_a3": "CHE",
                "flag": "🇨🇭",
                "slug": "switzerland",
                "term_years": "2023–2024 / 2025 Transition",
                "regional_group": "Western European and Others Group (WEOG)",
                "active_military": 21800,
                "defense_budget_usd": "$6.2 Billion",
                "status": "Elected Non-Permanent"
            }
        ]

    @classmethod
    def get_specialized_agencies(cls):
        """
        All major United Nations Specialized Agencies, Autonomous Bodies, and Programs
        along with their headquarters, connected countries, and student educational briefs.
        """
        return [
            {
                "code": "WHO",
                "name": "World Health Organization",
                "role": "Global Public Health & Pandemic Response",
                "founded": 1948,
                "headquarters": "Geneva, Switzerland",
                "leader": "Tedros Adhanom Ghebreyesus (Director-General)",
                "member_states_count": 194,
                "connected_countries": ["United States", "China", "India", "Germany", "United Kingdom", "Japan", "Brazil", "South Africa", "Nigeria", "France"],
                "badge": "Public Health",
                "desc": "Directs and coordinates international health within the UN system, leading vaccination campaigns, eradicating smallpox, combating malaria, and responding to health emergencies."
            },
            {
                "code": "UNESCO",
                "name": "UN Educational, Scientific and Cultural Organization",
                "role": "Education, World Heritage & Science Preservation",
                "founded": 1945,
                "headquarters": "Paris, France",
                "leader": "Audrey Azoulay (Director-General)",
                "member_states_count": 194,
                "connected_countries": ["France", "Italy", "Spain", "China", "Egypt", "India", "Greece", "Mexico", "United Kingdom", "Japan"],
                "badge": "Culture & Heritage",
                "desc": "Protects over 1,200 World Heritage Sites across the globe, promotes universal literacy, science education, and freedom of expression."
            },
            {
                "code": "UNICEF",
                "name": "United Nations Children's Fund",
                "role": "Child Survival, Nutrition & Emergency Relief",
                "founded": 1946,
                "headquarters": "New York City, United States",
                "leader": "Catherine Russell (Executive Director)",
                "member_states_count": 190,
                "connected_countries": ["United States", "Sweden", "Norway", "United Kingdom", "Germany", "Japan", "Canada", "Australia", "Netherlands", "South Korea"],
                "badge": "Humanitarian",
                "desc": "Provides developmental and humanitarian assistance to children and mothers in over 190 countries and territories."
            },
            {
                "code": "WTO",
                "name": "World Trade Organization",
                "role": "Rules of Global Trade & Dispute Settlement",
                "founded": 1995,
                "headquarters": "Geneva, Switzerland",
                "leader": "Ngozi Okonjo-Iweala (Director-General)",
                "member_states_count": 166,
                "connected_countries": ["United States", "China", "Germany", "Japan", "India", "United Kingdom", "South Korea", "France", "Canada", "Singapore"],
                "badge": "Global Commerce",
                "desc": "Regulates and facilitates international trade between nations, providing a forum for negotiating trade agreements and resolving trade disputes."
            },
            {
                "code": "IMF",
                "name": "International Monetary Fund",
                "role": "Global Financial Stability & Balance of Payments",
                "founded": 1944,
                "headquarters": "Washington, D.C., United States",
                "leader": "Kristalina Georgieva (Managing Director)",
                "member_states_count": 190,
                "connected_countries": ["United States", "Japan", "Germany", "China", "France", "United Kingdom", "Italy", "India", "Saudi Arabia", "Canada"],
                "badge": "Monetary System",
                "desc": "Promotes international monetary cooperation, exchange rate stability, and provides balance-of-payments crisis loans to member nations."
            },
            {
                "code": "World Bank",
                "name": "World Bank Group (IBRD / IDA)",
                "role": "Poverty Eradication & Development Financing",
                "founded": 1944,
                "headquarters": "Washington, D.C., United States",
                "leader": "Ajay Banga (President)",
                "member_states_count": 189,
                "connected_countries": ["United States", "Japan", "China", "Germany", "United Kingdom", "India", "France", "Brazil", "Indonesia", "Nigeria"],
                "badge": "Development",
                "desc": "Provides low-interest loans, zero-to-low-interest credits, and grants to developing countries for infrastructure, health, and economic sustainability."
            },
            {
                "code": "IAEA",
                "name": "International Atomic Energy Agency",
                "role": "Nuclear Non-Proliferation & Peaceful Nuclear Energy",
                "founded": 1957,
                "headquarters": "Vienna, Austria",
                "leader": "Rafael Mariano Grossi (Director-General)",
                "member_states_count": 178,
                "connected_countries": ["United States", "Russia", "France", "China", "United Kingdom", "Iran", "Ukraine", "Japan", "South Korea", "India"],
                "badge": "Nuclear Safeguards",
                "desc": "Autonomous UN body inspecting nuclear facilities worldwide to ensure nuclear technology is not diverted to military purposes, and verifying reactor safety."
            },
            {
                "code": "FAO",
                "name": "Food and Agriculture Organization",
                "role": "Global Food Security, Agriculture & Forestry",
                "founded": 1945,
                "headquarters": "Rome, Italy",
                "leader": "Qu Dongyu (Director-General)",
                "member_states_count": 195,
                "connected_countries": ["Italy", "United States", "Brazil", "China", "India", "Argentina", "Canada", "Australia", "Ukraine", "Indonesia"],
                "badge": "Food Security",
                "desc": "Leads international efforts to defeat hunger, improve agricultural productivity, ensure rural development, and optimize food supply chains."
            },
            {
                "code": "UNHCR",
                "name": "UN High Commissioner for Refugees",
                "role": "Refugee Protection, Asylum & Resettlement",
                "founded": 1950,
                "headquarters": "Geneva, Switzerland",
                "leader": "Filippo Grandi (High Commissioner)",
                "member_states_count": 137,
                "connected_countries": ["Turkey", "Germany", "Pakistan", "Uganda", "Colombia", "Jordan", "Lebanon", "United States", "Poland", "Sudan"],
                "badge": "Refugee Protection",
                "desc": "Twice awarded the Nobel Peace Prize for protecting and supporting displaced people, refugees, and stateless individuals worldwide."
            },
            {
                "code": "WFP",
                "name": "World Food Programme",
                "role": "Emergency Food Assistance & Humanitarian Logistics",
                "founded": 1961,
                "headquarters": "Rome, Italy",
                "leader": "Cindy McCain (Executive Director)",
                "member_states_count": 120,
                "connected_countries": ["United States", "Germany", "United Kingdom", "Japan", "Saudi Arabia", "Canada", "Sweden", "Netherlands", "Norway", "France"],
                "badge": "Hunger Relief",
                "desc": "The world's largest humanitarian organization addressing hunger and promoting food security in conflict zones and disaster areas (2020 Nobel Peace Prize laureate)."
            },
            {
                "code": "ILO",
                "name": "International Labour Organization",
                "role": "International Labor Standards & Workers' Rights",
                "founded": 1919,
                "headquarters": "Geneva, Switzerland",
                "leader": "Gilbert Houngbo (Director-General)",
                "member_states_count": 187,
                "connected_countries": ["Switzerland", "United Kingdom", "United States", "France", "Germany", "India", "Brazil", "Japan", "South Africa", "Australia"],
                "badge": "Labor Rights",
                "desc": "Oldest UN agency (originated in League of Nations) setting international standards for workplace health, elimination of child labor, and equal pay."
            },
            {
                "code": "UNEP",
                "name": "United Nations Environment Programme",
                "role": "Global Environmental Policy, Climate & Biodiversity",
                "founded": 1972,
                "headquarters": "Nairobi, Kenya",
                "leader": "Inger Andersen (Executive Director)",
                "member_states_count": 193,
                "connected_countries": ["Kenya", "United States", "Germany", "Norway", "France", "Brazil", "China", "India", "Japan", "United Kingdom"],
                "badge": "Environment",
                "desc": "Sets the global environmental agenda, coordinates the UN climate treaties, biodiversity conventions, and Montreal Protocol on ozone protection."
            }
        ]

    @classmethod
    def get_peacekeeping_missions(cls):
        """Active UN Peacekeeping Blue Helmet operations across the world."""
        return [
            {
                "acronym": "UNIFIL",
                "name": "UN Interim Force in Lebanon",
                "location": "Southern Lebanon (Blue Line)",
                "established": 1978,
                "personnel": 10500,
                "key_contributors": ["Indonesia", "Italy", "India", "Nepal", "Ghana", "Malaysia", "Spain", "France"]
            },
            {
                "acronym": "MONUSCO",
                "name": "UN Organization Stabilization Mission in DR Congo",
                "location": "Democratic Republic of the Congo",
                "established": 2010,
                "personnel": 12800,
                "key_contributors": ["India", "Pakistan", "Bangladesh", "South Africa", "Nepal", "Uruguay"]
            },
            {
                "acronym": "UNMISS",
                "name": "UN Mission in South Sudan",
                "location": "South Sudan",
                "established": 2011,
                "personnel": 17900,
                "key_contributors": ["Rwanda", "India", "Nepal", "Bangladesh", "Ethiopia", "China"]
            },
            {
                "acronym": "MINUSCA",
                "name": "UN Multidimensional Integrated Stabilization Mission in CAR",
                "location": "Central African Republic",
                "established": 2014,
                "personnel": 14200,
                "key_contributors": ["Rwanda", "Bangladesh", "Pakistan", "Egypt", "Nepal", "Cameroon"]
            },
            {
                "acronym": "UNFICYP",
                "name": "UN Peacekeeping Force in Cyprus",
                "location": "Cyprus (Buffer Zone / Green Line)",
                "established": 1964,
                "personnel": 860,
                "key_contributors": ["Argentina", "United Kingdom", "Slovakia", "Hungary", "Serbia"]
            }
        ]
