import time
import requests

# Weather Code Mapping per WMO standard
WMO_WEATHER_CODES = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing Rime Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Moderate Drizzle", "🌦️"),
    55: ("Dense Drizzle", "🌧️"),
    61: ("Slight Rain", "🌧️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "⛈️"),
    71: ("Slight Snow", "🌨️"),
    73: ("Moderate Snow", "🌨️"),
    75: ("Heavy Snow", "❄️"),
    77: ("Snow Grains", "❄️"),
    80: ("Slight Rain Showers", "🌦️"),
    81: ("Moderate Rain Showers", "🌧️"),
    82: ("Violent Rain Showers", "⛈️"),
    85: ("Slight Snow Showers", "🌨️"),
    86: ("Heavy Snow Showers", "❄️"),
    95: ("Thunderstorm", "⚡"),
    96: ("Thunderstorm with Slight Hail", "⛈️"),
    99: ("Thunderstorm with Heavy Hail", "⛈️")
}

# In-memory cache to prevent excessive external requests: { key: (timestamp, data) }
_CACHE = {}
CACHE_TTL = 300  # 5 minutes cache

class LiveDataService:
    @staticmethod
    def get_live_weather(lat, lon):
        """Fetch live weather from Open-Meteo Free API (Zero API key required)."""
        if lat is None or lon is None:
            return None

        cache_key = f"weather_{round(lat, 2)}_{round(lon, 2)}"
        now = time.time()
        if cache_key in _CACHE:
            ts, data = _CACHE[cache_key]
            if now - ts < CACHE_TTL:
                return data

        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
            )
            res = requests.get(url, timeout=4)
            if res.ok:
                current = res.json().get("current", {})
                code = current.get("weather_code", 0)
                condition, icon = WMO_WEATHER_CODES.get(code, ("Fair", "☀️"))

                result = {
                    "is_live": True,
                    "temperature_c": current.get("temperature_2m"),
                    "apparent_temperature_c": current.get("apparent_temperature"),
                    "humidity_pct": current.get("relative_humidity_2m"),
                    "wind_speed_kmh": current.get("wind_speed_10m"),
                    "condition": condition,
                    "icon": icon,
                    "time": current.get("time"),
                    "source": "Open-Meteo Free Global Forecast"
                }
                _CACHE[cache_key] = (now, result)
                return result
        except Exception as e:
            # Non-blocking graceful fallback
            pass
        return None

    @staticmethod
    def get_live_exchange_rates(currency_code):
        """Fetch real live currency exchange rates from open.er-api.com (Zero API key required)."""
        if not currency_code:
            return None

        code = currency_code.upper().strip()
        cache_key = f"forex_{code}"
        now = time.time()
        if cache_key in _CACHE:
            ts, data = _CACHE[cache_key]
            if now - ts < CACHE_TTL:
                return data

        try:
            url = f"https://open.er-api.com/v6/latest/{code}"
            res = requests.get(url, timeout=4)
            if res.ok:
                json_data = res.json()
                rates = json_data.get("rates", {})
                
                # Extract key international benchmarks
                benchmarks = {
                    "USD": rates.get("USD"),
                    "EUR": rates.get("EUR"),
                    "GBP": rates.get("GBP"),
                    "JPY": rates.get("JPY"),
                    "INR": rates.get("INR"),
                    "CAD": rates.get("CAD"),
                    "AUD": rates.get("AUD"),
                    "CNY": rates.get("CNY")
                }
                # Remove self currency
                benchmarks.pop(code, None)

                result = {
                    "is_live": True,
                    "base_currency": code,
                    "last_updated": json_data.get("time_last_update_utc"),
                    "rates": benchmarks,
                    "source": "Open Exchange Rates Free API"
                }
                _CACHE[cache_key] = (now, result)
                return result
        except Exception as e:
            pass
        return None

    @staticmethod
    def get_live_country_telemetry(iso_a2):
        """Fetch supplemental live indicators from REST Countries v3.1 (Zero API key required)."""
        if not iso_a2:
            return None

        cache_key = f"telemetry_{iso_a2.upper()}"
        now = time.time()
        if cache_key in _CACHE:
            ts, data = _CACHE[cache_key]
            if now - ts < CACHE_TTL:
                return data

        try:
            url = f"https://restcountries.com/v3.1/alpha/{iso_a2.upper()}"
            res = requests.get(url, timeout=4)
            if res.ok:
                items = res.json()
                if items and isinstance(items, list):
                    item = items[0]
                    coat_of_arms = item.get("coatOfArms", {}).get("svg") or item.get("coatOfArms", {}).get("png")
                    un_member = item.get("unMember", True)
                    gini_data = item.get("gini", {})
                    gini_latest = list(gini_data.values())[-1] if gini_data else None

                    result = {
                        "is_live": True,
                        "un_member": un_member,
                        "coat_of_arms_url": coat_of_arms,
                        "gini_index": gini_latest,
                        "start_of_week": item.get("startOfWeek", "monday").capitalize(),
                        "google_maps_url": item.get("maps", {}).get("googleMaps"),
                        "source": "REST Countries v3.1 Open API"
                    }
                    _CACHE[cache_key] = (now, result)
                    return result
        except Exception as e:
            pass
        return None

    @staticmethod
    def get_live_population(country):
        """
        Calculate high-precision real-time live estimated population and fetch
        authoritative World Bank Demographic indicators (Zero API key required).
        """
        if not country or not country.population:
            return None

        # UN DESA Annual Population Growth Rate Benchmarks (%)
        GROWTH_RATES = {
            "IND": 0.0080, # India ~0.80%
            "CHN": -0.0005,# China -0.05%
            "USA": 0.0050, # US ~0.50%
            "IDN": 0.0074, # Indonesia ~0.74%
            "PAK": 0.0190, # Pakistan ~1.90%
            "NGA": 0.0240, # Nigeria ~2.40%
            "BRA": 0.0052, # Brazil ~0.52%
            "BGD": 0.0103, # Bangladesh ~1.03%
            "RUS": -0.0018,# Russia -0.18%
            "MEX": 0.0075, # Mexico ~0.75%
            "JPN": -0.0053,# Japan -0.53%
            "DEU": -0.0002,# Germany -0.02%
            "GBR": 0.0034, # UK ~0.34%
            "FRA": 0.0028, # France ~0.28%
            "ITA": -0.0025,# Italy -0.25%
            "ZAF": 0.0084, # South Africa ~0.84%
            "AUS": 0.0120, # Australia ~1.20%
            "CAN": 0.0150  # Canada ~1.50%
        }

        iso_a3 = (country.iso_a3 or "").upper()
        growth_rate = GROWTH_RATES.get(iso_a3, 0.0070) # default global avg ~0.70%

        # Calculate time elapsed since base year
        base_pop = country.population
        base_year = country.population_year or 2023
        import datetime
        now_dt = datetime.datetime.now(datetime.timezone.utc)
        base_dt = datetime.datetime(base_year, 1, 1, tzinfo=datetime.timezone.utc)
        elapsed_seconds = (now_dt - base_dt).total_seconds()
        seconds_in_year = 365.25 * 86400.0

        elapsed_years = elapsed_seconds / seconds_in_year
        current_live_estimate = int(base_pop * ((1.0 + growth_rate) ** elapsed_years))

        # Net change per second and daily births/deaths approximation
        net_per_second = (base_pop * growth_rate) / seconds_in_year
        daily_growth = int(net_per_second * 86400)
        global_share = round((current_live_estimate / 8150000000.0) * 100.0, 2)

        # Optional World Bank Open API latest indicator (cached)
        wb_data = None
        if country.iso_a2:
            cache_key = f"wb_pop_{country.iso_a2.upper()}"
            cache_now = time.time()
            if cache_key in _CACHE:
                _, wb_data = _CACHE[cache_key]
            else:
                try:
                    wb_url = f"https://api.worldbank.org/v2/country/{country.iso_a2.upper()}/indicator/SP.POP.TOTL?format=json&per_page=2"
                    wb_res = requests.get(wb_url, timeout=3)
                    if wb_res.ok:
                        wb_json = wb_res.json()
                        if len(wb_json) > 1 and wb_json[1]:
                            latest = wb_json[1][0]
                            wb_data = {
                                "value": latest.get("value"),
                                "date": latest.get("date"),
                                "source": "World Bank Open Data API"
                            }
                            _CACHE[cache_key] = (cache_now, wb_data)
                except Exception:
                    pass

        return {
            "is_live": True,
            "live_population": current_live_estimate,
            "base_population": base_pop,
            "base_year": base_year,
            "annual_growth_rate_pct": round(growth_rate * 100, 2),
            "net_change_per_second": round(net_per_second, 5),
            "daily_net_change": daily_growth,
            "global_share_pct": global_share,
            "world_bank_latest": wb_data,
            "calculation_timestamp": now_dt.isoformat(),
            "source": "UN DESA Demographic Models & World Bank Open Data"
        }

    @classmethod
    def get_composite_live_data(cls, country):
        """Aggregate all live data sources for a country with graceful error isolation."""
        # Find capital coordinates or fallback to country centroid
        capital = country.capitals.first()
        lat = capital.latitude if capital and capital.latitude else country.latitude
        lon = capital.longitude if capital and capital.longitude else country.longitude

        weather = cls.get_live_weather(lat, lon)
        forex = cls.get_live_exchange_rates(country.currency_code)
        telemetry = cls.get_live_country_telemetry(country.iso_a2)
        population = cls.get_live_population(country)

        return {
            "weather": weather,
            "forex": forex,
            "telemetry": telemetry,
            "population": population,
            "has_live_data": bool(weather or forex or telemetry or population)
        }
