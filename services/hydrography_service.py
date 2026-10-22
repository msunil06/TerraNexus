"""
Hydrography & Border Connectivity Service
Provides comprehensive data for:
- All land border sharing countries ranked by border length (longest border priority first).
- Connected oceans (Pacific, Atlantic, Indian, Arctic, Southern, or Landlocked).
- Connected marginal seas, gulfs, and straits.
- Connected major rivers flowing through or bordering each country.
- Sea-to-littoral coastal states connectivity.
Zero API keys required.
"""

# Global Comprehensive Hydrography & River Catalog
_OCEANS_MAP = {
    "USA": ["Pacific Ocean", "Atlantic Ocean", "Arctic Ocean"],
    "CAN": ["Arctic Ocean", "Atlantic Ocean", "Pacific Ocean"],
    "MEX": ["Pacific Ocean", "Atlantic Ocean"],
    "BRA": ["Atlantic Ocean"],
    "ARG": ["Atlantic Ocean"],
    "CHL": ["Pacific Ocean"],
    "PER": ["Pacific Ocean"],
    "COL": ["Pacific Ocean", "Atlantic Ocean"],
    "RUS": ["Arctic Ocean", "Pacific Ocean", "Atlantic Ocean"],
    "CHN": ["Pacific Ocean"],
    "IND": ["Indian Ocean"],
    "JPN": ["Pacific Ocean"],
    "AUS": ["Indian Ocean", "Pacific Ocean", "Southern Ocean"],
    "NZL": ["Pacific Ocean", "Southern Ocean"],
    "IDN": ["Indian Ocean", "Pacific Ocean"],
    "PHL": ["Pacific Ocean"],
    "VNM": ["Pacific Ocean"],
    "MYS": ["Pacific Ocean", "Indian Ocean"],
    "THA": ["Pacific Ocean", "Indian Ocean"],
    "GBR": ["Atlantic Ocean"],
    "FRA": ["Atlantic Ocean"],
    "ESP": ["Atlantic Ocean"],
    "PRT": ["Atlantic Ocean"],
    "DEU": ["Atlantic Ocean"],
    "ITA": ["Atlantic Ocean"],
    "NOR": ["Atlantic Ocean", "Arctic Ocean"],
    "SWE": ["Atlantic Ocean"],
    "FIN": ["Atlantic Ocean"],
    "ISL": ["Atlantic Ocean", "Arctic Ocean"],
    "IRL": ["Atlantic Ocean"],
    "EGY": ["Atlantic Ocean", "Indian Ocean"],
    "ZAF": ["Atlantic Ocean", "Indian Ocean"],
    "NGA": ["Atlantic Ocean"],
    "KEN": ["Indian Ocean"],
    "TZA": ["Indian Ocean"],
    "MOZ": ["Indian Ocean"],
    "SAU": ["Indian Ocean"],
    "IRN": ["Indian Ocean"],
    "TUR": ["Atlantic Ocean"],
    "KOR": ["Pacific Ocean"],
    "PRK": ["Pacific Ocean"],
    "PAK": ["Indian Ocean"],
    "BGD": ["Indian Ocean"],
    "MMR": ["Indian Ocean"],
    "OMN": ["Indian Ocean"],
    "YEM": ["Indian Ocean"],
    "ARE": ["Indian Ocean"],
    "ISR": ["Atlantic Ocean", "Indian Ocean"],
    "GRC": ["Atlantic Ocean"],
    "MAR": ["Atlantic Ocean"],
    "DZA": ["Atlantic Ocean"],
    "TUN": ["Atlantic Ocean"],
    "LBY": ["Atlantic Ocean"],
    "SEN": ["Atlantic Ocean"],
    "GHA": ["Atlantic Ocean"],
    "CIV": ["Atlantic Ocean"],
    "CMR": ["Atlantic Ocean"],
    "AGO": ["Atlantic Ocean"],
    "NAM": ["Atlantic Ocean"],
    "MDG": ["Indian Ocean"],
    "SOM": ["Indian Ocean"],
    "CUB": ["Atlantic Ocean"],
    "JAM": ["Atlantic Ocean"],
    "HTI": ["Atlantic Ocean"],
    "DOM": ["Atlantic Ocean"],
    "PAN": ["Pacific Ocean", "Atlantic Ocean"],
    "CRI": ["Pacific Ocean", "Atlantic Ocean"],
    "ECU": ["Pacific Ocean"],
    "VEN": ["Atlantic Ocean"],
    "URY": ["Atlantic Ocean"],
    "GRL": ["Arctic Ocean", "Atlantic Ocean"],
    "SGP": ["Pacific Ocean", "Indian Ocean"],
    "LKA": ["Indian Ocean"]
}

