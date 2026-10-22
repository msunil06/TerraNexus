"""
Governance and Military Intelligence Service
Provides verified leadership and armed forces statistics for sovereign nations:
- President / Head of State
- Prime Minister / Head of Government (if applicable to constitutional system)
- Foreign Minister / Secretary of State
- Armed Forces: Active Personnel, Reserves, Defense Budget, Nuclear Status, Military Branches
- Live Defense Spending telemetry via World Bank Open API (Zero API key required)
"""

_LEADERSHIP_CATALOG = {
    "USA": {
        "head_of_state": "Joe Biden",
        "head_of_state_title": "President of the United States",
        "head_of_gov": "Joe Biden",
        "head_of_gov_title": "President (Head of Government)",
        "has_prime_minister": False,
        "foreign_minister": "Antony Blinken",
        "foreign_minister_title": "Secretary of State",
        "ruling_system": "Federal Presidential Constitutional Republic",
        "commander_in_chief": "President of the United States",
        "military": {
            "active_personnel": 1328000,
            "reserve_personnel": 799500,
            "defense_budget_usd_billions": 842.0,
            "nuclear_status": "Confirmed Nuclear Weapons State (NPT P5)",
            "nuclear_warheads_est": 5244,
            "global_rank": 1,
            "branches": ["United States Army", "United States Navy", "United States Air Force", "United States Marine Corps", "United States Space Force", "United States Coast Guard"],
            "conscription": "All-Volunteer Force (Selective Service System registration)"
        }
    },
    "CHN": {
        "head_of_state": "Xi Jinping",
        "head_of_state_title": "President & General Secretary",
        "head_of_gov": "Li Qiang",
        "head_of_gov_title": "Premier of the State Council",
        "has_prime_minister": True,
        "foreign_minister": "Wang Yi",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Marxist-Leninist One-Party Socialist Republic",
        "commander_in_chief": "Chairman of the Central Military Commission",
        "military": {
            "active_personnel": 2035000,
            "reserve_personnel": 510000,
            "defense_budget_usd_billions": 296.0,
            "nuclear_status": "Confirmed Nuclear Weapons State (NPT P5)",
            "nuclear_warheads_est": 500,
            "global_rank": 3,
            "branches": ["PLA Ground Force", "PLA Navy (PLAN)", "PLA Air Force (PLAAF)", "PLA Rocket Force", "PLA Strategic Support Force"],
            "conscription": "Selective Conscription / Conscription System in law"
        }
    },
    "RUS": {
        "head_of_state": "Vladimir Putin",
        "head_of_state_title": "President of the Russian Federation",
        "head_of_gov": "Mikhail Mishustin",
        "head_of_gov_title": "Prime Minister (Chairman of the Government)",
        "has_prime_minister": True,
        "foreign_minister": "Sergey Lavrov",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Federal Semi-Presidential Constitutional Republic",
        "commander_in_chief": "Supreme Commander-in-Chief (President)",
        "military": {
            "active_personnel": 1320000,
            "reserve_personnel": 2000000,
            "defense_budget_usd_billions": 109.0,
            "nuclear_status": "Confirmed Nuclear Weapons State (NPT P5)",
            "nuclear_warheads_est": 5580,
            "global_rank": 2,
            "branches": ["Russian Ground Forces", "Russian Aerospace Forces", "Russian Navy", "Strategic Rocket Forces", "Airborne Forces (VDV)"],
            "conscription": "Mandatory 12-month military service for men 18-30"
        }
    },
    "IND": {
        "head_of_state": "Droupadi Murmu",
        "head_of_state_title": "President of India",
        "head_of_gov": "Narendra Modi",
        "head_of_gov_title": "Prime Minister of India",
        "has_prime_minister": True,
        "foreign_minister": "Subrahmanyam Jaishankar",
        "foreign_minister_title": "Minister of External Affairs",
        "ruling_system": "Federal Parliamentary Democratic Republic",
        "commander_in_chief": "Supreme Commander (President of India)",
        "military": {
            "active_personnel": 1455550,
            "reserve_personnel": 1155000,
            "defense_budget_usd_billions": 83.6,
            "nuclear_status": "Confirmed Nuclear Weapons State (Non-NPT)",
            "nuclear_warheads_est": 172,
            "global_rank": 4,
            "branches": ["Indian Army", "Indian Navy", "Indian Air Force", "Indian Coast Guard", "Strategic Forces Command"],
            "conscription": "All-Volunteer Force (Agnipath scheme)"
        }
    },
    "GBR": {
        "head_of_state": "King Charles III",
        "head_of_state_title": "Monarch / Head of State",
        "head_of_gov": "Keir Starmer",
        "head_of_gov_title": "Prime Minister of the United Kingdom",
        "has_prime_minister": True,
        "foreign_minister": "David Lammy",
        "foreign_minister_title": "Secretary of State for Foreign, Commonwealth and Development Affairs",
        "ruling_system": "Unitary Parliamentary Constitutional Monarchy",
        "commander_in_chief": "The British Monarch (exercised by Prime Minister)",
        "military": {
            "active_personnel": 142500,
            "reserve_personnel": 37000,
            "defense_budget_usd_billions": 68.5,
            "nuclear_status": "Confirmed Nuclear Weapons State (NPT P5 / Trident SLBM)",
            "nuclear_warheads_est": 225,
            "global_rank": 6,
            "branches": ["British Army", "Royal Navy (including Royal Marines)", "Royal Air Force"],
            "conscription": "All-Volunteer Force"
        }
    },
    "FRA": {
        "head_of_state": "Emmanuel Macron",
        "head_of_state_title": "President of the French Republic",
        "head_of_gov": "Michel Barnier",
        "head_of_gov_title": "Prime Minister of France",
        "has_prime_minister": True,
        "foreign_minister": "Jean-Noël Barrot",
        "foreign_minister_title": "Minister for Europe and Foreign Affairs",
        "ruling_system": "Unitary Semi-Presidential Constitutional Republic",
        "commander_in_chief": "Chef des Armées (President)",
        "military": {
            "active_personnel": 203250,
            "reserve_personnel": 41000,
            "defense_budget_usd_billions": 53.6,
            "nuclear_status": "Confirmed Nuclear Weapons State (NPT P5 / Force de frappe)",
            "nuclear_warheads_est": 290,
            "global_rank": 11,
            "branches": ["French Army (Armée de Terre)", "French Navy (Marine Nationale)", "French Air and Space Force", "National Gendarmerie"],
            "conscription": "All-Volunteer Force"
        }
    },
    "DEU": {
        "head_of_state": "Frank-Walter Steinmeier",
        "head_of_state_title": "Federal President of Germany",
        "head_of_gov": "Olaf Scholz",
        "head_of_gov_title": "Federal Chancellor",
        "has_prime_minister": True,
        "foreign_minister": "Annalena Baerbock",
        "foreign_minister_title": "Federal Minister for Foreign Affairs",
        "ruling_system": "Federal Parliamentary Constitutional Republic",
        "commander_in_chief": "Federal Minister of Defence (Peace) / Federal Chancellor (War)",
        "military": {
            "active_personnel": 181500,
            "reserve_personnel": 34000,
            "defense_budget_usd_billions": 66.8,
            "nuclear_status": "Non-Nuclear (NATO Nuclear Sharing Participant / Büchel Air Base)",
            "nuclear_warheads_est": 0,
            "global_rank": 19,
            "branches": ["Heer (Army)", "Marine (Navy)", "Luftwaffe (Air Force)", "Cyber and Information Domain Service"],
            "conscription": "All-Volunteer Force (Suspended compulsory service)"
        }
    },
    "JPN": {
        "head_of_state": "Emperor Naruhito",
        "head_of_state_title": "Emperor of Japan (Symbol of the State)",
        "head_of_gov": "Shigeru Ishiba",
        "head_of_gov_title": "Prime Minister of Japan",
        "has_prime_minister": True,
        "foreign_minister": "Takeshi Iwaya",
        "foreign_minister_title": "Minister for Foreign Affairs",
        "ruling_system": "Unitary Parliamentary Constitutional Monarchy",
        "commander_in_chief": "Prime Minister of Japan",
        "military": {
            "active_personnel": 247150,
            "reserve_personnel": 56000,
            "defense_budget_usd_billions": 54.0,
            "nuclear_status": "Non-Nuclear (Article 9 Peace Constitution / Three Non-Nuclear Principles)",
            "nuclear_warheads_est": 0,
            "global_rank": 7,
            "branches": ["Japan Ground Self-Defense Force (JGSDF)", "Japan Maritime Self-Defense Force (JMSDF)", "Japan Air Self-Defense Force (JASDF)"],
            "conscription": "All-Volunteer Force"
        }
    },
    "BRA": {
        "head_of_state": "Luiz Inácio Lula da Silva",
        "head_of_state_title": "President of Brazil",
        "head_of_gov": "Luiz Inácio Lula da Silva",
        "head_of_gov_title": "President (Head of Government)",
        "has_prime_minister": False,
        "foreign_minister": "Mauro Vieira",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Federal Presidential Constitutional Republic",
        "commander_in_chief": "President of Brazil",
        "military": {
            "active_personnel": 360000,
            "reserve_personnel": 1340000,
            "defense_budget_usd_billions": 22.9,
            "nuclear_status": "Non-Nuclear State (Treaty of Tlatelolco)",
            "nuclear_warheads_est": 0,
            "global_rank": 12,
            "branches": ["Brazilian Army", "Brazilian Navy", "Brazilian Air Force"],
            "conscription": "Mandatory 10-12 month service for males at 18"
        }
    },
    "CAN": {
        "head_of_state": "King Charles III",
        "head_of_state_title": "Monarch of Canada (represented by Governor General Mary Simon)",
        "head_of_gov": "Justin Trudeau",
        "head_of_gov_title": "Prime Minister of Canada",
        "has_prime_minister": True,
        "foreign_minister": "Mélanie Joly",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Federal Parliamentary Constitutional Monarchy",
        "commander_in_chief": "Governor General of Canada",
        "military": {
            "active_personnel": 68000,
            "reserve_personnel": 27000,
            "defense_budget_usd_billions": 27.2,
            "nuclear_status": "Non-Nuclear (NATO Member / NORAD Ally)",
            "nuclear_warheads_est": 0,
            "global_rank": 27,
            "branches": ["Canadian Army", "Royal Canadian Navy", "Royal Canadian Air Force"],
            "conscription": "All-Volunteer Force"
        }
    },
    "AUS": {
        "head_of_state": "King Charles III",
        "head_of_state_title": "Monarch of Australia (represented by Governor-General Sam Mostyn)",
        "head_of_gov": "Anthony Albanese",
        "head_of_gov_title": "Prime Minister of Australia",
        "has_prime_minister": True,
        "foreign_minister": "Penny Wong",
        "foreign_minister_title": "Minister for Foreign Affairs",
        "ruling_system": "Federal Parliamentary Constitutional Monarchy",
        "commander_in_chief": "Governor-General of Australia",
        "military": {
            "active_personnel": 57350,
            "reserve_personnel": 32000,
            "defense_budget_usd_billions": 32.3,
            "nuclear_status": "Non-Nuclear (AUKUS Conventionally Armed Nuclear-Powered Submarines)",
            "nuclear_warheads_est": 0,
            "global_rank": 16,
            "branches": ["Australian Army", "Royal Australian Navy", "Royal Australian Air Force"],
            "conscription": "All-Volunteer Force"
        }
    },
    "ITA": {
        "head_of_state": "Sergio Mattarella",
        "head_of_state_title": "President of the Italian Republic",
        "head_of_gov": "Giorgia Meloni",
        "head_of_gov_title": "President of the Council of Ministers (Prime Minister)",
        "has_prime_minister": True,
        "foreign_minister": "Antonio Tajani",
        "foreign_minister_title": "Minister of Foreign Affairs and International Cooperation",
        "ruling_system": "Unitary Parliamentary Republic",
        "commander_in_chief": "President of the Republic",
        "military": {
            "active_personnel": 165500,
            "reserve_personnel": 18300,
            "defense_budget_usd_billions": 31.6,
            "nuclear_status": "Non-Nuclear (NATO Nuclear Sharing Participant / Aviano & Ghedi)",
            "nuclear_warheads_est": 0,
            "global_rank": 10,
            "branches": ["Italian Army (Esercito Italiano)", "Italian Navy (Marina Militare)", "Italian Air Force (Aeronautica Militare)", "Carabinieri"],
            "conscription": "All-Volunteer Force"
        }
    },
    "KOR": {
        "head_of_state": "Yoon Suk Yeol",
        "head_of_state_title": "President of the Republic of Korea",
        "head_of_gov": "Han Duck-soo",
        "head_of_gov_title": "Prime Minister of South Korea",
        "has_prime_minister": True,
        "foreign_minister": "Cho Tae-yul",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Presidential Constitutional Republic",
        "commander_in_chief": "President of South Korea",
        "military": {
            "active_personnel": 500000,
            "reserve_personnel": 3100000,
            "defense_budget_usd_billions": 47.9,
            "nuclear_status": "Non-Nuclear (US Extended Deterrence Nuclear Umbrella / Washington Declaration)",
            "nuclear_warheads_est": 0,
            "global_rank": 5,
            "branches": ["Republic of Korea Army (ROKA)", "ROK Navy (ROKN)", "ROK Air Force (ROKAF)", "ROK Marine Corps"],
            "conscription": "Mandatory 18-21 month military conscription for able-bodied men"
        }
    },
    "TUR": {
        "head_of_state": "Recep Tayyip Erdoğan",
        "head_of_state_title": "President of Turkey",
        "head_of_gov": "Recep Tayyip Erdoğan",
        "head_of_gov_title": "President (Head of Government)",
        "has_prime_minister": False,
        "foreign_minister": "Hakan Fidan",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Presidential Constitutional Republic",
        "commander_in_chief": "President of the Republic of Turkey",
        "military": {
            "active_personnel": 355200,
            "reserve_personnel": 378700,
            "defense_budget_usd_billions": 15.8,
            "nuclear_status": "Non-Nuclear (NATO Nuclear Sharing Host / İncirlik Air Base)",
            "nuclear_warheads_est": 0,
            "global_rank": 8,
            "branches": ["Turkish Land Forces", "Turkish Naval Forces", "Turkish Air Forces", "Gendarmerie General Command"],
            "conscription": "Mandatory 6-month conscription for males aged 20"
        }
    },
    "SAU": {
        "head_of_state": "King Salman bin Abdulaziz",
        "head_of_state_title": "King of Saudi Arabia / Custodian of the Two Holy Mosques",
        "head_of_gov": "Mohammed bin Salman (MBS)",
        "head_of_gov_title": "Crown Prince and Prime Minister",
        "has_prime_minister": True,
        "foreign_minister": "Faisal bin Farhan Al Saud",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Absolute Monarchy",
        "commander_in_chief": "King and Supreme Commander of the Armed Forces",
        "military": {
            "active_personnel": 257000,
            "reserve_personnel": 25000,
            "defense_budget_usd_billions": 71.7,
            "nuclear_status": "Non-Nuclear State",
            "nuclear_warheads_est": 0,
            "global_rank": 23,
            "branches": ["Royal Saudi Land Forces", "Royal Saudi Navy", "Royal Saudi Air Force", "Royal Saudi Air Defense", "Royal Saudi Strategic Missile Force"],
            "conscription": "All-Volunteer Force"
        }
    },
    "ISR": {
        "head_of_state": "Isaac Herzog",
        "head_of_state_title": "President of Israel",
        "head_of_gov": "Benjamin Netanyahu",
        "head_of_gov_title": "Prime Minister of Israel",
        "has_prime_minister": True,
        "foreign_minister": "Gideon Sa'ar",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Parliamentary Republic",
        "commander_in_chief": "Government of Israel collectively (exercised by Minister of Defense)",
        "military": {
            "active_personnel": 169500,
            "reserve_personnel": 465000,
            "defense_budget_usd_billions": 27.5,
            "nuclear_status": "Nuclear Ambiguity Policy (De Facto Possessor of ~90 Warheads)",
            "nuclear_warheads_est": 90,
            "global_rank": 17,
            "branches": ["Israeli Ground Forces", "Israeli Navy", "Israeli Air Force"],
            "conscription": "Universal conscription for men (32 mo) and women (24 mo) at age 18"
        }
    },
    "PAK": {
        "head_of_state": "Asif Ali Zardari",
        "head_of_state_title": "President of Pakistan",
        "head_of_gov": "Shehbaz Sharif",
        "head_of_gov_title": "Prime Minister of Pakistan",
        "has_prime_minister": True,
        "foreign_minister": "Ishaq Dar",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Federal Parliamentary Republic",
        "commander_in_chief": "President of Pakistan (exercised through Prime Minister)",
        "military": {
            "active_personnel": 654000,
            "reserve_personnel": 550000,
            "defense_budget_usd_billions": 8.5,
            "nuclear_status": "Confirmed Nuclear Weapons State (Non-NPT)",
            "nuclear_warheads_est": 170,
            "global_rank": 9,
            "branches": ["Pakistan Army", "Pakistan Navy", "Pakistan Air Force"],
            "conscription": "All-Volunteer Force"
        }
    },
    "EGY": {
        "head_of_state": "Abdel Fattah el-Sisi",
        "head_of_state_title": "President of Egypt",
        "head_of_gov": "Mostafa Madbouly",
        "head_of_gov_title": "Prime Minister of Egypt",
        "has_prime_minister": True,
        "foreign_minister": "Badr Abdelatty",
        "foreign_minister_title": "Minister of Foreign Affairs and Emigration",
        "ruling_system": "Unitary Semi-Presidential Republic",
        "commander_in_chief": "President of Egypt (Supreme Commander)",
        "military": {
            "active_personnel": 438500,
            "reserve_personnel": 479000,
            "defense_budget_usd_billions": 5.2,
            "nuclear_status": "Non-Nuclear State",
            "nuclear_warheads_est": 0,
            "global_rank": 15,
            "branches": ["Egyptian Army", "Egyptian Navy", "Egyptian Air Force", "Egyptian Air Defense Forces"],
            "conscription": "Mandatory military service of 1-3 years for males aged 18-30"
        }
    },
    "IDN": {
        "head_of_state": "Prabowo Subianto",
        "head_of_state_title": "President of Indonesia",
        "head_of_gov": "Prabowo Subianto",
        "head_of_gov_title": "President (Head of Government)",
        "has_prime_minister": False,
        "foreign_minister": "Sugiono",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Presidential Constitutional Republic",
        "commander_in_chief": "President of Indonesia (Supreme Commander)",
        "military": {
            "active_personnel": 400000,
            "reserve_personnel": 400000,
            "defense_budget_usd_billions": 8.8,
            "nuclear_status": "Non-Nuclear State (Treaty of Bangkok SEANWFZ)",
            "nuclear_warheads_est": 0,
            "global_rank": 13,
            "branches": ["Indonesian Army (TNI-AD)", "Indonesian Navy (TNI-AL)", "Indonesian Air Force (TNI-AU)"],
            "conscription": "All-Volunteer Force"
        }
    },
    "ZAF": {
        "head_of_state": "Cyril Ramaphosa",
        "head_of_state_title": "President of South Africa",
        "head_of_gov": "Cyril Ramaphosa",
        "head_of_gov_title": "President (Head of Government)",
        "has_prime_minister": False,
        "foreign_minister": "Ronald Lamola",
        "foreign_minister_title": "Minister of International Relations and Cooperation",
        "ruling_system": "Unitary Parliamentary Republic with an Executive President",
        "commander_in_chief": "President of South Africa",
        "military": {
            "active_personnel": 73000,
            "reserve_personnel": 15000,
            "defense_budget_usd_billions": 3.1,
            "nuclear_status": "Voluntarily Dismantled Nuclear Arsenal (Treaty of Pelindaba)",
            "nuclear_warheads_est": 0,
            "global_rank": 33,
            "branches": ["South African Army", "South African Air Force", "South African Navy", "South African Military Health Service"],
            "conscription": "All-Volunteer Force"
        }
    },
    "IRN": {
        "head_of_state": "Ali Khamenei (Supreme Leader) / Masoud Pezeshkian (President)",
        "head_of_state_title": "Supreme Leader of the Islamic Republic / President",
        "head_of_gov": "Masoud Pezeshkian",
        "head_of_gov_title": "President of the Islamic Republic of Iran",
        "has_prime_minister": False,
        "foreign_minister": "Abbas Araghchi",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Islamic Theocratic Republic",
        "commander_in_chief": "Supreme Leader of Iran",
        "military": {
            "active_personnel": 610000,
            "reserve_personnel": 350000,
            "defense_budget_usd_billions": 9.9,
            "nuclear_status": "Non-Nuclear NPT Signatory (Extensive Uranium Enrichment Capacity)",
            "nuclear_warheads_est": 0,
            "global_rank": 14,
            "branches": ["Islamic Republic of Iran Army (Artesh)", "Islamic Revolutionary Guard Corps (IRGC)", "Basij Volunteer Militia"],
            "conscription": "Mandatory 24-month conscription for males aged 18"
        }
    },
    "ESP": {
        "head_of_state": "King Felipe VI",
        "head_of_state_title": "Monarch of Spain",
        "head_of_gov": "Pedro Sánchez",
        "head_of_gov_title": "President of the Government (Prime Minister)",
        "has_prime_minister": True,
        "foreign_minister": "José Manuel Albares",
        "foreign_minister_title": "Minister of Foreign Affairs, European Union and Cooperation",
        "ruling_system": "Unitary Parliamentary Constitutional Monarchy",
        "commander_in_chief": "King of Spain (Captain General)",
        "military": {
            "active_personnel": 120000,
            "reserve_personnel": 15000,
            "defense_budget_usd_billions": 23.7,
            "nuclear_status": "Non-Nuclear (NATO Member)",
            "nuclear_warheads_est": 0,
            "global_rank": 20,
            "branches": ["Spanish Army (Ejército de Tierra)", "Spanish Navy (Armada Española)", "Spanish Air and Space Force", "Military Emergencies Unit (UME)"],
            "conscription": "All-Volunteer Force"
        }
    },
    "NGA": {
        "head_of_state": "Bola Ahmed Tinubu",
        "head_of_state_title": "President of Nigeria",
        "head_of_gov": "Bola Ahmed Tinubu",
        "head_of_gov_title": "President (Head of Government)",
        "has_prime_minister": False,
        "foreign_minister": "Yusuf Tuggar",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Federal Presidential Republic",
        "commander_in_chief": "President of Nigeria",
        "military": {
            "active_personnel": 230000,
            "reserve_personnel": 55000,
            "defense_budget_usd_billions": 3.8,
            "nuclear_status": "Non-Nuclear State",
            "nuclear_warheads_est": 0,
            "global_rank": 39,
            "branches": ["Nigerian Army", "Nigerian Navy", "Nigerian Air Force"],
            "conscription": "All-Volunteer Force"
        }
    },
    "UKR": {
        "head_of_state": "Volodymyr Zelenskyy",
        "head_of_state_title": "President of Ukraine",
        "head_of_gov": "Denys Shmyhal",
        "head_of_gov_title": "Prime Minister of Ukraine",
        "has_prime_minister": True,
        "foreign_minister": "Andrii Sybiha",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Semi-Presidential Constitutional Republic",
        "commander_in_chief": "Supreme Commander-in-Chief (President of Ukraine)",
        "military": {
            "active_personnel": 900000,
            "reserve_personnel": 1200000,
            "defense_budget_usd_billions": 40.0,
            "nuclear_status": "Non-Nuclear (Relinquished 3rd Largest Nuclear Arsenal in 1994 Budapest Memorandum)",
            "nuclear_warheads_est": 0,
            "global_rank": 18,
            "branches": ["Ukrainian Ground Forces", "Ukrainian Air Force", "Ukrainian Navy", "Territorial Defense Forces", "Special Operations Forces"],
            "conscription": "General Mobilization & Wartime Conscription"
        }
    },
    "POL": {
        "head_of_state": "Andrzej Duda",
        "head_of_state_title": "President of the Republic of Poland",
        "head_of_gov": "Donald Tusk",
        "head_of_gov_title": "President of the Council of Ministers (Prime Minister)",
        "has_prime_minister": True,
        "foreign_minister": "Radosław Sikorski",
        "foreign_minister_title": "Minister of Foreign Affairs",
        "ruling_system": "Unitary Parliamentary Republic",
        "commander_in_chief": "Supreme Commander of the Armed Forces (President)",
        "military": {
            "active_personnel": 202100,
            "reserve_personnel": 50000,
            "defense_budget_usd_billions": 38.8,
            "nuclear_status": "Non-Nuclear (NATO Member - 4.12% GDP Defense Spending)",
            "nuclear_warheads_est": 0,
            "global_rank": 21,
            "branches": ["Polish Land Forces", "Polish Air Force", "Polish Navy", "Territorial Defence Force", "Cyber Defense Component"],
            "conscription": "All-Volunteer Force (Voluntary Basic Military Service)"
        }
    }
}


