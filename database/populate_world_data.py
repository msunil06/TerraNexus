"""
TerraNexus Authoritative Global Geographical Data Seeder
Populates comprehensive, verified data for:
- All 7 Continents with accurate country counts
- All 195+ Sovereign World Countries with capitals, coordinates, currencies, populations, flags
- Detailed Capitals for every country with exact GPS coordinates
- World Islands with administrative centers, elevations, surface areas, coordinates
- Key cities and administrative divisions
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import db
from models.geography import Continent, Country, Capital, AdministrativeDivision, City
from models.marine_and_physical import GeographicFeature

def populate_all_world_data(app):
    with app.app_context():
        print("Starting comprehensive global data population...")
        
        # 1. Update/Ensure All 7 Continents
        continents_meta = {
            "asia": {
                "name": "Asia", "code": "AS", "area_km2": 44579000, "population": 4750000000, "countries_count": 49,
                "overview": "Asia is Earth's largest and most populous continent, covering 30% of total land area and home to 60% of world population.",
                "highest_point": "Mount Everest (8,848 m)", "lowest_point": "Dead Sea (-430 m)"
            },
            "africa": {
                "name": "Africa", "code": "AF", "area_km2": 30370000, "population": 1460000000, "countries_count": 54,
                "overview": "Africa is the second-largest and second-most populous continent, spanning the equator across diverse tropical, savanna, and desert biomes.",
                "highest_point": "Mount Kilimanjaro (5,895 m)", "lowest_point": "Lake Assal (-155 m)"
            },
            "europe": {
                "name": "Europe", "code": "EU", "area_km2": 10180000, "population": 745000000, "countries_count": 44,
                "overview": "Europe is situated in the Northern Hemisphere, known for dense cultural heritage, parliamentary governance, and interconnected economies.",
                "highest_point": "Mount Elbrus (5,642 m)", "lowest_point": "Caspian Sea shore (-28 m)"
            },
            "north-america": {
                "name": "North America", "code": "NA", "area_km2": 24709000, "population": 600000000, "countries_count": 23,
                "overview": "North America spans from the Arctic Ocean to the Caribbean Sea, featuring advanced industrial economies and vast natural reserves.",
                "highest_point": "Denali (6,190 m)", "lowest_point": "Death Valley (-86 m)"
            },
            "south-america": {
                "name": "South America", "code": "SA", "area_km2": 17840000, "population": 435000000, "countries_count": 12,
                "overview": "South America is dominated by the Amazon rainforest basin and the Andes mountains, holding extraordinary biological diversity.",
                "highest_point": "Aconcagua (6,961 m)", "lowest_point": "Laguna del Carbón (-105 m)"
            },
            "oceania": {
                "name": "Oceania", "code": "OC", "area_km2": 8525989, "population": 45000000, "countries_count": 14,
                "overview": "Oceania encompasses Australasia, Melanesia, Micronesia, and Polynesia across the Pacific Ocean.",
                "highest_point": "Puncak Jaya (4,884 m)", "lowest_point": "Lake Eyre (-15 m)"
            },
            "antarctica": {
                "name": "Antarctica", "code": "AN", "area_km2": 14200000, "population": 1500, "countries_count": 0,
                "overview": "Antarctica is Earth's southernmost continent, governed under the Antarctic Treaty System dedicated to peaceful scientific investigation.",
                "highest_point": "Vinson Massif (4,892 m)", "lowest_point": "Deep Lake, Vestfold Hills (-50 m)"
            }
        }

        continent_objs = {}
        for slug, cdata in continents_meta.items():
            cont = Continent.query.filter_by(slug=slug).first()
            if not cont:
                cont = Continent(slug=slug, **cdata)
                db.session.add(cont)
                db.session.flush()
            else:
                for k, v in cdata.items():
                    setattr(cont, k, v)
            continent_objs[slug] = cont
        db.session.commit()

        # 2. Comprehensive Countries Catalog
        # Sourced from UN / ISO 3166-1 / World Bank
        countries_master = [
            # ASIA (49)
            ("AF", "AFG", "Afghanistan", "Islamic Republic of Afghanistan", "afghanistan", "asia", "Southern Asia", "Kabul", 34.5553, 69.2075, 41128771, 652230, "AFN", "Afghan Afghani", "؋", "🇦🇫", "Pashto, Dari"),
            ("AM", "ARM", "Armenia", "Republic of Armenia", "armenia", "asia", "Western Asia", "Yerevan", 40.1792, 44.4991, 2780469, 29743, "AMD", "Armenian Dram", "֏", "🇦🇲", "Armenian"),
            ("AZ", "AZE", "Azerbaijan", "Republic of Azerbaijan", "azerbaijan", "asia", "Western Asia", "Baku", 40.4093, 49.8671, 10145212, 86600, "AZN", "Azerbaijani Manat", "₼", "🇦🇿", "Azerbaijani"),
            ("BH", "BHR", "Bahrain", "Kingdom of Bahrain", "bahrain", "asia", "Western Asia", "Manama", 26.2285, 50.5860, 1472233, 765, "BHD", "Bahraini Dinar", ".د.ب", "🇧🇭", "Arabic"),
            ("BD", "BGD", "Bangladesh", "People's Republic of Bangladesh", "bangladesh", "asia", "Southern Asia", "Dhaka", 23.8103, 90.4125, 171186372, 147570, "BDT", "Bangladeshi Taka", "৳", "🇧🇩", "Bengali"),
            ("BT", "BTN", "Bhutan", "Kingdom of Bhutan", "bhutan", "asia", "Southern Asia", "Thimphu", 27.4728, 89.6393, 782455, 38394, "BTN", "Bhutanese Ngultrum", "Nu.", "🇧🇹", "Dzongkha"),
            ("BN", "BRN", "Brunei", "Nation of Brunei, the Abode of Peace", "brunei", "asia", "South-Eastern Asia", "Bandar Seri Begawan", 4.9031, 114.9398, 449002, 5765, "BND", "Brunei Dollar", "$", "🇧🇳", "Malay"),
            ("KH", "KHM", "Cambodia", "Kingdom of Cambodia", "cambodia", "asia", "South-Eastern Asia", "Phnom Penh", 11.5564, 104.9282, 16767842, 181035, "KHR", "Cambodian Riel", "៛", "🇰🇭", "Khmer"),
            ("CN", "CHN", "China", "People's Republic of China", "china", "asia", "Eastern Asia", "Beijing", 39.9042, 116.4074, 1409670000, 9596961, "CNY", "Chinese Yuan", "¥", "🇨🇳", "Standard Chinese"),
            ("CY", "CYP", "Cyprus", "Republic of Cyprus", "cyprus", "asia", "Western Asia", "Nicosia", 35.1856, 33.3823, 1251488, 9251, "EUR", "Euro", "€", "🇨🇾", "Greek, Turkish"),
            ("GE", "GEO", "Georgia", "Georgia", "georgia", "asia", "Western Asia", "Tbilisi", 41.7151, 44.8271, 3712502, 69700, "GEL", "Georgian Lari", "₾", "🇬🇪", "Georgian"),
            ("IN", "IND", "India", "Republic of India", "india", "asia", "Southern Asia", "New Delhi", 28.6139, 77.2090, 1428627663, 3287263, "INR", "Indian Rupee", "₹", "🇮🇳", "Hindi, English"),
            ("ID", "IDN", "Indonesia", "Republic of Indonesia", "indonesia", "asia", "South-Eastern Asia", "Jakarta", -6.2088, 106.8456, 275501339, 1904569, "IDR", "Indonesian Rupiah", "Rp", "🇮🇩", "Indonesian"),
            ("IR", "IRN", "Iran", "Islamic Republic of Iran", "iran", "asia", "Southern Asia", "Tehran", 35.6892, 51.3890, 88550570, 1648195, "IRR", "Iranian Rial", "﷼", "🇮🇷", "Persian"),
            ("IQ", "IRQ", "Iraq", "Republic of Iraq", "iraq", "asia", "Western Asia", "Baghdad", 33.3152, 44.3661, 44496122, 438317, "IQD", "Iraqi Dinar", "ع.د", "🇮🇶", "Arabic, Kurdish"),
            ("IL", "ISR", "Israel", "State of Israel", "israel", "asia", "Western Asia", "Jerusalem", 31.7683, 35.2137, 9550600, 20770, "ILS", "Israeli New Shekel", "₪", "🇮🇱", "Hebrew"),
            ("JP", "JPN", "Japan", "Japan", "japan", "asia", "Eastern Asia", "Tokyo", 35.6762, 139.6503, 124516650, 377975, "JPY", "Japanese Yen", "¥", "🇯🇵", "Japanese"),
            ("JO", "JOR", "Jordan", "Hashemite Kingdom of Jordan", "jordan", "asia", "Western Asia", "Amman", 31.9454, 35.9284, 11285869, 89342, "JOD", "Jordanian Dinar", "د.ا", "🇯🇴", "Arabic"),
            ("KZ", "KAZ", "Kazakhstan", "Republic of Kazakhstan", "kazakhstan", "asia", "Central Asia", "Astana", 51.1694, 71.4491, 19621972, 2724900, "KZT", "Kazakhstani Tenge", "₸", "🇰🇿", "Kazakh, Russian"),
            ("KW", "KWT", "Kuwait", "State of Kuwait", "kuwait", "asia", "Western Asia", "Kuwait City", 29.3759, 47.9774, 4268873, 17818, "KWD", "Kuwaiti Dinar", "د.ك", "🇰🇼", "Arabic"),
            ("KG", "KGZ", "Kyrgyzstan", "Kyrgyz Republic", "kyrgyzstan", "asia", "Central Asia", "Bishkek", 42.8746, 74.5698, 6964000, 199951, "KGS", "Kyrgyzstani Som", "с", "🇰🇬", "Kyrgyz, Russian"),
            ("LA", "LAO", "Laos", "Lao People's Democratic Republic", "laos", "asia", "South-Eastern Asia", "Vientiane", 17.9757, 102.6331, 7529475, 236800, "LAK", "Lao Kip", "₭", "🇱🇦", "Lao"),
            ("LB", "LBN", "Lebanon", "Lebanese Republic", "lebanon", "asia", "Western Asia", "Beirut", 33.8938, 35.5018, 5489739, 10452, "LBP", "Lebanese Pound", "ل.ل", "🇱🇧", "Arabic"),
            ("MY", "MYS", "Malaysia", "Malaysia", "malaysia", "asia", "South-Eastern Asia", "Kuala Lumpur", 3.1390, 101.6869, 33938221, 330803, "MYR", "Malaysian Ringgit", "RM", "🇲🇾", "Malaysian"),
            ("MV", "MDV", "Maldives", "Republic of Maldives", "maldives", "asia", "Southern Asia", "Male", 4.1755, 73.5093, 523781, 298, "MVR", "Maldivian Rufiyaa", "Rf", "🇲🇻", "Dhivehi"),
            ("MN", "MNG", "Mongolia", "Mongolia", "mongolia", "asia", "Eastern Asia", "Ulaanbaatar", 47.8864, 106.9057, 3398366, 1564116, "MNT", "Mongolian Tögrög", "₮", "🇲🇳", "Mongolian"),
            ("MM", "MMR", "Myanmar", "Republic of the Union of Myanmar", "myanmar", "asia", "South-Eastern Asia", "Naypyidaw", 19.7633, 96.0785, 54179306, 676578, "MMK", "Myanmar Kyat", "K", "🇲🇲", "Burmese"),
            ("NP", "NPL", "Nepal", "Federal Democratic Republic of Nepal", "nepal", "asia", "Southern Asia", "Kathmandu", 27.7172, 85.3240, 30547580, 147181, "NPR", "Nepalese Rupee", "₨", "🇳🇵", "Nepali"),
            ("KP", "PRK", "North Korea", "Democratic People's Republic of Korea", "north-korea", "asia", "Eastern Asia", "Pyongyang", 39.0392, 125.7625, 26069416, 120538, "KPW", "North Korean Won", "₩", "🇰🇵", "Korean"),
            ("OM", "OMN", "Oman", "Sultanate of Oman", "oman", "asia", "Western Asia", "Muscat", 23.5859, 58.4059, 4576298, 309500, "OMR", "Omani Rial", "ر.ع.", "🇴🇲", "Arabic"),
            ("PK", "PAK", "Pakistan", "Islamic Republic of Pakistan", "pakistan", "asia", "Southern Asia", "Islamabad", 33.6844, 73.0479, 235824862, 881912, "PKR", "Pakistani Rupee", "₨", "🇵🇰", "Urdu, English"),
            ("PH", "PHL", "Philippines", "Republic of the Philippines", "philippines", "asia", "South-Eastern Asia", "Manila", 14.5995, 120.9842, 115559003, 300000, "PHP", "Philippine Peso", "₱", "🇵🇭", "Filipino, English"),
            ("QA", "QAT", "Qatar", "State of Qatar", "qatar", "asia", "Western Asia", "Doha", 25.2854, 51.5310, 2695122, 11586, "QAR", "Qatari Riyal", "ر.ق", "🇶🇦", "Arabic"),
            ("SA", "SAU", "Saudi Arabia", "Kingdom of Saudi Arabia", "saudi-arabia", "asia", "Western Asia", "Riyadh", 24.7136, 46.6753, 36408820, 2149690, "SAR", "Saudi Riyal", "ر.س", "🇸🇦", "Arabic"),
            ("SG", "SGP", "Singapore", "Republic of Singapore", "singapore", "asia", "South-Eastern Asia", "Singapore", 1.3521, 103.8198, 5637000, 728, "SGD", "Singapore Dollar", "$", "🇸🇬", "English, Malay, Mandarin, Tamil"),
            ("KR", "KOR", "South Korea", "Republic of Korea", "south-korea", "asia", "Eastern Asia", "Seoul", 37.5665, 126.9780, 51692272, 100210, "KRW", "South Korean Won", "₩", "🇰🇷", "Korean"),
            ("LK", "LKA", "Sri Lanka", "Democratic Socialist Republic of Sri Lanka", "sri-lanka", "asia", "Southern Asia", "Colombo", 6.9271, 79.8612, 22181000, 65610, "LKR", "Sri Lankan Rupee", "Rs", "🇱🇰", "Sinhala, Tamil"),
            ("SY", "SYR", "Syria", "Syrian Arab Republic", "syria", "asia", "Western Asia", "Damascus", 33.5138, 36.2765, 22125249, 185180, "SYP", "Syrian Pound", "£S", "🇸🇾", "Arabic"),
            ("TJ", "TJK", "Tajikistan", "Republic of Tajikistan", "tajikistan", "asia", "Central Asia", "Dushanbe", 38.5598, 68.7870, 9952787, 143100, "TJS", "Tajikistani Somoni", "SM", "🇹🇯", "Tajik"),
            ("TH", "THA", "Thailand", "Kingdom of Thailand", "thailand", "asia", "South-Eastern Asia", "Bangkok", 13.7563, 100.5018, 71697030, 513120, "THB", "Thai Baht", "฿", "🇹🇭", "Thai"),
            ("TL", "TLS", "Timor-Leste", "Democratic Republic of Timor-Leste", "timor-leste", "asia", "South-Eastern Asia", "Dili", -8.5569, 125.5603, 1341296, 14874, "USD", "US Dollar", "$", "🇹🇱", "Portuguese, Tetum"),
            ("TR", "TUR", "Turkey", "Republic of Türkiye", "turkey", "asia", "Western Asia", "Ankara", 39.9334, 32.8597, 85279553, 783562, "TRY", "Turkish Lira", "₺", "🇹🇷", "Turkish"),
            ("TM", "TKM", "Turkmenistan", "Turkmenistan", "turkmenistan", "asia", "Central Asia", "Ashgabat", 37.9601, 58.3261, 6430770, 488100, "TMT", "Turkmenistan Manat", "m", "🇹🇲", "Turkmen"),
            ("AE", "ARE", "United Arab Emirates", "United Arab Emirates", "united-arab-emirates", "asia", "Western Asia", "Abu Dhabi", 24.4539, 54.3773, 9441129, 83600, "AED", "UAE Dirham", "د.إ", "🇦🇪", "Arabic"),
            ("UZ", "UZB", "Uzbekistan", "Republic of Uzbekistan", "uzbekistan", "asia", "Central Asia", "Tashkent", 41.2995, 69.2401, 35648100, 447400, "UZS", "Uzbekistani Som", "so'm", "🇺🇿", "Uzbek"),
            ("VN", "VNM", "Vietnam", "Socialist Republic of Vietnam", "vietnam", "asia", "South-Eastern Asia", "Hanoi", 21.0285, 105.8542, 98186856, 331212, "VND", "Vietnamese Dong", "₫", "🇻🇳", "Vietnamese"),
            ("YE", "YEM", "Yemen", "Republic of Yemen", "yemen", "asia", "Western Asia", "Sana'a", 15.3694, 44.1910, 33696614, 527968, "YER", "Yemeni Rial", "﷼", "🇾🇪", "Arabic"),
            ("TW", "TWN", "Taiwan", "Republic of China (Taiwan)", "taiwan", "asia", "Eastern Asia", "Taipei", 25.0330, 121.5654, 23894000, 36197, "TWD", "New Taiwan Dollar", "NT$", "🇹🇼", "Mandarin"),
            ("PS", "PSE", "Palestine", "State of Palestine", "palestine", "asia", "Western Asia", "Ramallah", 31.9038, 35.2034, 5250072, 6020, "ILS", "Israeli Shekel", "₪", "🇵🇸", "Arabic"),

            # AFRICA (54)
            ("DZ", "DZA", "Algeria", "People's Democratic Republic of Algeria", "algeria", "africa", "Northern Africa", "Algiers", 36.7538, 3.0588, 44903225, 2381741, "DZD", "Algerian Dinar", "د.ج", "🇩🇿", "Arabic, Berber"),
            ("AO", "AGO", "Angola", "Republic of Angola", "angola", "africa", "Middle Africa", "Luanda", -8.8390, 13.2894, 35588987, 1246700, "AOA", "Angolan Kwanza", "Kz", "🇦🇴", "Portuguese"),
            ("BJ", "BEN", "Benin", "Republic of Benin", "benin", "africa", "Western Africa", "Porto-Novo", 6.4969, 2.6289, 13352864, 112622, "XOF", "West African CFA Franc", "CFA", "🇧🇯", "French"),
            ("BW", "BWA", "Botswana", "Republic of Botswana", "botswana", "africa", "Southern Africa", "Gaborone", -24.6282, 25.9231, 2630296, 581730, "BWP", "Botswana Pula", "P", "🇧🇼", "English, Tswana"),
            ("BF", "BFA", "Burkina Faso", "Burkina Faso", "burkina-faso", "africa", "Western Africa", "Ouagadougou", 12.3714, -1.5197, 22673762, 274200, "XOF", "West African CFA Franc", "CFA", "🇧🇫", "French"),
            ("BI", "BDI", "Burundi", "Republic of Burundi", "burundi", "africa", "Eastern Africa", "Gitega", -3.4273, 29.9246, 12889576, 27830, "BIF", "Burundian Franc", "FBu", "🇧🇮", "Kirundi, French"),
            ("CV", "CPV", "Cabo Verde", "Republic of Cabo Verde", "cabo-verde", "africa", "Western Africa", "Praia", 14.9330, -23.5133, 593149, 4033, "CVE", "Cape Verdean Escudo", "$", "🇨🇻", "Portuguese"),
            ("CM", "CMR", "Cameroon", "Republic of Cameroon", "cameroon", "africa", "Middle Africa", "Yaounde", 3.8480, 11.5021, 27914536, 475442, "XAF", "Central African CFA Franc", "FCFA", "🇨🇲", "English, French"),
            ("CF", "CAF", "Central African Republic", "Central African Republic", "central-african-republic", "africa", "Middle Africa", "Bangui", 4.3947, 18.5582, 5579144, 622984, "XAF", "Central African CFA Franc", "FCFA", "🇨🇫", "French, Sango"),
            ("TD", "TCD", "Chad", "Republic of Chad", "chad", "africa", "Middle Africa", "N'Djamena", 12.1348, 15.0557, 17723315, 1284000, "XAF", "Central African CFA Franc", "FCFA", "🇹🇩", "French, Arabic"),
            ("KM", "COM", "Comoros", "Union of the Comoros", "comoros", "africa", "Eastern Africa", "Moroni", -11.7172, 43.2473, 836774, 2235, "KMF", "Comorian Franc", "CF", "🇰🇲", "Comorian, French, Arabic"),
            ("CG", "COG", "Congo", "Republic of the Congo", "congo", "africa", "Middle Africa", "Brazzaville", -4.2634, 15.2429, 5970424, 342000, "XAF", "Central African CFA Franc", "FCFA", "🇨🇬", "French"),
            ("CD", "COD", "DR Congo", "Democratic Republic of the Congo", "dr-congo", "africa", "Middle Africa", "Kinshasa", -4.4419, 15.2663, 99010212, 2344858, "CDF", "Congolese Franc", "FC", "🇨🇩", "French"),
            ("CI", "CIV", "Cote d'Ivoire", "Republic of Côte d'Ivoire", "cote-divoire", "africa", "Western Africa", "Yamoussoukro", 6.8276, -5.2893, 28160542, 322463, "XOF", "West African CFA Franc", "CFA", "🇨🇮", "French"),
            ("DJ", "DJI", "Djibouti", "Republic of Djibouti", "djibouti", "africa", "Eastern Africa", "Djibouti City", 11.5721, 43.1456, 1120849, 23200, "DJF", "Djiboutian Franc", "Fdj", "🇩🇯", "Arabic, French"),
            ("EG", "EGY", "Egypt", "Arab Republic of Egypt", "egypt", "africa", "Northern Africa", "Cairo", 30.0444, 31.2357, 109300000, 1002450, "EGP", "Egyptian Pound", "E£", "🇪🇬", "Arabic"),
            ("GQ", "GNQ", "Equatorial Guinea", "Republic of Equatorial Guinea", "equatorial-guinea", "africa", "Middle Africa", "Malabo", 3.7504, 8.7371, 1674908, 28051, "XAF", "Central African CFA Franc", "FCFA", "🇬🇶", "Spanish, French, Portuguese"),
            ("ER", "ERI", "Eritrea", "State of Eritrea", "eritrea", "africa", "Eastern Africa", "Asmara", 15.3229, 38.9251, 3684032, 117600, "ERN", "Eritrean Nakfa", "Nfk", "🇪🇷", "Tigrinya, Arabic, English"),
            ("SZ", "SWZ", "Eswatini", "Kingdom of Eswatini", "eswatini", "africa", "Southern Africa", "Mbabane", -26.3054, 31.1367, 1201670, 17364, "SZL", "Swazi Lilangeni", "L", "🇸🇿", "Swazi, English"),
            ("ET", "ETH", "Ethiopia", "Federal Democratic Republic of Ethiopia", "ethiopia", "africa", "Eastern Africa", "Addis Ababa", 9.0320, 38.7482, 123379924, 1104300, "ETB", "Ethiopian Birr", "Br", "🇪🇹", "Amharic"),
            ("GA", "GAB", "Gabon", "Gabonese Republic", "gabon", "africa", "Middle Africa", "Libreville", 0.4162, 9.4673, 2388992, 267667, "XAF", "Central African CFA Franc", "FCFA", "🇬🇦", "French"),
            ("GM", "GMB", "Gambia", "Republic of the Gambia", "gambia", "africa", "Western Africa", "Banjul", 13.4549, -16.5790, 2705992, 11295, "GMD", "Gambian Dalasi", "D", "🇬🇲", "English"),
            ("GH", "GHA", "Ghana", "Republic of Ghana", "ghana", "africa", "Western Africa", "Accra", 5.6037, -0.1870, 33475870, 238533, "GHS", "Ghanaian Cedi", "₵", "🇬🇭", "English"),
            ("GN", "GIN", "Guinea", "Republic of Guinea", "guinea", "africa", "Western Africa", "Conakry", 9.6412, -13.5784, 13859341, 245857, "GNF", "Guinean Franc", "FG", "🇬🇳", "French"),
            ("GW", "GNB", "Guinea-Bissau", "Republic of Guinea-Bissau", "guinea-bissau", "africa", "Western Africa", "Bissau", 11.8816, -15.6178, 2060721, 36125, "XOF", "West African CFA Franc", "CFA", "🇬🇼", "Portuguese"),
            ("KE", "KEN", "Kenya", "Republic of Kenya", "kenya", "africa", "Eastern Africa", "Nairobi", -1.2921, 36.8219, 54027487, 580367, "KES", "Kenyan Shilling", "KSh", "🇰🇪", "Swahili, English"),
            ("LS", "LSO", "Lesotho", "Kingdom of Lesotho", "lesotho", "africa", "Southern Africa", "Maseru", -29.3151, 27.4869, 2305825, 30355, "LSL", "Lesotho Loti", "L", "🇱🇸", "Sesotho, English"),
            ("LR", "LBR", "Liberia", "Republic of Liberia", "liberia", "africa", "Western Africa", "Monrovia", 6.3156, -10.8074, 5302681, 111369, "LRD", "Liberian Dollar", "$", "🇱🇷", "English"),
            ("LY", "LBY", "Libya", "State of Libya", "libya", "africa", "Northern Africa", "Tripoli", 32.8872, 13.1913, 6812341, 1759540, "LYD", "Libyan Dinar", "ل.د", "🇱🇾", "Arabic"),
            ("MG", "MDG", "Madagascar", "Republic of Madagascar", "madagascar", "africa", "Eastern Africa", "Antananarivo", -18.8792, 47.5079, 29611714, 587041, "MGA", "Malagasy Ariary", "Ar", "🇲🇬", "Malagasy, French"),
            ("MW", "MWI", "Malawi", "Republic of Malawi", "malawi", "africa", "Eastern Africa", "Lilongwe", -13.9626, 33.7741, 20405317, 118484, "MWK", "Malawian Kwacha", "MK", "🇲🇼", "English, Chichewa"),
            ("ML", "MLI", "Mali", "Republic of Mali", "mali", "africa", "Western Africa", "Bamako", 12.6392, -8.0029, 22593590, 1240192, "XOF", "West African CFA Franc", "CFA", "🇲🇱", "French"),
            ("MR", "MRT", "Mauritania", "Islamic Republic of Mauritania", "mauritania", "africa", "Western Africa", "Nouakchott", 18.0735, -15.9582, 4736129, 1030700, "MRU", "Mauritanian Ouguiya", "UM", "🇲🇷", "Arabic"),
            ("MU", "MUS", "Mauritius", "Republic of Mauritius", "mauritius", "africa", "Eastern Africa", "Port Louis", -20.1609, 57.5012, 1299469, 2040, "MUR", "Mauritian Rupee", "₨", "🇲🇺", "English, French"),
            ("MA", "MAR", "Morocco", "Kingdom of Morocco", "morocco", "africa", "Northern Africa", "Rabat", 34.0209, -6.8416, 37457971, 446550, "MAD", "Moroccan Dirham", "د.م.", "🇲🇦", "Arabic, Berber"),
            ("MZ", "MOZ", "Mozambique", "Republic of Mozambique", "mozambique", "africa", "Eastern Africa", "Maputo", -25.9692, 32.5732, 32975440, 801590, "MZN", "Mozambican Metical", "MT", "🇲🇿", "Portuguese"),
            ("NA", "NAM", "Namibia", "Republic of Namibia", "namibia", "africa", "Southern Africa", "Windhoek", -22.5609, 17.0658, 2567012, 825615, "NAD", "Namibian Dollar", "$", "🇳🇦", "English"),
            ("NE", "NER", "Niger", "Republic of the Niger", "niger", "africa", "Western Africa", "Niamey", 13.5116, 2.1254, 26207977, 1267000, "XOF", "West African CFA Franc", "CFA", "🇳🇪", "French"),
            ("NG", "NGA", "Nigeria", "Federal Republic of Nigeria", "nigeria", "africa", "Western Africa", "Abuja", 9.0765, 7.3986, 218541212, 923768, "NGN", "Nigerian Naira", "₦", "🇳🇬", "English"),
            ("RW", "RWA", "Rwanda", "Republic of Rwanda", "rwanda", "africa", "Eastern Africa", "Kigali", -1.9441, 30.0619, 13776698, 26338, "RWF", "Rwandan Franc", "FRw", "🇷🇼", "Kinyarwanda, French, English"),
            ("ST", "STP", "Sao Tome and Principe", "Democratic Republic of São Tomé and Príncipe", "sao-tome-and-principe", "africa", "Middle Africa", "Sao Tome", 0.3302, 6.7273, 227380, 964, "STN", "São Tomé Dobra", "Db", "🇸🇹", "Portuguese"),
            ("SN", "SEN", "Senegal", "Republic of Senegal", "senegal", "africa", "Western Africa", "Dakar", 14.7167, -17.4677, 17316449, 196722, "XOF", "West African CFA Franc", "CFA", "🇸🇳", "French"),
            ("SC", "SYC", "Seychelles", "Republic of Seychelles", "seychelles", "africa", "Eastern Africa", "Victoria", -4.6191, 55.4513, 107118, 452, "SCR", "Seychellois Rupee", "₨", "🇸🇨", "Seychellois Creole, English, French"),
            ("SL", "SLE", "Sierra Leone", "Republic of Sierra Leone", "sierra-leone", "africa", "Western Africa", "Freetown", 8.4840, -13.2299, 8605718, 71740, "SLE", "Sierra Leonean Leone", "Le", "🇸🇱", "English"),
            ("SO", "SOM", "Somalia", "Federal Republic of Somalia", "somalia", "africa", "Eastern Africa", "Mogadishu", 2.0469, 45.3182, 17597511, 637657, "SOS", "Somali Shilling", "Sh", "🇸🇴", "Somali, Arabic"),
            ("ZA", "ZAF", "South Africa", "Republic of South Africa", "south-africa", "africa", "Southern Africa", "Pretoria", -25.7479, 28.2293, 59893885, 1221037, "ZAR", "South African Rand", "R", "🇿🇦", "11 Official Languages"),
            ("SS", "SSD", "South Sudan", "Republic of South Sudan", "south-sudan", "africa", "Eastern Africa", "Juba", 4.8594, 31.5713, 10913164, 619745, "SSP", "South Sudanese Pound", "£", "🇸🇸", "English"),
            ("SD", "SDN", "Sudan", "Republic of the Sudan", "sudan", "africa", "Northern Africa", "Khartoum", 15.5007, 32.5599, 46874204, 1861484, "SDG", "Sudanese Pound", "ج.س.", "🇸🇩", "Arabic, English"),
            ("TZ", "TZA", "Tanzania", "United Republic of Tanzania", "tanzania", "africa", "Eastern Africa", "Dodoma", -6.1630, 35.7516, 65497748, 947303, "TZS", "Tanzanian Shilling", "TSh", "🇹🇿", "Swahili, English"),
            ("TG", "TGO", "Togo", "Togolese Republic", "togo", "africa", "Western Africa", "Lome", 6.1375, 1.2123, 8848699, 56785, "XOF", "West African CFA Franc", "CFA", "🇹🇬", "French"),
            ("TN", "TUN", "Tunisia", "Republic of Tunisia", "tunisia", "africa", "Northern Africa", "Tunis", 36.8065, 10.1815, 12356117, 163610, "TND", "Tunisian Dinar", "د.ت", "🇹🇳", "Arabic"),
            ("UG", "UGA", "Uganda", "Republic of Uganda", "uganda", "africa", "Eastern Africa", "Kampala", 0.3476, 32.5825, 47249585, 241550, "UGX", "Ugandan Shilling", "USh", "🇺🇬", "English, Swahili"),
            ("ZM", "ZMB", "Zambia", "Republic of Zambia", "zambia", "africa", "Eastern Africa", "Lusaka", -15.3875, 28.3228, 20017675, 752618, "ZMW", "Zambian Kwacha", "ZK", "🇿🇲", "English"),
            ("ZW", "ZWE", "Zimbabwe", "Republic of Zimbabwe", "zimbabwe", "africa", "Eastern Africa", "Harare", -17.8252, 31.0335, 16320537, 390757, "ZWG", "Zimbabwe Gold", "$", "🇿🇼", "16 Official Languages"),

            # EUROPE (44)
            ("AL", "ALB", "Albania", "Republic of Albania", "albania", "europe", "Southern Europe", "Tirana", 41.3275, 19.8187, 2775634, 28748, "ALL", "Albanian Lek", "L", "🇦🇱", "Albanian"),
            ("AD", "AND", "Andorra", "Principality of Andorra", "andorra", "europe", "Southern Europe", "Andorra la Vella", 42.5063, 1.5218, 79824, 468, "EUR", "Euro", "€", "🇦🇩", "Catalan"),
            ("AT", "AUT", "Austria", "Republic of Austria", "austria", "europe", "Western Europe", "Vienna", 48.2082, 16.3738, 8956279, 83879, "EUR", "Euro", "€", "🇦🇹", "German"),
            ("BY", "BLR", "Belarus", "Republic of Belarus", "belarus", "europe", "Eastern Europe", "Minsk", 53.9045, 27.5615, 9200617, 207600, "BYN", "Belarusian Ruble", "Br", "🇧🇾", "Belarusian, Russian"),
            ("BE", "BEL", "Belgium", "Kingdom of Belgium", "belgium", "europe", "Western Europe", "Brussels", 50.8503, 4.3517, 11655930, 30528, "EUR", "Euro", "€", "🇧🇪", "Dutch, French, German"),
            ("BA", "BIH", "Bosnia and Herzegovina", "Bosnia and Herzegovina", "bosnia-and-herzegovina", "europe", "Southern Europe", "Sarajevo", 43.8563, 18.4131, 3233526, 51209, "BAM", "Convertible Mark", "KM", "🇧🇦", "Bosnian, Croatian, Serbian"),
            ("BG", "BGR", "Bulgaria", "Republic of Bulgaria", "bulgaria", "europe", "Eastern Europe", "Sofia", 42.6977, 23.3219, 6447710, 110994, "BGN", "Bulgarian Lev", "лв", "🇧🇬", "Bulgarian"),
            ("HR", "HRV", "Croatia", "Republic of Croatia", "croatia", "europe", "Southern Europe", "Zagreb", 45.8150, 15.9819, 3855641, 56594, "EUR", "Euro", "€", "🇭🇷", "Croatian"),
            ("CZ", "CZE", "Czech Republic", "Czech Republic", "czech-republic", "europe", "Eastern Europe", "Prague", 50.0755, 14.4378, 10516707, 78866, "CZK", "Czech Koruna", "Kč", "🇨🇿", "Czech"),
            ("DK", "DNK", "Denmark", "Kingdom of Denmark", "denmark", "europe", "Northern Europe", "Copenhagen", 55.6761, 12.5683, 5903037, 43094, "DKK", "Danish Krone", "kr", "🇩🇰", "Danish"),
            ("EE", "EST", "Estonia", "Republic of Estonia", "estonia", "europe", "Northern Europe", "Tallinn", 59.4370, 24.7536, 1348840, 45227, "EUR", "Euro", "€", "🇪🇪", "Estonian"),
            ("FI", "FIN", "Finland", "Republic of Finland", "finland", "europe", "Northern Europe", "Helsinki", 60.1699, 24.9384, 5540720, 338424, "EUR", "Euro", "€", "🇫🇮", "Finnish, Swedish"),
            ("FR", "FRA", "France", "French Republic", "france", "europe", "Western Europe", "Paris", 48.8566, 2.3522, 67971411, 643801, "EUR", "Euro", "€", "🇫🇷", "French"),
            ("DE", "DEU", "Germany", "Federal Republic of Germany", "germany", "europe", "Western Europe", "Berlin", 52.5200, 13.4050, 84358845, 357022, "EUR", "Euro", "€", "🇩🇪", "German"),
            ("GR", "GRC", "Greece", "Hellenic Republic", "greece", "europe", "Southern Europe", "Athens", 37.9838, 23.7275, 10426915, 131957, "EUR", "Euro", "€", "🇬🇷", "Greek"),
            ("HU", "HUN", "Hungary", "Hungary", "hungary", "europe", "Eastern Europe", "Budapest", 47.4979, 19.0402, 9603634, 93028, "HUF", "Hungarian Forint", "Ft", "🇭🇺", "Hungarian"),
            ("IS", "ISL", "Iceland", "Iceland", "iceland", "europe", "Northern Europe", "Reykjavik", 64.1466, -21.9426, 376248, 103000, "ISK", "Icelandic Króna", "kr", "🇮🇸", "Icelandic"),
            ("IE", "IRL", "Ireland", "Ireland", "ireland", "europe", "Northern Europe", "Dublin", 53.3498, -6.2603, 5127170, 70273, "EUR", "Euro", "€", "🇮🇪", "Irish, English"),
            ("IT", "ITA", "Italy", "Italian Republic", "italy", "europe", "Southern Europe", "Rome", 41.9028, 12.4964, 58850717, 301340, "EUR", "Euro", "€", "🇮🇹", "Italian"),
            ("LV", "LVA", "Latvia", "Republic of Latvia", "latvia", "europe", "Northern Europe", "Riga", 56.9496, 24.1052, 1875757, 64589, "EUR", "Euro", "€", "🇱🇻", "Latvian"),
            ("LI", "LIE", "Liechtenstein", "Principality of Liechtenstein", "liechtenstein", "europe", "Western Europe", "Vaduz", 47.1410, 9.5209, 39327, 160, "CHF", "Swiss Franc", "CHF", "🇱🇮", "German"),
            ("LT", "LTU", "Lithuania", "Republic of Lithuania", "lithuania", "europe", "Northern Europe", "Vilnius", 54.6872, 25.2797, 2833242, 65300, "EUR", "Euro", "€", "🇱🇹", "Lithuanian"),
            ("LU", "LUX", "Luxembourg", "Grand Duchy of Luxembourg", "luxembourg", "europe", "Western Europe", "Luxembourg City", 49.6116, 6.1319, 650774, 2586, "EUR", "Euro", "€", "🇱🇺", "Luxembourgish, French, German"),
            ("MT", "MLT", "Malta", "Republic of Malta", "malta", "europe", "Southern Europe", "Valletta", 35.8989, 14.5146, 533286, 316, "EUR", "Euro", "€", "🇲🇹", "Maltese, English"),
            ("MD", "MDA", "Moldova", "Republic of Moldova", "moldova", "europe", "Eastern Europe", "Chisinau", 47.0105, 28.8638, 2538894, 33846, "MDL", "Moldovan Leu", "L", "🇲🇩", "Romanian"),
            ("MC", "MCO", "Monaco", "Principality of Monaco", "monaco", "europe", "Western Europe", "Monaco", 43.7384, 7.4246, 36469, 2, "EUR", "Euro", "€", "🇲🇨", "French"),
            ("ME", "MNE", "Montenegro", "Montenegro", "montenegro", "europe", "Southern Europe", "Podgorica", 42.4304, 19.2594, 617213, 13812, "EUR", "Euro", "€", "🇲🇪", "Montenegrin"),
            ("NL", "NLD", "Netherlands", "Kingdom of the Netherlands", "netherlands", "europe", "Western Europe", "Amsterdam", 52.3676, 4.9041, 17700982, 41850, "EUR", "Euro", "€", "🇳🇱", "Dutch"),
            ("MK", "MKD", "North Macedonia", "Republic of North Macedonia", "north-macedonia", "europe", "Southern Europe", "Skopje", 41.9973, 21.4280, 2058000, 25713, "MKD", "Macedonian Denar", "ден", "🇲🇰", "Macedonian"),
            ("NO", "NOR", "Norway", "Kingdom of Norway", "norway", "europe", "Northern Europe", "Oslo", 59.9139, 10.7522, 5457127, 385207, "NOK", "Norwegian Krone", "kr", "🇳🇴", "Norwegian"),
            ("PL", "POL", "Poland", "Republic of Poland", "poland", "europe", "Eastern Europe", "Warsaw", 52.2297, 21.0122, 37561599, 312696, "PLN", "Polish Złoty", "zł", "🇵🇱", "Polish"),
            ("PT", "PRT", "Portugal", "Portuguese Republic", "portugal", "europe", "Southern Europe", "Lisbon", 38.7223, -9.1393, 10352042, 92212, "EUR", "Euro", "€", "🇵🇹", "Portuguese"),
            ("RO", "ROU", "Romania", "Romania", "romania", "europe", "Eastern Europe", "Bucharest", 44.4268, 26.1025, 19051562, 238397, "RON", "Romanian Leu", "lei", "🇷🇴", "Romanian"),
            ("SM", "SMR", "San Marino", "Republic of San Marino", "san-marino", "europe", "Southern Europe", "San Marino", 43.9424, 12.4578, 33660, 61, "EUR", "Euro", "€", "🇸🇲", "Italian"),
            ("RS", "SRB", "Serbia", "Republic of Serbia", "serbia", "europe", "Southern Europe", "Belgrade", 44.7866, 20.4489, 6647003, 88361, "RSD", "Serbian Dinar", "дин.", "🇷🇸", "Serbian"),
            ("SK", "SVK", "Slovakia", "Slovak Republic", "slovakia", "europe", "Eastern Europe", "Bratislava", 48.1486, 17.1077, 5428792, 49035, "EUR", "Euro", "€", "🇸🇰", "Slovak"),
            ("SI", "SVN", "Slovenia", "Republic of Slovenia", "slovenia", "europe", "Southern Europe", "Ljubljana", 46.0569, 14.5058, 2111614, 20273, "EUR", "Euro", "€", "🇸🇮", "Slovene"),
            ("ES", "ESP", "Spain", "Kingdom of Spain", "spain", "europe", "Southern Europe", "Madrid", 40.4168, -3.7038, 47778340, 505990, "EUR", "Euro", "€", "🇪🇸", "Spanish"),
            ("SE", "SWE", "Sweden", "Kingdom of Sweden", "sweden", "europe", "Northern Europe", "Stockholm", 59.3293, 18.0686, 10486941, 450295, "SEK", "Swedish Krona", "kr", "🇸🇪", "Swedish"),
            ("CH", "CHE", "Switzerland", "Swiss Confederation", "switzerland", "europe", "Western Europe", "Bern", 46.9480, 7.4474, 8769742, 41285, "CHF", "Swiss Franc", "CHF", "🇨🇭", "German, French, Italian, Romansh"),
            ("UA", "UKR", "Ukraine", "Ukraine", "ukraine", "europe", "Eastern Europe", "Kyiv", 50.4501, 30.5234, 38000000, 603550, "UAH", "Ukrainian Hryvnia", "₴", "🇺🇦", "Ukrainian"),
            ("GB", "GBR", "United Kingdom", "United Kingdom of Great Britain and Northern Ireland", "united-kingdom", "europe", "Northern Europe", "London", 51.5074, -0.1278, 67508936, 242495, "GBP", "British Pound", "£", "🇬🇧", "English"),
            ("VA", "VAT", "Vatican City", "Vatican City State", "vatican-city", "europe", "Southern Europe", "Vatican City", 41.9029, 12.4534, 800, 0.49, "EUR", "Euro", "€", "🇻🇦", "Italian, Latin"),
            ("RU", "RUS", "Russia", "Russian Federation", "russia", "europe", "Eastern Europe", "Moscow", 55.7558, 37.6173, 144236933, 17098246, "RUB", "Russian Ruble", "₽", "🇷🇺", "Russian"),

            # NORTH AMERICA (23)
            ("AG", "ATG", "Antigua and Barbuda", "Antigua and Barbuda", "antigua-and-barbuda", "north-america", "Caribbean", "Saint John's", 17.1274, -61.8468, 93763, 442, "XCD", "East Caribbean Dollar", "$", "🇦🇬", "English"),
            ("BS", "BHS", "Bahamas", "Commonwealth of the Bahamas", "bahamas", "north-america", "Caribbean", "Nassau", 25.0443, -77.3504, 409984, 13943, "BSD", "Bahamian Dollar", "$", "🇧🇸", "English"),
            ("BB", "BRB", "Barbados", "Barbados", "barbados", "north-america", "Caribbean", "Bridgetown", 13.0969, -59.6145, 281635, 430, "BBD", "Barbadian Dollar", "$", "🇧🇧", "English"),
            ("BZ", "BLZ", "Belize", "Belize", "belize", "north-america", "Central America", "Belmopan", 17.2510, -88.7590, 405272, 22966, "BZD", "Belize Dollar", "$", "🇧🇿", "English"),
            ("CA", "CAN", "Canada", "Canada", "canada", "north-america", "Northern America", "Ottawa", 45.4215, -75.6972, 38929902, 9984670, "CAD", "Canadian Dollar", "$", "🇨🇦", "English, French"),
            ("CR", "CRI", "Costa Rica", "Republic of Costa Rica", "costa-rica", "north-america", "Central America", "San Jose", 9.9281, -84.0907, 5180829, 51100, "CRC", "Costa Rican Colón", "₡", "🇨🇷", "Spanish"),
            ("CU", "CUB", "Cuba", "Republic of Cuba", "cuba", "north-america", "Caribbean", "Havana", 23.1136, -82.3666, 11212191, 109884, "CUP", "Cuban Peso", "$", "🇨🇺", "Spanish"),
            ("DM", "DMA", "Dominica", "Commonwealth of Dominica", "dominica", "north-america", "Caribbean", "Roseau", 15.3017, -61.3881, 72737, 751, "XCD", "East Caribbean Dollar", "$", "🇩🇲", "English"),
            ("DO", "DOM", "Dominican Republic", "Dominican Republic", "dominican-republic", "north-america", "Caribbean", "Santo Domingo", 18.4861, -69.9312, 11228821, 48671, "DOP", "Dominican Peso", "$", "🇩🇴", "Spanish"),
            ("SV", "SLV", "El Salvador", "Republic of El Salvador", "el-salvador", "north-america", "Central America", "San Salvador", 13.6929, -89.2182, 6336392, 21041, "USD", "US Dollar", "$", "🇸🇻", "Spanish"),
            ("GD", "GRD", "Grenada", "Grenada", "grenada", "north-america", "Caribbean", "St. George's", 12.0561, -61.7488, 125438, 344, "XCD", "East Caribbean Dollar", "$", "🇬🇩", "English"),
            ("GT", "GTM", "Guatemala", "Republic of Guatemala", "guatemala", "north-america", "Central America", "Guatemala City", 14.6349, -90.5069, 17980803, 108889, "GTQ", "Guatemalan Quetzal", "Q", "🇬🇹", "Spanish"),
            ("HT", "HTI", "Haiti", "Republic of Haiti", "haiti", "north-america", "Caribbean", "Port-au-Prince", 18.5944, -72.3074, 11584996, 27750, "HTG", "Haitian Gourde", "G", "🇭🇹", "French, Haitian Creole"),
            ("HN", "HND", "Honduras", "Republic of Honduras", "honduras", "north-america", "Central America", "Tegucigalpa", 14.0723, -87.1921, 10432860, 112492, "HNL", "Honduran Lempira", "L", "🇭🇳", "Spanish"),
            ("JM", "JAM", "Jamaica", "Jamaica", "jamaica", "north-america", "Caribbean", "Kingston", 17.9712, -76.7936, 2827377, 10991, "JMD", "Jamaican Dollar", "$", "🇯🇲", "English"),
            ("MX", "MEX", "Mexico", "United Mexican States", "mexico", "north-america", "Central America", "Mexico City", 19.4326, -99.1332, 127504125, 1964375, "MXN", "Mexican Peso", "$", "🇲🇽", "Spanish"),
            ("NI", "NIC", "Nicaragua", "Republic of Nicaragua", "nicaragua", "north-america", "Central America", "Managua", 12.1150, -86.2362, 6948392, 130373, "NIO", "Nicaraguan Córdoba", "C$", "🇳🇮", "Spanish"),
            ("PA", "PAN", "Panama", "Republic of Panama", "panama", "north-america", "Central America", "Panama City", 8.9824, -79.5199, 4408581, 75417, "PAB", "Panamanian Balboa", "B/.", "🇵🇦", "Spanish"),
            ("KN", "KNA", "Saint Kitts and Nevis", "Federation of Saint Christopher and Nevis", "saint-kitts-and-nevis", "north-america", "Caribbean", "Basseterre", 17.3026, -62.7177, 47657, 261, "XCD", "East Caribbean Dollar", "$", "🇰🇳", "English"),
            ("LC", "LCA", "Saint Lucia", "Saint Lucia", "saint-lucia", "north-america", "Caribbean", "Castries", 14.0101, -60.9875, 179857, 616, "XCD", "East Caribbean Dollar", "$", "🇱🇨", "English"),
            ("VC", "VCT", "Saint Vincent and the Grenadines", "Saint Vincent and the Grenadines", "saint-vincent-and-the-grenadines", "north-america", "Caribbean", "Kingstown", 13.1600, -61.2248, 103948, 389, "XCD", "East Caribbean Dollar", "$", "🇻🇨", "English"),
            ("TT", "TTO", "Trinidad and Tobago", "Republic of Trinidad and Tobago", "trinidad-and-tobago", "north-america", "Caribbean", "Port of Spain", 10.6549, -61.5019, 1531044, 5130, "TTD", "Trinidad and Tobago Dollar", "$", "🇹🇹", "English"),
            ("US", "USA", "United States", "United States of America", "united-states", "north-america", "Northern America", "Washington D.C.", 38.9072, -77.0369, 334914895, 9833517, "USD", "United States Dollar", "$", "🇺🇸", "English"),

            # SOUTH AMERICA (12)
            ("AR", "ARG", "Argentina", "Argentine Republic", "argentina", "south-america", "South America", "Buenos Aires", -34.6037, -58.3816, 46234830, 2780400, "ARS", "Argentine Peso", "$", "🇦🇷", "Spanish"),
            ("BO", "BOL", "Bolivia", "Plurinational State of Bolivia", "bolivia", "south-america", "South America", "Sucre", -19.0196, -65.2619, 12224110, 1098581, "BOB", "Bolivian Boliviano", "Bs.", "🇧🇴", "Spanish, Quechua, Aymara"),
            ("BR", "BRA", "Brazil", "Federative Republic of Brazil", "brazil", "south-america", "South America", "Brasilia", -15.7975, -47.8919, 215313498, 8515767, "BRL", "Brazilian Real", "R$", "🇧🇷", "Portuguese"),
            ("CL", "CHL", "Chile", "Republic of Chile", "chile", "south-america", "South America", "Santiago", -33.4489, -70.6693, 19603733, 756102, "CLP", "Chilean Peso", "$", "🇨🇱", "Spanish"),
            ("CO", "COL", "Colombia", "Republic of Colombia", "colombia", "south-america", "South America", "Bogota", 4.7110, -74.0721, 51874024, 1141748, "COP", "Colombian Peso", "$", "🇨🇴", "Spanish"),
            ("EC", "ECU", "Ecuador", "Republic of Ecuador", "ecuador", "south-america", "South America", "Quito", -0.1807, -78.4678, 18001000, 276841, "USD", "US Dollar", "$", "🇪🇨", "Spanish"),
            ("GY", "GUY", "Guyana", "Co-operative Republic of Guyana", "guyana", "south-america", "South America", "Georgetown", 6.8013, -58.1551, 808726, 214969, "GYD", "Guyanese Dollar", "$", "🇬🇾", "English"),
            ("PY", "PRY", "Paraguay", "Republic of Paraguay", "paraguay", "south-america", "South America", "Asuncion", -25.2637, -57.5759, 6780744, 406752, "PYG", "Paraguayan Guaraní", "₲", "🇵🇾", "Spanish, Guarani"),
            ("PE", "PER", "Peru", "Republic of Peru", "peru", "south-america", "South America", "Lima", -12.0464, -77.0428, 34049588, 1285216, "PEN", "Peruvian Sol", "S/.", "🇵🇪", "Spanish"),
            ("SR", "SUR", "Suriname", "Republic of Suriname", "suriname", "south-america", "South America", "Paramaribo", 5.8520, -55.2038, 618040, 163820, "SRD", "Surinamese Dollar", "$", "🇸🇷", "Dutch"),
            ("UY", "URY", "Uruguay", "Oriental Republic of Uruguay", "uruguay", "south-america", "South America", "Montevideo", -34.9011, -56.1645, 3422794, 176215, "UYU", "Uruguayan Peso", "$", "🇺🇾", "Spanish"),
            ("VE", "VEN", "Venezuela", "Bolivarian Republic of Venezuela", "venezuela", "south-america", "South America", "Caracas", 10.4806, -66.9036, 28302000, 916445, "VES", "Venezuelan Bolívar", "Bs.", "🇻🇪", "Spanish"),

            # OCEANIA (14)
            ("AU", "AUS", "Australia", "Commonwealth of Australia", "australia", "oceania", "Australasia", "Canberra", -35.2809, 149.1300, 26005540, 7692024, "AUD", "Australian Dollar", "$", "🇦🇺", "English"),
            ("FJ", "FJI", "Fiji", "Republic of Fiji", "fiji", "oceania", "Melanesia", "Suva", -18.1248, 178.4501, 929766, 18274, "FJD", "Fijian Dollar", "$", "🇫🇯", "English, Fijian, Hindi"),
            ("KI", "KIR", "Kiribati", "Republic of Kiribati", "kiribati", "oceania", "Micronesia", "South Tarawa", 1.3291, 172.9790, 131232, 811, "AUD", "Australian Dollar", "$", "🇰🇮", "English, Gilbertese"),
            ("MH", "MHL", "Marshall Islands", "Republic of the Marshall Islands", "marshall-islands", "oceania", "Micronesia", "Majuro", 7.1164, 171.1858, 41569, 181, "USD", "US Dollar", "$", "🇲🇭", "Marshallese, English"),
            ("FM", "FSM", "Micronesia", "Federated States of Micronesia", "micronesia", "oceania", "Micronesia", "Palikir", 6.9248, 158.1611, 114164, 702, "USD", "US Dollar", "$", "🇫🇲", "English"),
            ("NR", "NRU", "Nauru", "Republic of Nauru", "nauru", "oceania", "Micronesia", "Yaren", -0.5477, 166.9209, 12511, 21, "AUD", "Australian Dollar", "$", "🇳🇷", "Nauruan, English"),
            ("NZ", "NZL", "New Zealand", "New Zealand", "new-zealand", "oceania", "Australasia", "Wellington", -41.2865, 174.7762, 5124100, 268838, "NZD", "New Zealand Dollar", "$", "🇳🇿", "English, Māori"),
            ("PW", "PLW", "Palau", "Republic of Palau", "palau", "oceania", "Micronesia", "Ngerulmud", 7.5004, 134.6243, 18055, 459, "USD", "US Dollar", "$", "🇵🇼", "Palauan, English"),
            ("PG", "PNG", "Papua New Guinea", "Independent State of Papua New Guinea", "papua-new-guinea", "oceania", "Melanesia", "Port Moresby", -9.4438, 147.1803, 10142619, 462840, "PGK", "Papua New Guinean Kina", "K", "🇵🇬", "English, Tok Pisin, Hiri Motu"),
            ("WS", "WSM", "Samoa", "Independent State of Samoa", "samoa", "oceania", "Polynesia", "Apia", -13.8333, -171.7667, 222382, 2842, "WST", "Samoan Tālā", "T", "🇼🇸", "Samoan, English"),
            ("SB", "SLB", "Solomon Islands", "Solomon Islands", "solomon-islands", "oceania", "Melanesia", "Honiara", -9.4456, 159.9729, 724273, 28896, "SBD", "Solomon Islands Dollar", "$", "🇸🇧", "English"),
            ("TO", "TON", "Tonga", "Kingdom of Tonga", "tonga", "oceania", "Polynesia", "Nuku'alofa", -21.1393, -175.2018, 106858, 747, "TOP", "Tongan Paʻanga", "T$", "🇹🇴", "Tongan, English"),
            ("TV", "TUV", "Tuvalu", "Tuvalu", "tuvalu", "oceania", "Polynesia", "Funafuti", -8.5211, 179.1962, 11312, 26, "AUD", "Australian Dollar", "$", "🇹🇻", "Tuvaluan, English"),
            ("VU", "VUT", "Vanuatu", "Republic of Vanuatu", "vanuatu", "oceania", "Melanesia", "Port Vila", -17.7333, 168.3273, 326740, 12189, "VUV", "Vanuatu Vatu", "VT", "🇻🇺", "Bislama, English, French")
        ]

        count_created = 0
        count_updated = 0

        for row in countries_master:
            (iso_a2, iso_a3, common_name, official_name, slug, cont_slug, subregion,
             capital_name, cap_lat, cap_lon, pop, area, curr_code, curr_name, curr_sym, flag, langs) = row

            cont_obj = continent_objs.get(cont_slug)
            continent_id = cont_obj.id if cont_obj else 1

            country = Country.query.filter((Country.iso_a2 == iso_a2) | (Country.slug == slug)).first()
            if not country:
                country = Country(
                    iso_a2=iso_a2,
                    iso_a3=iso_a3,
                    common_name=common_name,
                    official_name=official_name,
                    slug=slug,
                    continent_id=continent_id,
                    subregion=subregion,
                    capital_name=capital_name,
                    latitude=cap_lat,
                    longitude=cap_lon,
                    population=pop,
                    area_km2=area,
                    currency_code=curr_code,
                    currency_name=curr_name,
                    currency_symbol=curr_sym,
                    flag_emoji=flag,
                    official_languages=langs,
                    overview=f"{common_name} ({official_name}) is a sovereign nation located in {subregion}, {cont_obj.name if cont_obj else ''}. Its capital and seat of governance is {capital_name}."
                )
                db.session.add(country)
                db.session.flush()
                count_created += 1
            else:
                country.iso_a3 = iso_a3
                country.common_name = common_name
                country.official_name = official_name
                country.continent_id = continent_id
                country.subregion = subregion
                country.capital_name = capital_name
                country.latitude = cap_lat
                country.longitude = cap_lon
                country.population = pop
                country.area_km2 = area
                country.currency_code = curr_code
                country.currency_name = curr_name
                country.currency_symbol = curr_sym
                country.flag_emoji = flag
                country.official_languages = langs
                if not country.overview:
                    country.overview = f"{common_name} ({official_name}) is a sovereign nation located in {subregion}, {cont_obj.name if cont_obj else ''}. Its capital and seat of governance is {capital_name}."
                count_updated += 1

            # Ensure Capital City record exists with exact coordinates
            if capital_name and cap_lat and cap_lon:
                cap = Capital.query.filter_by(country_id=country.id, name=capital_name).first()
                if not cap:
                    cap = Capital(
                        country_id=country.id,
                        name=capital_name,
                        capital_type="primary",
                        latitude=cap_lat,
                        longitude=cap_lon
                    )
                    db.session.add(cap)
                else:
                    cap.latitude = cap_lat
                    cap.longitude = cap_lon

        db.session.commit()
        print(f"Countries populated: {count_created} created, {count_updated} updated.")

        # Update actual count on Continent objects
        for slug, cont in continent_objs.items():
            actual_count = Country.query.filter_by(continent_id=cont.id).count()
            cont.countries_count = actual_count
        db.session.commit()

        # 3. Comprehensive World Islands in GeographicFeature
        islands_master = [
            # name, slug, feature_type, primary_iso, admin_center, area_km2, elev_m, lat, lon, waters, overview
            ("Greenland", "greenland", "island", "DNK", "Nuuk", 2166086, 3694, 71.7069, -42.6043, "Arctic Ocean / North Atlantic", "Greenland is the world's largest island, an autonomous territory within the Kingdom of Denmark. Its capital is Nuuk."),
            ("New Guinea", "new-guinea", "island", "PNG", "Port Moresby", 785753, 4884, -4.0000, 138.0000, "Southwestern Pacific Ocean", "New Guinea is the second-largest island in the world, split between Papua New Guinea (capital: Port Moresby) and Indonesia."),
            ("Borneo", "borneo", "island", "IDN", "Samarinda / Nusantara", 748168, 4095, 0.9619, 114.5548, "South China Sea / Java Sea", "Borneo is the third-largest island in the world, shared by Indonesia, Malaysia, and Brunei. Home to ancient rainforests."),
            ("Madagascar", "madagascar-island", "island", "MDG", "Antananarivo", 587041, 2876, -18.7669, 46.8691, "Indian Ocean / Mozambique Channel", "Madagascar is the fourth-largest island on Earth, home to extraordinary endemic biodiversity. Its capital and largest city is Antananarivo."),
            ("Baffin Island", "baffin-island", "island", "CAN", "Iqaluit", 507451, 2147, 65.4215, -70.9654, "Arctic Archipelago / Baffin Bay", "Baffin Island is Canada's largest island, situated in Nunavut. Its administrative center and territory capital is Iqaluit."),
            ("Sumatra", "sumatra", "island", "IDN", "Medan", 473481, 3805, -0.5897, 101.3431, "Indian Ocean / Strait of Malacca", "Sumatra is the sixth-largest island in the world, situated in western Indonesia. Its largest administrative metropolis is Medan."),
            ("Honshu", "honshu", "island", "JPN", "Tokyo", 227960, 3776, 36.2048, 138.2529, "Pacific Ocean / Sea of Japan", "Honshu is the main and most populous island of Japan, home to the capital Tokyo, Mount Fuji, Kyoto, and Osaka."),
            ("Victoria Island", "victoria-island", "island", "CAN", "Cambridge Bay", 217291, 655, 71.0000, -110.0000, "Canadian Arctic Archipelago", "Victoria Island is Canada's second-largest island. Its primary settlement and administrative hub is Cambridge Bay."),
            ("Great Britain", "great-britain", "island", "GBR", "London", 209331, 1345, 54.0000, -2.0000, "North Atlantic / North Sea", "Great Britain is the largest island of the British Isles, comprising England, Scotland, and Wales. The capital is London."),
            ("South Island (New Zealand)", "south-island-nz", "island", "NZL", "Christchurch", 150437, 3724, -43.9000, 170.5000, "Tasman Sea / South Pacific", "The South Island of New Zealand is renowned for the Southern Alps. Its largest city and regional center is Christchurch."),
            ("North Island (New Zealand)", "north-island-nz", "island", "NZL", "Wellington", 113729, 2797, -38.5000, 175.5000, "Pacific Ocean / Tasman Sea", "The North Island of New Zealand contains the national capital Wellington and the largest metropolitan area, Auckland."),
            ("Cuba", "cuba-island", "island", "CUB", "Havana", 109884, 1974, 21.5218, -77.7812, "Caribbean Sea / Gulf of Mexico", "Cuba is the largest island in the Caribbean, rich in cultural heritage and colonial architecture. Its capital is Havana."),
            ("Iceland", "iceland-island", "island", "ISL", "Reykjavik", 103000, 2110, 64.9631, -19.0208, "North Atlantic / Arctic Ocean", "Iceland is a volcanic island nation on the Mid-Atlantic Ridge. Its vibrant capital and cultural center is Reykjavik."),
            ("Java", "java", "island", "IDN", "Jakarta", 128297, 3676, -7.6145, 110.7122, "Java Sea / Indian Ocean", "Java is the world's most populous island, home to over 150 million people, ancient temples, and Indonesia's capital Jakarta."),
            ("Sri Lanka", "sri-lanka-island", "island", "LKA", "Colombo / Kotte", 65610, 2524, 7.8731, 80.7718, "Indian Ocean / Bay of Bengal", "Sri Lanka is a pearl-shaped island nation in the Indian Ocean, with its commercial capital Colombo and legislative capital Kotte."),
            ("Taiwan", "taiwan-island", "island", "TWN", "Taipei", 36197, 3952, 23.6978, 120.9605, "East China Sea / Pacific Ocean", "Taiwan is a mountainous island in East Asia, globally famous for technology manufacturing and cuisine. Capital is Taipei."),
            ("Hawaii Archipelago", "hawaii-archipelago", "archipelago", "USA", "Honolulu", 28311, 4207, 21.3069, -157.8583, "Central Pacific Ocean", "The Hawaiian Islands are an isolated volcanic archipelago in the Central Pacific. The capital and major port is Honolulu on Oahu."),
            ("Sicily", "sicily", "island", "ITA", "Palermo", 25711, 3357, 37.5990, 14.0154, "Mediterranean Sea", "Sicily is the largest island in the Mediterranean Sea, dominated by Mount Etna. Its historic regional capital is Palermo."),
            ("Puerto Rico", "puerto-rico", "island", "USA", "San Juan", 9104, 1338, 18.2208, -66.5901, "Caribbean Sea / North Atlantic", "Puerto Rico is an island territory in the northeastern Caribbean. Its capital and oldest city is historic San Juan."),
            ("Tasmania", "tasmania", "island", "AUS", "Hobart", 68401, 1617, -42.0409, 146.8087, "Southern Ocean / Tasman Sea", "Tasmania is an Australian island state separated by Bass Strait, known for pristine wilderness. Its capital is Hobart."),
            ("Jamaica", "jamaica-island", "island", "JAM", "Kingston", 10991, 2256, 18.1096, -77.2975, "Caribbean Sea", "Jamaica is an island nation in the Caribbean Sea. Its bustling capital and port city is Kingston."),
            ("Cyprus", "cyprus-island", "island", "CYP", "Nicosia", 9251, 1952, 35.1264, 33.4299, "Eastern Mediterranean Sea", "Cyprus is the third-largest island in the Mediterranean, located south of Turkey. Its ancient divided capital is Nicosia."),
            ("Mallorca", "mallorca", "island", "ESP", "Palma", 3640, 1445, 39.6953, 3.0176, "Balearic Sea (Mediterranean)", "Mallorca is the largest of the Balearic Islands of Spain, a world-famous Mediterranean destination with capital Palma."),
            ("Bali", "bali", "island", "IDN", "Denpasar", 5780, 3142, -8.3405, 115.0920, "Bali Sea / Indian Ocean", "Bali is an iconic Indonesian island famous for volcanic mountains, iconic rice paddies, and coral reefs. Capital: Denpasar."),
            ("Galapagos Islands", "galapagos-islands", "archipelago", "ECU", "Puerto Baquerizo Moreno", 8010, 1707, -0.9538, -90.9656, "Pacific Ocean", "The Galápagos Islands are a UNESCO volcanic archipelago famous for Darwinian evolutionary biodiversity. Capital: Puerto Baquerizo Moreno.")
        ]

        for item in islands_master:
            (name, slug, ftype, iso, admin_center, area, elev, lat, lon, waters, overview) = item
            feat = GeographicFeature.query.filter_by(slug=slug).first()
            if not feat:
                feat = GeographicFeature(
                    name=name,
                    slug=slug,
                    feature_type=ftype,
                    primary_country_iso=iso,
                    administrative_center=admin_center,
                    area_km2=area,
                    elevation_m=elev,
                    latitude=lat,
                    longitude=lon,
                    connected_features=waters,
                    overview=overview
                )
                db.session.add(feat)
            else:
                feat.name = name
                feat.feature_type = ftype
                feat.primary_country_iso = iso
                feat.administrative_center = admin_center
                feat.area_km2 = area
                feat.elevation_m = elev
                feat.latitude = lat
                feat.longitude = lon
                feat.connected_features = waters
                feat.overview = overview

        # 4. Key Administrative Divisions with Capitals for important countries
        divisions_data = [
            # India
            ("Maharashtra", "state", "Mumbai", 19.0760, 72.8777, "IND"),
            ("Delhi", "union_territory", "New Delhi", 28.6139, 77.2090, "IND"),
            ("Karnataka", "state", "Bengaluru", 12.9716, 77.5946, "IND"),
            ("Tamil Nadu", "state", "Chennai", 13.0827, 80.2707, "IND"),
            ("Uttar Pradesh", "state", "Lucknow", 26.8467, 80.9462, "IND"),
            ("Gujarat", "state", "Gandhinagar", 23.2156, 72.6369, "IND"),
            ("West Bengal", "state", "Kolkata", 22.5726, 88.3639, "IND"),
            # United States
            ("California", "state", "Sacramento", 38.5816, -121.4944, "USA"),
            ("New York", "state", "Albany", 42.6526, -73.7562, "USA"),
            ("Texas", "state", "Austin", 30.2672, -97.7431, "USA"),
            ("Florida", "state", "Tallahassee", 30.4383, -84.2807, "USA"),
            ("Illinois", "state", "Springfield", 39.7817, -89.6501, "USA"),
            # Germany
            ("Bavaria", "state", "Munich", 48.1351, 11.5820, "DEU"),
            ("Berlin", "state", "Berlin", 52.5200, 13.4050, "DEU"),
            ("North Rhine-Westphalia", "state", "Dusseldorf", 51.2277, 6.7735, "DEU"),
            # Australia
            ("New South Wales", "state", "Sydney", -33.8688, 151.2093, "AUS"),
            ("Victoria", "state", "Melbourne", -37.8136, 144.9631, "AUS"),
            ("Queensland", "state", "Brisbane", -27.4698, 153.0251, "AUS"),
            # Japan
            ("Tokyo Prefecture", "prefecture", "Shinjuku (Tokyo)", 35.6895, 139.6917, "JPN"),
            ("Osaka Prefecture", "prefecture", "Osaka", 34.6937, 135.5023, "JPN"),
            ("Kyoto Prefecture", "prefecture", "Kyoto", 35.0116, 135.7681, "JPN")
        ]

        for div_name, div_type, center, lat, lon, country_iso in divisions_data:
            c = Country.query.filter_by(iso_a3=country_iso).first()
            if c:
                slug = div_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
                existing_div = AdministrativeDivision.query.filter_by(country_id=c.id, name=div_name).first()
                if not existing_div:
                    div_obj = AdministrativeDivision(
                        country_id=c.id,
                        name=div_name,
                        slug=slug,
                        division_type=div_type,
                        capital_or_center=center,
                        latitude=lat,
                        longitude=lon
                    )
                    db.session.add(div_obj)
                else:
                    existing_div.capital_or_center = center
                    existing_div.latitude = lat
                    existing_div.longitude = lon

        db.session.commit()
        print("Data population completed successfully!")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    populate_all_world_data(app)