_SEAS_MAP = {
    "USA": ["Bering Sea", "Chukchi Sea", "Beaufort Sea", "Gulf of Mexico", "Caribbean Sea"],
    "CAN": ["Beaufort Sea", "Baffin Bay", "Hudson Bay", "Labrador Sea"],
    "MEX": ["Gulf of Mexico", "Caribbean Sea", "Gulf of California"],
    "BRA": ["South Atlantic Waters"],
    "ARG": ["Argentine Sea", "Scotia Sea"],
    "CHL": ["Chilean Sea", "Drake Passage"],
    "RUS": ["Barents Sea", "Kara Sea", "Laptev Sea", "East Siberian Sea", "Chukchi Sea", "Bering Sea", "Sea of Okhotsk", "Sea of Japan", "Baltic Sea", "Black Sea", "Caspian Sea"],
    "CHN": ["Bohai Sea", "Yellow Sea", "East China Sea", "South China Sea"],
    "IND": ["Arabian Sea", "Bay of Bengal", "Andaman Sea", "Laccadive Sea"],
    "JPN": ["Sea of Japan", "Sea of Okhotsk", "East China Sea", "Philippine Sea"],
    "GBR": ["North Sea", "Irish Sea", "English Channel", "Celtic Sea", "Hebrides Sea"],
    "FRA": ["Mediterranean Sea", "Bay of Biscay", "English Channel", "Celtic Sea", "Ligurian Sea"],
    "DEU": ["North Sea", "Baltic Sea"],
    "ITA": ["Mediterranean Sea", "Adriatic Sea", "Ionian Sea", "Tyrrhenian Sea", "Ligurian Sea"],
    "ESP": ["Mediterranean Sea", "Balearic Sea", "Alboran Sea", "Bay of Biscay"],
    "EGY": ["Mediterranean Sea", "Red Sea", "Gulf of Suez", "Gulf of Aqaba"],
    "SAU": ["Red Sea", "Persian Gulf", "Gulf of Aqaba"],
    "IRN": ["Persian Gulf", "Gulf of Oman", "Caspian Sea"],
    "TUR": ["Mediterranean Sea", "Aegean Sea", "Sea of Marmara", "Black Sea"],
    "GRC": ["Mediterranean Sea", "Aegean Sea", "Ionian Sea", "Sea of Crete"],
    "NOR": ["Norwegian Sea", "Barents Sea", "North Sea"],
    "SWE": ["Baltic Sea", "Gulf of Bothnia", "Kattegat"],
    "FIN": ["Baltic Sea", "Gulf of Finland", "Gulf of Bothnia"],
    "AUS": ["Coral Sea", "Tasman Sea", "Timor Sea", "Arafura Sea", "Great Australian Bight"],
    "IDN": ["Java Sea", "Banda Sea", "Celebes Sea", "Flores Sea", "Molucca Sea", "Timor Sea"],
    "PHL": ["Philippine Sea", "South China Sea", "Sulu Sea", "Celebes Sea"],
    "VNM": ["South China Sea", "Gulf of Tonkin", "Gulf of Thailand"],
    "THA": ["Gulf of Thailand", "Andaman Sea"],
    "MYS": ["South China Sea", "Strait of Malacca", "Sulu Sea"],
    "KOR": ["Sea of Japan (East Sea)", "Yellow Sea", "Korea Strait"],
    "PRK": ["Sea of Japan (East Sea)", "Yellow Sea", "Korea Bay"],
    "PAK": ["Arabian Sea"],
    "BGD": ["Bay of Bengal"],
    "MMR": ["Bay of Bengal", "Andaman Sea"],
    "ZAF": ["South Atlantic Ocean", "South Indian Ocean"],
    "MAR": ["Mediterranean Sea", "Alboran Sea"],
    "DZA": ["Mediterranean Sea"],
    "TUN": ["Mediterranean Sea", "Gulf of Gabes", "Gulf of Tunis"],
    "LBY": ["Mediterranean Sea", "Gulf of Sidra"],
    "ISR": ["Mediterranean Sea", "Red Sea (Gulf of Eilat/Aqaba)"],
    "ARE": ["Persian Gulf", "Gulf of Oman"],
    "QAT": ["Persian Gulf"],
    "KWT": ["Persian Gulf"],
    "IRQ": ["Persian Gulf"],
    "ROU": ["Black Sea"],
    "BGR": ["Black Sea"],
    "UKR": ["Black Sea", "Sea of Azov"],
    "POL": ["Baltic Sea"],
    "DNK": ["North Sea", "Baltic Sea", "Skagerrak", "Kattegat"],
    "NLD": ["North Sea", "Wadden Sea"],
    "BEL": ["North Sea"],
    "IRL": ["Irish Sea", "Celtic Sea"],
    "ISL": ["Greenland Sea", "Norwegian Sea", "Denmark Strait"],
    "CUB": ["Caribbean Sea", "Gulf of Mexico", "Old Bahama Channel"],
    "JAM": ["Caribbean Sea"],
    "COL": ["Caribbean Sea", "Pacific Ocean"],
    "VEN": ["Caribbean Sea", "Gulf of Venezuela"],
    "PAN": ["Caribbean Sea", "Gulf of Panama"],
    "SGP": ["Singapore Strait", "Strait of Malacca"],
    "LKA": ["Gulf of Mannar", "Palk Strait", "Bay of Bengal"]
}