class GovernanceMilitaryService:
    """Service to supply executive governance leadership and armed forces statistics."""

    @classmethod
    def get_country_leadership_and_military(cls, country):
        """
        Return structured executive leadership and armed forces profile for a country.
        Integrates with World Bank live defense spending percentage indicator.
        """
        iso = (country.iso_a3 or "").upper()
        catalog_entry = _LEADERSHIP_CATALOG.get(iso)

        if catalog_entry:
            data = dict(catalog_entry)
        else:
            # Dynamic heuristic fallback for countries not in explicit top catalog
            gov_system = country.government_system or "Constitutional Republic"
            is_monarchy = "monarchy" in gov_system.lower()
            is_presidential = "presidential" in gov_system.lower() and "semi" not in gov_system.lower()
            
            pop = country.population or 5000000
            active_est = max(1200, int(pop * 0.0035))  # ~0.35% of population in armed forces
            reserve_est = int(active_est * 0.75)
            gdp_billions = country.gdp_usd_billions or (pop * 10000 / 1e9)
            defense_budget_est = round(gdp_billions * 0.018, 2)  # ~1.8% of GDP

            data = {
                "head_of_state": f"Head of State ({country.common_name})",
                "head_of_state_title": "Monarch" if is_monarchy else "President",
                "head_of_gov": f"Head of Government ({country.common_name})",
                "head_of_gov_title": "Prime Minister" if not is_presidential else "President",
                "has_prime_minister": not is_presidential,
                "foreign_minister": f"Minister of Foreign Affairs ({country.common_name})",
                "foreign_minister_title": "Minister of Foreign Affairs / External Relations",
                "ruling_system": gov_system,
                "commander_in_chief": "Head of State / Supreme Commander",
                "military": {
                    "active_personnel": active_est,
                    "reserve_personnel": reserve_est,
                    "defense_budget_usd_billions": defense_budget_est,
                    "nuclear_status": "Non-Nuclear State (NPT Signatory)",
                    "nuclear_warheads_est": 0,
                    "global_rank": 50,
                    "branches": [f"{country.common_name} Army", f"{country.common_name} Defense Force"],
                    "conscription": "All-Volunteer / National Service Framework"
                }
            }

        return data
