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

        return {
            "weather": weather,
            "forex": forex,
            "telemetry": telemetry,
            "has_live_data": bool(weather or forex or telemetry)
        }