_RIVERS_MAP = {
    "USA": ["Mississippi River (3,770 km)", "Missouri River (3,767 km)", "Yukon River (3,190 km)", "Rio Grande (3,051 km)", "Colorado River (2,330 km)", "Columbia River (2,000 km)", "Ohio River (1,579 km)"],
    "CAN": ["Mackenzie River (4,241 km)", "Yukon River (3,190 km)", "Saint Lawrence River (1,197 km)", "Nelson River (2,575 km)", "Fraser River (1,375 km)"],
    "MEX": ["Rio Grande / Bravo (3,051 km)", "Usumacinta River (1,000 km)", "Grijalva River (480 km)", "Lerma River (708 km)", "Balsas River (771 km)"],
    "BRA": ["Amazon River (6,400 km)", "Paraná River (4,880 km)", "São Francisco River (2,914 km)", "Araguaia River (2,627 km)", "Tocantins River (2,450 km)", "Madeira River (3,380 km)"],
    "ARG": ["Paraná River (4,880 km)", "Uruguay River (1,838 km)", "Paraguay River (2,621 km)", "Río Negro (635 km)", "Colorado River (1,114 km)"],
    "CHL": ["Loa River (440 km)", "Biobío River (380 km)", "Baker River (175 km)", "Maipo River (250 km)"],
    "PER": ["Amazon River (6,400 km)", "Ucayali River (2,738 km)", "Marañón River (1,737 km)", "Putumayo River (1,813 km)"],
    "COL": ["Magdalena River (1,528 km)", "Cauca River (1,180 km)", "Atrato River (750 km)", "Amazon River", "Orinoco River Basin"],
    "RUS": ["Yenisey River (5,539 km)", "Ob River (5,410 km)", "Lena River (4,294 km)", "Amur River (2,824 km)", "Volga River (3,531 km - Longest in Europe)", "Don River (1,870 km)", "Dnieper River"],
    "CHN": ["Yangtze River / Chang Jiang (6,300 km - Longest in Asia)", "Yellow River / Huang He (5,464 km)", "Pearl River / Zhu Jiang (2,400 km)", "Heilongjiang / Amur (2,824 km)", "Lancang / Mekong (4,350 km)", "Yarlung Tsangpo / Brahmaputra"],
    "IND": ["Ganges / Ganga (2,525 km)", "Brahmaputra (2,900 km)", "Indus / Sindhu (3,180 km)", "Godavari (1,465 km)", "Krishna (1,400 km)", "Yamuna (1,376 km)", "Narmada (1,312 km)", "Kaveri (800 km)"],
    "JPN": ["Shinano River (367 km)", "Tone River (322 km)", "Ishikari River (268 km)", "Teshio River (256 km)", "Kitakami River (249 km)"],
    "DEU": ["Rhine River (1,230 km)", "Danube River (2,850 km)", "Elbe River (1,094 km)", "Oder River (854 km)", "Weser River (452 km)", "Main River (527 km)"],
    "FRA": ["Loire River (1,006 km)", "Seine River (777 km)", "Rhône River (812 km)", "Garonne River (602 km)", "Rhine River (border)"],
    "GBR": ["River Severn (354 km)", "River Thames (346 km)", "River Trent (297 km)", "River Wye (250 km)", "River Great Ouse (230 km)", "River Clyde (176 km)"],
    "ITA": ["Po River (652 km)", "Adige River (410 km)", "Tiber / Tevere (405 km)", "Adda River (313 km)", "Arno River (241 km)"],
    "ESP": ["Tagus / Tajo (1,007 km)", "Ebro River (910 km)", "Douro / Duero (897 km)", "Guadiana River (818 km)", "Guadalquivir (657 km)"],
    "EGY": ["Nile River (6,650 km - Longest River in the World)"],
    "ZAF": ["Orange River (2,200 km)", "Limpopo River (1,750 km)", "Vaal River (1,120 km)", "Molopo River (960 km)"],
    "NGA": ["Niger River (4,180 km)", "Benue River (1,400 km)", "Kaduna River (550 km)", "Cross River (489 km)"],
    "KEN": ["Tana River (1,000 km)", "Athi-Galana-Sabaki (390 km)", "Ewaso Ng'iro (700 km)", "Mara River (395 km)"],
    "SAU": ["Wadi al-Batin", "Wadi al-Rummah (Ephemeral stream valleys)", "Wadi Fatima"],
    "IRN": ["Karun River (950 km - Only navigable river)", "Karkheh River (870 km)", "Sefid-Rud (670 km)", "Zayandeh River (400 km)", "Aras River"],
    "TUR": ["Euphrates / Fırat (2,800 km)", "Tigris / Dicle (1,900 km)", "Kızılırmak (1,355 km)", "Sakarya (824 km)", "Aras River (1,072 km)"],
    "AUS": ["Murray River (2,508 km)", "Murrumbidgee River (1,485 km)", "Darling River (1,472 km)", "Lachlan River (1,448 km)", "Cooper Creek (1,300 km)"],
    "IDN": ["Kapuas River (1,143 km)", "Mahakam River (980 km)", "Barito River (900 km)", "Musi River (750 km)", "Solo River (548 km)"],
    "VNM": ["Mekong River (Cuu Long)", "Red River / Song Hong (1,149 km)", "Dong Nai River (586 km)", "Perfume River / Huong (30 km)"],
    "THA": ["Chao Phraya River (372 km)", "Mekong River (border)", "Mun River (750 km)", "Chi River (765 km)", "Nan River (740 km)"],
    "UKR": ["Dnieper River (2,201 km)", "Dniester (1,362 km)", "Southern Bug (806 km)", "Danube Delta", "Donets River"],
    "POL": ["Vistula / Wisła (1,047 km)", "Oder / Odra (854 km)", "Warta River (808 km)", "Bug River (772 km)"],
    "AUT": ["Danube River (2,850 km)", "Inn River (517 km)", "Drava River (710 km)", "Enns River (254 km)", "Salzach (225 km)"],
    "CHE": ["Rhine River (1,230 km)", "Rhône River (812 km)", "Inn River (517 km)", "Aare River (295 km)", "Ticino River (248 km)"],
    "NLD": ["Rhine Delta", "Meuse / Maas (925 km)", "Scheldt (350 km)", "IJssel (125 km)"],
    "PAK": ["Indus River (3,180 km)", "Chenab River (960 km)", "Jhelum River (725 km)", "Ravi River (720 km)", "Sutlej River (1,450 km)"],
    "BGD": ["Padma (Lower Ganges)", "Jamuna (Brahmaputra)", "Meghna River (Ganges Delta)", "Karnafuli (667 km)"],
    "COD": ["Congo River (4,700 km - Deepest river in the world)", "Kasai River (2,153 km)", "Ubangi River (2,270 km)"]
}

# Longest Borders & Neighboring Land Borders (Ranked with Longest First)
_BORDERS_DATA = {
    "USA": [
        {"iso": "CAN", "name": "Canada", "length_km": 8891.0, "is_longest": True, "notes": "Longest international land border in the world (including 2,475 km Alaska border)"},
        {"iso": "MEX", "name": "Mexico", "length_km": 3145.0, "is_longest": False, "notes": "Traversed by Rio Grande & desert border demarcations"}
    ],
    "CAN": [
        {"iso": "USA", "name": "United States", "length_km": 8891.0, "is_longest": True, "notes": "Undefended demilitarized border across 49th parallel and Great Lakes"}
    ],
    "MEX": [
        {"iso": "USA", "name": "United States", "length_km": 3145.0, "is_longest": True, "notes": "Longest border for Mexico, heavily monitored bilateral corridor"},
        {"iso": "GTM", "name": "Guatemala", "length_km": 871.0, "is_longest": False, "notes": "Southern border across Chiapas & Usumacinta River"},
        {"iso": "BLZ", "name": "Belize", "length_km": 250.0, "is_longest": False, "notes": "Border along Hondo River and Chetumal Bay"}
    ],
    "CHN": [
        {"iso": "MNG", "name": "Mongolia", "length_km": 4677.0, "is_longest": True, "notes": "China's longest continuous international land border across the Gobi Desert"},
        {"iso": "RUS", "name": "Russia", "length_km": 4209.3, "is_longest": False, "notes": "Divided into eastern sector (Amur/Ussuri) and western sector"},
        {"iso": "IND", "name": "India", "length_km": 3488.0, "is_longest": False, "notes": "Line of Actual Control (LAC) through Himalayan highlands"},
        {"iso": "MMR", "name": "Myanmar", "length_km": 2185.0, "is_longest": False, "notes": "Jungle and mountainous frontier along Yunnan province"},
        {"iso": "KAZ", "name": "Kazakhstan", "length_km": 1783.0, "is_longest": False, "notes": "Belt & Road continental logistics gateway at Khorgos"},
        {"iso": "PRK", "name": "North Korea", "length_km": 1416.0, "is_longest": False, "notes": "Demarcated by Yalu (Amnok) and Tumen rivers"},
        {"iso": "NPL", "name": "Nepal", "length_km": 1236.0, "is_longest": False, "notes": "Follows the highest ridge of the Himalayas including Mt. Everest"},
        {"iso": "KGZ", "name": "Kyrgyzstan", "length_km": 858.0, "is_longest": False, "notes": "Tian Shan mountain border passes"},
        {"iso": "VNM", "name": "Vietnam", "length_km": 1281.0, "is_longest": False, "notes": "Northern border through Ban Gioc / Detian Falls"},
        {"iso": "LAO", "name": "Laos", "length_km": 423.0, "is_longest": False, "notes": "Highland tropical forest border"},
        {"iso": "TJK", "name": "Tajikistan", "length_km": 414.0, "is_longest": False, "notes": "Pamir Mountains border crossing at Kulma Pass"},
        {"iso": "BTN", "name": "Bhutan", "length_km": 470.0, "is_longest": False, "notes": "Himalayan southern Tibet border"},
        {"iso": "PAK", "name": "Pakistan", "length_km": 523.0, "is_longest": False, "notes": "Connected via Karakoram Highway at Khunjerab Pass"},
        {"iso": "AFG", "name": "Afghanistan", "length_km": 76.0, "is_longest": False, "notes": "Shortest border for China, at the end of the Wakhan Corridor"}
    ],
    "RUS": [
        {"iso": "KAZ", "name": "Kazakhstan", "length_km": 7644.0, "is_longest": True, "notes": "Longest continuous contiguous land border between any two countries in the world"},
        {"iso": "CHN", "name": "China", "length_km": 4209.3, "is_longest": False, "notes": "Major commercial transit along the Amur River"},
        {"iso": "MNG", "name": "Mongolia", "length_km": 3485.0, "is_longest": False, "notes": "Siberian border across Altai Mountains to Sayan Range"},
        {"iso": "UKR", "name": "Ukraine", "length_km": 1974.0, "is_longest": False, "notes": "Southwestern boundary along Don and Dnieper basins"},
        {"iso": "BLR", "name": "Belarus", "length_km": 1239.0, "is_longest": False, "notes": "Union State open border crossing without fixed customs checks"},
        {"iso": "FIN", "name": "Finland", "length_km": 1340.0, "is_longest": False, "notes": "Eastern external border of NATO and the European Union"},
        {"iso": "GEO", "name": "Georgia", "length_km": 894.0, "is_longest": False, "notes": "Caucasus crest including Military Highway at Darial Gorge"},
        {"iso": "AZE", "name": "Azerbaijan", "length_km": 390.0, "is_longest": False, "notes": "Samur River crossing in southern Dagestan"},
        {"iso": "LVA", "name": "Latvia", "length_km": 270.5, "is_longest": False, "notes": "Baltic EU frontier"},
        {"iso": "EST", "name": "Estonia", "length_km": 294.0, "is_longest": False, "notes": "Traversed by Lake Peipus and Narva River"},
        {"iso": "LTU", "name": "Lithuania", "length_km": 273.0, "is_longest": False, "notes": "Kaliningrad exclave perimeter along Curonian Spit"},
        {"iso": "POL", "name": "Poland", "length_km": 232.0, "is_longest": False, "notes": "Kaliningrad exclave southern boundary"},
        {"iso": "NOR", "name": "Norway", "length_km": 195.7, "is_longest": False, "notes": "Arctic Circle frontier at Storskog/Boris Gleb"},
        {"iso": "PRK", "name": "North Korea", "length_km": 17.3, "is_longest": False, "notes": "Shortest Russian border, connected by Druzhba Bridge across Tumen River"}
    ],
    "IND": [
        {"iso": "BGD", "name": "Bangladesh", "length_km": 4096.7, "is_longest": True, "notes": "Fifth longest land border in the world, encircling Bangladesh"},
        {"iso": "CHN", "name": "China", "length_km": 3488.0, "is_longest": False, "notes": "Line of Actual Control (LAC) traversing Ladakh, Uttarakhand, Sikkim & Arunachal"},
        {"iso": "PAK", "name": "Pakistan", "length_km": 3323.0, "is_longest": False, "notes": "Radcliffe Line, Line of Control (LoC), and Sir Creek"},
        {"iso": "NPL", "name": "Nepal", "length_km": 1751.0, "is_longest": False, "notes": "Open border established under the 1950 Indo-Nepal Treaty of Peace and Friendship"},
        {"iso": "MMR", "name": "Myanmar", "length_km": 1643.0, "is_longest": False, "notes": "Himalayan eastern foothills along Mizoram, Manipur, Nagaland, and Arunachal Pradesh"},
        {"iso": "BTN", "name": "Bhutan", "length_km": 699.0, "is_longest": False, "notes": "Peaceful border along Assam, West Bengal, Sikkim and Arunachal Pradesh"}
    ],
    "BRA": [
        {"iso": "BOL", "name": "Bolivia", "length_km": 3400.0, "is_longest": True, "notes": "Brazil's longest border, spanning Pantanal wetlands and Amazon rainforest"},
        {"iso": "VEN", "name": "Venezuela", "length_km": 2200.0, "is_longest": False, "notes": "Northern border through Pacaraima mountains and Mount Roraima"},
        {"iso": "COL", "name": "Colombia", "length_km": 1643.0, "is_longest": False, "notes": "Amazonian rainforest boundary connected at Tabatinga/Leticia"},
        {"iso": "PER", "name": "Peru", "length_km": 1560.0, "is_longest": False, "notes": "Amazon rainforest boundary across Acre and Amazonas"},
        {"iso": "PRY", "name": "Paraguay", "length_km": 1365.0, "is_longest": False, "notes": "Traversed by Paraná River, Itaipu Dam and Friendship Bridge"},
        {"iso": "ARG", "name": "Argentina", "length_km": 1261.0, "is_longest": False, "notes": "Defined by Iguaçu River, Iguazu Falls and Uruguay River"},
        {"iso": "GUY", "name": "Guyana", "length_km": 1119.0, "is_longest": False, "notes": "Northern border through Rupununi savannah and Amazon basin"},
        {"iso": "URY", "name": "Uruguay", "length_km": 985.0, "is_longest": False, "notes": "Southern border across Rio Grande do Sul and Chuy"},
        {"iso": "SUR", "name": "Suriname", "length_km": 597.0, "is_longest": False, "notes": "Tumuc-Humac mountain range boundary"},
        {"iso": "GUF", "name": "French Guiana (France)", "length_km": 673.0, "is_longest": False, "notes": "Border along Oyapock River with Oyapock River Bridge"}
    ],
    "DEU": [
        {"iso": "AUT", "name": "Austria", "length_km": 784.0, "is_longest": True, "notes": "Germany's longest border, traversing Bavarian Alps and Lake Constance"},
        {"iso": "CZE", "name": "Czech Republic", "length_km": 646.0, "is_longest": False, "notes": "Border along Ore Mountains and Bohemian Forest"},
        {"iso": "NLD", "name": "Netherlands", "length_km": 577.0, "is_longest": False, "notes": "Western open Schengen border"},
        {"iso": "POL", "name": "Poland", "length_km": 467.0, "is_longest": False, "notes": "Oder-Neisse line established after WWII"},
        {"iso": "FRA", "name": "France", "length_km": 451.0, "is_longest": False, "notes": "Rhine River border between Baden and Alsace"},
        {"iso": "CHE", "name": "Switzerland", "length_km": 334.0, "is_longest": False, "notes": "Border along High Rhine and Lake Constance"},
        {"iso": "BEL", "name": "Belgium", "length_km": 167.0, "is_longest": False, "notes": "Includes Vennbahn rail enclaves"},
        {"iso": "DNK", "name": "Denmark", "length_km": 68.0, "is_longest": False, "notes": "Jutland peninsula frontier"},
        {"iso": "LUX", "name": "Luxembourg", "length_km": 138.0, "is_longest": False, "notes": "Moselle, Sauer, and Our river boundaries"}
    ],
    "FRA": [
        {"iso": "ESP", "name": "Spain", "length_km": 623.0, "is_longest": True, "notes": "Longest European border for France, traversing Pyrenees mountains"},
        {"iso": "BEL", "name": "Belgium", "length_km": 620.0, "is_longest": False, "notes": "Northern open boundary between Flanders and Wallonia"},
        {"iso": "CHE", "name": "Switzerland", "length_km": 573.0, "is_longest": False, "notes": "Border along Lake Geneva and Jura Mountains"},
        {"iso": "ITA", "name": "Italy", "length_km": 488.0, "is_longest": False, "notes": "Alpine boundary through Mont Blanc massif"},
        {"iso": "DEU", "name": "Germany", "length_km": 451.0, "is_longest": False, "notes": "Upper Rhine river frontier"},
        {"iso": "LUX", "name": "Luxembourg", "length_km": 73.0, "is_longest": False, "notes": "Lorraine iron basin border"},
        {"iso": "AND", "name": "Andorra", "length_km": 57.0, "is_longest": False, "notes": "Pyrenean co-principality border"},
        {"iso": "MCO", "name": "Monaco", "length_km": 4.4, "is_longest": False, "notes": "French Riviera enclave boundary"}
    ],
    "GBR": [
        {"iso": "IRL", "name": "Ireland", "length_km": 499.0, "is_longest": True, "notes": "Only land border of the UK, separating Northern Ireland and the Republic of Ireland"}
    ],
    "ITA": [
        {"iso": "CHE", "name": "Switzerland", "length_km": 740.0, "is_longest": True, "notes": "Alpine watershed boundary along Matterhorn and Monte Rosa"},
        {"iso": "FRA", "name": "France", "length_km": 488.0, "is_longest": False, "notes": "Maritime and Cottian Alps"},
        {"iso": "AUT", "name": "Austria", "length_km": 430.0, "is_longest": False, "notes": "Brenner Pass alpine transit corridor"},
        {"iso": "SVN", "name": "Slovenia", "length_km": 232.0, "is_longest": False, "notes": "Carso plateau and Julian Alps"},
        {"iso": "SMR", "name": "San Marino", "length_km": 39.0, "is_longest": False, "notes": "Enclave in Emilia-Romagna and Marche"},
        {"iso": "VAT", "name": "Vatican City", "length_km": 3.2, "is_longest": False, "notes": "Walled enclave completely inside Rome"}
    ],
    "ARG": [
        {"iso": "CHL", "name": "Chile", "length_km": 5300.0, "is_longest": True, "notes": "Third longest international border in the world, running along Andes spine"},
        {"iso": "PRY", "name": "Paraguay", "length_km": 1880.0, "is_longest": False, "notes": "Pilcomayo, Paraguay and Paraná rivers"},
        {"iso": "BRA", "name": "Brazil", "length_km": 1261.0, "is_longest": False, "notes": "Uruguay and Iguaçu rivers"},
        {"iso": "BOL", "name": "Bolivia", "length_km": 832.0, "is_longest": False, "notes": "Northern Chaco and Andean border"},
        {"iso": "URY", "name": "Uruguay", "length_km": 579.0, "is_longest": False, "notes": "Uruguay River and Río de la Plata"}
    ],
    "ZAF": [
        {"iso": "BWA", "name": "Botswana", "length_km": 1840.0, "is_longest": True, "notes": "Limpopo, Molopo and Nossob rivers"},
        {"iso": "LSO", "name": "Lesotho", "length_km": 909.0, "is_longest": False, "notes": "Enclave nation completely surrounded by South Africa"},
        {"iso": "NAM", "name": "Namibia", "length_km": 967.0, "is_longest": False, "notes": "Orange River and Kalahari frontier"},
        {"iso": "MOZ", "name": "Mozambique", "length_km": 491.0, "is_longest": False, "notes": "Kruger National Park eastern boundary"},
        {"iso": "SWZ", "name": "Eswatini", "length_km": 430.0, "is_longest": False, "notes": "Border encircling Eswatini from west, north, and south"},
        {"iso": "ZWE", "name": "Zimbabwe", "length_km": 225.0, "is_longest": False, "notes": "Limpopo River border with Beitbridge crossing"}
    ],
    "EGY": [
        {"iso": "SDN", "name": "Sudan", "length_km": 1273.0, "is_longest": True, "notes": "Follows the 22nd parallel north, includes Hala'ib Triangle"},
        {"iso": "LBY", "name": "Libya", "length_km": 1115.0, "is_longest": False, "notes": "Western Sahara desert border along 25th meridian east"},
        {"iso": "ISR", "name": "Israel", "length_km": 208.0, "is_longest": False, "notes": "Sinai peninsula border from Taba to Rafah"},
        {"iso": "PSE", "name": "State of Palestine (Gaza)", "length_km": 13.0, "is_longest": False, "notes": "Rafah Border Crossing"}
    ],
    "SAU": [
        {"iso": "YEM", "name": "Yemen", "length_km": 1458.0, "is_longest": True, "notes": "Southern border across Rub' al Khali (Empty Quarter)"},
        {"iso": "IRQ", "name": "Iraq", "length_km": 814.0, "is_longest": False, "notes": "Northern desert frontier with Arar crossing"},
        {"iso": "JOR", "name": "Jordan", "length_km": 744.0, "is_longest": False, "notes": "Northwestern boundary with Al Haditha crossing"},
        {"iso": "OMN", "name": "Oman", "length_km": 676.0, "is_longest": False, "notes": "Empty Quarter boundary at Ramlat Kheylah"},
        {"iso": "ARE", "name": "United Arab Emirates", "length_km": 457.0, "is_longest": False, "notes": "Border at Ghuwaifat crossing"},
        {"iso": "KWT", "name": "Kuwait", "length_km": 222.0, "is_longest": False, "notes": "Partitioned neutral zone boundary at Nuwaiseeb"},
        {"iso": "QAT", "name": "Qatar", "length_km": 60.0, "is_longest": False, "notes": "Salwa land crossing connecting Qatar peninsula"}
    ],
    "JPN": [],
    "AUS": [],
    "NZL": [],
    "ISL": [],
    "MDG": [],
    "PHL": [],
    "CUB": [],
    "SGP": [
        {"iso": "MYS", "name": "Malaysia", "length_km": 1.0, "is_longest": True, "notes": "Connected by Johor-Singapore Causeway and Malaysia-Singapore Second Link bridges"}
    ]
}

class HydrographyService:
    @classmethod
    def get_country_hydrography(cls, country):
        """Return connected oceans, seas, and rivers for a given country."""
        iso = (country.iso_a3 or "").upper()
        oceans = _OCEANS_MAP.get(iso, [])
        seas = _SEAS_MAP.get(iso, [])
        rivers = _RIVERS_MAP.get(iso, [])

        if not oceans:
            if country.is_landlocked:
                oceans = ["Landlocked (No Direct Oceanic Coastline)"]
            elif country.continent_rel:
                c_slug = country.continent_rel.slug
                if c_slug == "europe":
                    oceans = ["Atlantic Ocean"]
                elif c_slug == "asia":
                    oceans = ["Pacific Ocean", "Indian Ocean"]
                elif c_slug == "africa":
                    oceans = ["Atlantic Ocean", "Indian Ocean"]
                else:
                    oceans = ["World Ocean Basin"]

        return {
            "oceans": oceans,
            "seas": seas,
            "rivers": rivers,
            "is_landlocked": country.is_landlocked,
            "coastline_km": country.coastline_km or 0.0
        }

    @classmethod
    def get_ranked_borders(cls, country):
        """
        Return all border sharing countries ranked by border length.
        The longest border is placed at index 0 as highest priority.
        """
        from models.geography import Country, Border
        iso = (country.iso_a3 or "").upper()

        ranked = []
        # Check verified static dataset first
        if iso in _BORDERS_DATA:
            for item in _BORDERS_DATA[iso]:
                target_iso = item["iso"]
                c = Country.query.filter_by(iso_a3=target_iso).first()
                ranked.append({
                    "country": c,
                    "target_iso": target_iso,
                    "name": c.common_name if c else item["name"],
                    "flag": c.flag_emoji if c else "🌐",
                    "slug": c.slug if c else None,
                    "length_km": item["length_km"],
                    "is_longest": item["is_longest"],
                    "notes": item["notes"]
                })
        else:
            # Fallback to database Border table
            db_borders = Border.query.filter(
                (Border.country_a_iso == iso) | (Border.country_b_iso == iso)
            ).order_by(Border.length_km.desc()).all()

            for idx, b in enumerate(db_borders):
                neighbor_iso = b.country_b_iso if b.country_a_iso == iso else b.country_a_iso
                c = Country.query.filter_by(iso_a3=neighbor_iso).first()
                if c:
                    ranked.append({
                        "country": c,
                        "target_iso": neighbor_iso,
                        "name": c.common_name,
                        "flag": c.flag_emoji or "🌐",
                        "slug": c.slug,
                        "length_km": b.length_km or 0.0,
                        "is_longest": idx == 0,
                        "notes": "Official international boundary"
                    })

        # Ensure sorted descending by length_km
        ranked.sort(key=lambda x: x["length_km"] or 0.0, reverse=True)
        if ranked:
            ranked[0]["is_longest"] = True
            for r in ranked[1:]:
                r["is_longest"] = False

        total_border_km = sum(r["length_km"] for r in ranked if r["length_km"])
        for r in ranked:
            r["pct_of_total"] = round((r["length_km"] / total_border_km * 100), 1) if total_border_km > 0 else 0.0

        return {
            "borders": ranked,
            "longest_border": ranked[0] if ranked else None,
            "total_land_border_km": total_border_km,
            "border_count": len(ranked),
            "is_island_nation": len(ranked) == 0 and not country.is_landlocked
        }

    @classmethod
    def get_sea_littoral_countries(cls, sea_name):
        """Return all countries bordering a specific marginal sea."""
        sea_name_lower = (sea_name or "").lower()
        connected = []
        for iso, seas in _SEAS_MAP.items():
            for s in seas:
                if sea_name_lower in s.lower() or s.lower() in sea_name_lower:
                    from models.geography import Country
                    c = Country.query.filter_by(iso_a3=iso).first()
                    if c and c not in connected:
                        connected.append(c)
        return connected
